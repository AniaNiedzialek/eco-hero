from fastapi import APIRouter, HTTPException, File, UploadFile
from services.scanner_service import scan_barcode, get_recycling_resources, scrape_cat

router = APIRouter(prefix="/scanner", tags=["scanner"])

@router.get("/status")
def get_status():
    return {"status": "ok"}

@router.post("/uploadfile/")
async def create_upload_file(zip_code: str = None, file: UploadFile = None):
    if not 'image' in file.content_type:
        raise HTTPException(status_code=404, detail={
            "message": "Invalid or missing file type ",
            "payload": file.content_type
        })
    if not zip_code or len(zip_code) < 4:
        raise HTTPException(status_code=404, detail={
            "message": "Invalid or missing zipcode ",
            "payload": zip_code
        })
    
    barcode = scan_barcode(file.file)
    print("DEBUG: barcode =", barcode.text)
    if not barcode:
        raise HTTPException(status_code=404, detail={
            "message": "No valid codes found for barcode ",
            "payload": barcode
        })
    
    resources = get_recycling_resources(barcode.category, zip_code)
    if not resources:
        raise HTTPException(status_code=404, detail={
            "message": "No valid resources found for barcode ",
            "payload": resources
        })
    
    return resources

@router.post("/scanbarcode/")
async def scan_barcode_endpoint(zip_code: str = None, barcode: str = None):
    if not barcode:
        raise HTTPException(status_code=404, detail={
            "message": "Barcode code is required ",
            "payload": barcode
        })
    if not zip_code or len(zip_code) < 4:
        raise HTTPException(status_code=404, detail={
            "message": "Invalid or missing zipcode ",
            "payload": zip_code
        })
    
    category = scrape_cat(barcode)
    resources = get_recycling_resources(category, zip_code)
    if not resources:
        raise HTTPException(status_code=404, detail={
            "message": "No valid resources found for barcode ",
            "payload": resources
        })
    
    return resources
