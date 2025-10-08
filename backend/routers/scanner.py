from fastapi import APIRouter, HTTPException, File, UploadFile
from services.scanner_service import scan_barcode, get_recycling_resources

router = APIRouter(prefix="/scanner", tags=["scanner"])

@router.get("/status")
def get_status():
    return {"status": "ok"}

@router.post("/uploadfile/")
async def create_upload_file(zip_code: str, file: UploadFile):
    if not 'image' in file.content_type:
        raise HTTPException(status_code=404, detail={
            "message": "Invalid file type ",
            "payload": file.content_type
        })
    
    barcode = scan_barcode(file.file)
    if not barcode:
        raise HTTPException(status_code=404, detail={
            "message": "No valid codes found for barcode ",
            "payload": barcode
        })
    
    resources = get_recycling_resources(barcode, zip_code)
    if not resources:
        raise HTTPException(status_code=404, detail={
            "message": "No valid resources found for barcode ",
            "payload": resources
        })
    
    return resources
