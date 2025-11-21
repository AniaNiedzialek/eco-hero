from fastapi import APIRouter, HTTPException
from services.bin_service import *

router = APIRouter(prefix="/bin", tags=["bin"])

@router.get("/near")
async def get_bins_near(addr: str, radius_miles: int = 20, max_results: int = 10):
    try:
        print(f"Geocoding address: {addr}")
        geoc = geocode_address(addr)
        if geoc:
            lat, lon = geoc
            print(f"Geocoded to: {lat}, {lon}")
            bins = find_bins_near(lat, lon, radius_miles, max_results)
            print(f"Found {len(bins)} bins")
            return bins
        else:
            raise HTTPException(400, "Address not found. Please try a more specific address.")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_bins_near: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(503, f"Service temporarily unavailable: {str(e)}")