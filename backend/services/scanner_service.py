from pathlib import Path
import time
import cv2
import zxingcpp
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
from dotenv import load_dotenv
from typing import Dict
from urllib.parse import urlencode
import tempfile
import numpy as np

# -------- Mock --------
load_dotenv()
MOCK = os.getenv('MOCK', 'False') == 'True'

# -------- Paths --------
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CA_BASELINE_PATH = DATA_DIR / "barcodes" / "test_bc.png"

# -------- Models --------
class BarcodeInfo:
    def __init__(self, text: str, format: str, position: str):
        self.text = text
        self.format = format 
        self.position = position
        self.category = 'None'

# -------- Helpers --------
def scan_barcode(img_source=CA_BASELINE_PATH) -> BarcodeInfo:
    # Case 1: img_source is a path (str or Path)
    if isinstance(img_source, (str, Path)):
        img = cv2.imread(str(img_source))
        if img is None:
            raise ValueError(f"Could not read image from path: {img_source}")

    # Case 2: img_source is a file-like object (e.g., tempfile or UploadFile.file)
    else:
        image_bytes = img_source.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Could not decode image from file-like object")

    barcode_data = zxingcpp.read_barcodes(img)
    if barcode_data:
        barcode = barcode_data[0]
        barcodeInfo = BarcodeInfo(barcode.text, barcode.format, barcode.position)
        _set_category(barcodeInfo)
        return barcodeInfo

    return None

def get_recycling_resources(cat: str, zipcode: int) -> Dict[str, str]:
    if cat is None:
        return cat
    return _scrape_resources(cat, zipcode)

# Webscrape
def _set_category(barcode: BarcodeInfo):
    barcode.category = scrape_cat(barcode.text) if not MOCK else scrape_cat('5449000009067')

def scrape_cat(code: str) -> str:
    url = f"https://www.barcodelookup.com/{code}"
    if MOCK:
        soup = BeautifulSoup(open('mock_data/barcode_page.html').read(), 'html.parser')
    else:
        html_content = _get_dynamic_page_source(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        
    category_div = soup.find_all('div', class_='product-text-label')
    for div in category_div:
        if div.get_text(strip=True).startswith('Category:'):
            category = div.find('span', class_='product-text').get_text(strip=True)
            return category
    return None

def _get_dynamic_page_source(url: str):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(5)
    page_source = driver.page_source
    driver.quit()
    return page_source

def _build_earth911_url(category: str, zipcode: int, max_distance=25):
    base_url = "https://search.earth911.com/"
    params = {
        "what": category,
        "where": zipcode,
        "list_filter": "all",
        "max_distance": max_distance,
        "family_id": "",
        "latitude": "",
        "longitude": "",
        "country": "",
        "province": "",
        "city": "",
        "sponsor": ""
    }
    return f"{base_url}?{urlencode(params)}"

def _scrape_resources(category: str, zipcode: int) -> Dict[str, str]: 
    url = _build_earth911_url(category, zipcode)
    resources = dict()
    if MOCK:
        soup = BeautifulSoup(open('mock_data/resources_page.html').read(), 'html.parser')
    else:
        html_content = _get_dynamic_page_source(url)
        soup = BeautifulSoup(html_content, 'html.parser')
    
    category_div = soup.find('ul', class_='result-list').find_all_next('div', class_='description')
    for div in category_div:
        title = div.find('h2', class_='title').get_text(strip=True)
        ref = div.find('a')['href']
        if not MOCK:
            ref = 'https://search.earth911.com' + ref
        resources[title] = ref
    return resources
