from fastapi import APIRouter, HTTPException
from services.bin_service import *

router = APIRouter(prefix="/bin", tags=["bin"])

@router.get("/near")
async def get_bins_near(addr: str, radius_miles: int = 20, max_results: int = 10):
    try:
        geoc = geocode_address(addr)
        if geoc:
            lat, lon = geoc
            bins = find_bins_near(lat, lon, radius_miles, max_results)
        else:
            raise HTTPException(400, "Address not found. Please try a more specific address.")
        return bins
    except Exception as e:
        print(f"Geocoding error: {str(e)}")
        raise HTTPException(503, f"Geocoding service temporarily unavailable. Please try again later.")