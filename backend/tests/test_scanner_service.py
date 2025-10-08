import pytest
from services.scanner_service import scan_barcode, get_recycling_resources

def test_scan_barcode():
    barcode = scan_barcode() 
    assert barcode
    assert barcode.text == '9783981305449'
    assert barcode.category == 'None'
    
def test_get_resources():
    assert len(get_recycling_resources('Food, Beverages & Tobacco', 95051)) > 0
