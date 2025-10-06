from fastapi import APIRouter, HTTPException
from services.rules_service import extract_rules_for_zip 

router = APIRouter(prefix="/rules", tags=["rules"])

@router.get("/status")
def get_status():
    return {"status": "ok"}

@router.get("/{zip_code}")
def get_rules_by_zip(zip_code: str):
    result = extract_rules_for_zip(zip_code)
    if not result.get("rules"):
        raise HTTPException(status_code=404, detail={
            "message": "No rules found for zip code ",
            "payload": result
        })
    return result