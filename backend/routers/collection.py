from __future__ import annotations
from fastapi import APIRouter, HTTPException
from scrapers.san_jose import get_san_jose_schedule
import pgeocode

router = APIRouter(prefix="/collection", tags=["collection"])

# -------- Helpers --------
def resolve_region(zip_code: str) -> str:
    z = zip_code.strip()
    if not z.isdigit() or len(z) != 5:
        return None

    # Geocode ZIP
    rec = pgeocode.Nominatim("us").query_postal_code(z)
    if rec is None or rec.empty:
        return None

    city = rec.get("place_name") if "place_name" in rec else None
    state = rec.get("state_code") if "state_code" in rec else None

    return city, state

# -------- Routes --------
@router.get("/schedule")
async def get_collection_schedule(address: str = None, zip_code: str = None) -> dict:
    if not address or len(address.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Address is required. Example: ?address=200+E+Santa+Clara+St"
        )
    
    city = None
    schedule = None
    state = None

    # Convert zip code to city and state
    if zip_code:
        city, state = resolve_region(zip_code)
        print(f"City: {city}")

    match city:
        case "San Jose" | "san jose" | "San José":
            schedule = await get_san_jose_schedule(address)
        # TODO: Add more cities
        case _:
            raise HTTPException(
                status_code=400,
                detail="No available collection schedule found."
            )
    
    if not schedule:
        return {
            "address": address,
            "schedule": [],
            "message": "No collection schedule found for this address. Please verify the address is correct and in San Jose, California."
        }
    
    return {
        "address": address,
        "schedule": schedule,
        "city": city,
        "state": state
    }
