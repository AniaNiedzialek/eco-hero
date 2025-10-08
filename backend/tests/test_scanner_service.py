import pytest
from services.scanner_service import scan_barcode, set_category

def test_scan_barcode():
    barcode = scan_barcode() 
    assert len(barcode) != 0

def test_set_category():
    assert set_category()
