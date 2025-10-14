from __future__ import annotations
from fastapi import APIRouter, HTTPException
from scrapers.san_jose import get_san_jose_schedule
from services.notification_service import send_notification
import pgeocode
from pydantic import BaseModel
from services.schedule_service import *

router = APIRouter(prefix="/collection", tags=["collection"])

# -------- Models --------
class NotifyRequest(BaseModel):
    email: str
    address: str
    zip_code: str | None = None


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

    # Check if schedule already exists
    cached_schedule = get_schedule_by_address_and_zip(address, zip_code)
    if cached_schedule and cached_schedule.schedule:
        schedule = cached_schedule.schedule
    else:
        match city:
            case "San Jose" | "san jose" | "San José":
                schedule = await get_san_jose_schedule(address)
            case "Santa Clara" | "santa clara":
                schedule = "https://www.recology.com/recology-south-bay/santa-clara-county-residential/collection-calendar/"
            case "Cupertino" | "cupertino":
                schedule = "https://www.recology.com/recology-south-bay/cupertino/collection-calendar/"
            case "San Francisco" | "san francisco":
                schedule = "https://www.recology.com/recology-san-francisco/collection-calendar/"
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

    # Add schedule to database only if it wasn't cached
    if not cached_schedule:
        add_schedule({
            "address": address,
            "city": city,
            "state": state,
            "zip_code": zip_code,
            "schedule": schedule
        })

    return {
        "address": address,
        "schedule": schedule,
        "city": city,
        "state": state
    }

@router.post("/notify")
async def send_schedule_notification(req: NotifyRequest):
    # Get the schedule first
    schedule_data = await get_collection_schedule(req.address, req.zip_code)
    
    # Check if we found a schedule
    if not schedule_data.get("schedule"):
        raise HTTPException(400, "No schedule found to send")
    
    # Send notification
    try:
        result = send_notification(req.email, schedule_data)
        return {
            "success": True,
            "message": f"Schedule sent to {req.email}",
            "email_id": result.get("id") if isinstance(result, dict) else None
        }
    except Exception as e:
        raise HTTPException(500, f"Failed to send email: {str(e)}")
