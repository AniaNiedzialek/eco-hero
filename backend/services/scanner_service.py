from pathlib import Path
import time
import cv2
import zxingcpp
from bs4 import BeautifulSoup
from selenium import webdriver
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any
from urllib.parse import urlencode

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
def scan_barcode(img_path=CA_BASELINE_PATH) -> list:
    img = cv2.imread(img_path)
    barcode_data = zxingcpp.read_barcodes(img)
    barcodes = set()

    for barcode in barcode_data:
        barcodes.add(BarcodeInfo(barcode.text, barcode.format, barcode.position))
    
    return barcodes

# Webscrape
def set_category(barcodes=None):
    if not barcodes:
        _scrape_cat('5449000009067')
    else:
        for barcode in barcodes:
            barcode.category = _scrape_cat(barcode.text)
    return True

def get_recycling_resources(cat: str) -> Dict[str, str]:
    if cat == 'None':
        return None
    return _scrape_resources(cat, 95051)

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
            print(category)
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
        print('Title:', title, 'Ref:', ref)
        resources[title] = ref
    return resources
