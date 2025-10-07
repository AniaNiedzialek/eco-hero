import pytest
from services.scanner_service import scan_barcode

def test_scan_barcode():
    barcode = scan_barcode() 
    assert len(barcode) != 0
