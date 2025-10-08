import pytest
from services.scanner_service import scan_barcode, set_category, get_recycling_resources

def test_scan_barcode():
    barcode = scan_barcode() 
    assert len(barcode) != 0

def test_set_category():
    barcode = scan_barcode() 
    set_category(barcode)
    for b in barcode:
        assert isinstance(b.category, str)
    
def test_get_resources():
    assert len(get_recycling_resources('Food, Beverages & Tobacco')) > 0
