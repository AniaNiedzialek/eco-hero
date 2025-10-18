from pathlib import Path
import time
import cv2
import zxingcpp
from bs4 import BeautifulSoup
from selenium import webdriver
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
# TODO: fix to only take in one barcode (to align with get_recycling_resources)
def scan_barcode(img_source=CA_BASELINE_PATH) -> list:
    img = cv2.imread(img_source) if isinstance(img_source, Path) else img_source
    image_bytes = img.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    barcode_data = zxingcpp.read_barcodes(img)
    if barcode_data:
        barcode = barcode_data[0]
        barcodeInfo = BarcodeInfo(barcode.text, barcode.format, barcode.position)
        _set_category(barcodeInfo)
        return barcodeInfo

    return None

def get_recycling_resources(cat: str, zipcode: int) -> Dict[str, str]:
    if cat == 'None':
        return None
    return _scrape_resources(cat, zipcode)

# Webscrape
def _set_category(barcode: BarcodeInfo):
    barcode.category = _scrape_cat(barcode.text) if not MOCK else _scrape_cat('5449000009067')


def _scrape_cat(code: str) -> str:
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
    return 'None'

def _get_dynamic_page_source(url: str):
    driver = webdriver.Chrome()
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
