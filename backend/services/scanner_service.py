from pathlib import Path
import cv2
import zxingcpp

# -------- Paths --------
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CA_BASELINE_PATH = DATA_DIR / "barcodes" / "test_bc.png"

# -------- Models --------
class BarcodeInfo:
    def __init__(self, text: str, format: str, position: str):
        self.text = text
        self.format = format 
        self.position = position

# -------- Helpers --------
def scan_barcode(img_path=CA_BASELINE_PATH) -> list:
    img = cv2.imread(img_path)
    barcode_data = zxingcpp.read_barcodes(img)
    barcodes = list()

    for barcode in barcode_data:
        print('Found barcode:'
              f'\n Text:        "{barcode.text}"'
              f'\n Format:      "{barcode.format}"'
              f'\n Position:    "{barcode.position}"')
        barcodes.append(BarcodeInfo(barcode.text, barcode.format, barcode.position))
    
    return barcodes
