from fastapi import APIRouter, HTTPException, File, UploadFile
from services.gemini_scanner_service import identify_product_with_gemini, get_recycling_info_from_barcode
from services.bin_service import find_recycling_places
import cv2
import numpy as np
import zxingcpp

router = APIRouter(prefix="/scanner", tags=["scanner"])

@router.get("/status")
def get_status():
    return {"status": "ok"}

@router.post("/uploadfile/")
async def create_upload_file(zip_code: str = None, file: UploadFile = None):
    if not file or 'image' not in file.content_type:
        raise HTTPException(status_code=400, detail={
            "message": "Invalid or missing file type",
            "payload": file.content_type if file else "No file"
        })
    if not zip_code or len(zip_code) < 4:
        raise HTTPException(status_code=400, detail={
            "message": "Invalid or missing zipcode",
            "payload": zip_code
        })
    
    try:
        print(f"Processing image upload for zip {zip_code}")
        
        # Read image bytes
        image_bytes = await file.read()
        print(f"Image size: {len(image_bytes)} bytes")
        
        # Try to detect barcode first
        barcode_text = None
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is not None:
                print("Image decoded successfully")
                barcode_data = zxingcpp.read_barcodes(img)
                if barcode_data:
                    barcode_text = barcode_data[0].text
                    print(f"Detected barcode: {barcode_text}")
                    result = get_recycling_info_from_barcode(barcode_text)
                    return result
                else:
                    print("No barcode detected in image")
        except Exception as e:
            print(f"Barcode detection failed: {e}")
        
        # If no barcode found, use Gemini
        print("No barcode found, using Gemini Vision API...")
        result = identify_product_with_gemini(image_bytes, barcode_text)
        
        # Find recycling places
        if result.get("material") or result.get("product_name"):
            query_term = result.get("material") or result.get("product_name")
            places = find_recycling_places(f"recycling center for {query_term}", zip_code)
            result["places"] = places
            
        return result
        
    except Exception as e:
        import traceback
        print(f"Error processing image: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail={
            "message": "Failed to process image",
            "error": str(e)
        })

@router.post("/scanbarcode/")
async def scan_barcode_endpoint(zip_code: str = None, barcode: str = None):
    if not barcode:
        raise HTTPException(status_code=400, detail={
            "message": "Barcode code is required",
            "payload": barcode
        })
    if not zip_code or len(zip_code) < 4:
        raise HTTPException(status_code=400, detail={
            "message": "Invalid or missing zipcode",
            "payload": zip_code
        })
    
    try:
        # Use Gemini to get recycling info from barcode
        result = get_recycling_info_from_barcode(barcode)
        
        # Find recycling places
        if result.get("material") or result.get("product_name"):
            query_term = result.get("material") or result.get("product_name")
            places = find_recycling_places(f"recycling center for {query_term}", zip_code)
            result["places"] = places
            
        return result
    except Exception as e:
        print(f"Error processing barcode: {e}")
        raise HTTPException(status_code=500, detail={
            "message": "Failed to process barcode",
            "error": str(e)
        })
