import asyncio
import json
import logging
from datetime import datetime
import httpx

API_BASE_URL = "https://api.recollect.net/api"
AREA_ID = "recology-1052"
SERVICE_ID = "293"

logger = logging.getLogger(__name__)

async def try_recollect_api(address: str) -> list[dict]:
    """Get schedule data directly from Recollect API."""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            suggestions = await _fetch_address_suggestions(client, address)
            if not suggestions:
                return []
            first_match = suggestions[0]
            place_id = first_match.get("place_id") or first_match.get("id")
            if not place_id:
                return []
            return await _fetch_calendar_for_place(client, place_id)
    except Exception as e:
        logger.exception("API request failed: %s", e)
    return []

async def fetch_calendar(address: str, headless: bool = True):
    return await try_recollect_api(address)

async def _fetch_address_suggestions(client: httpx.AsyncClient, address: str) -> list[dict]:
    url = f"{API_BASE_URL}/areas/{AREA_ID}/services/{SERVICE_ID}/address-suggest"
    try:
        resp = await client.get(url, params={"q": address})
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        logger.warning("Suggest request failed for %s: %s", address, exc)
        return []
    data = resp.json()
    if isinstance(data, list):
        return data
    logger.debug("Unexpected suggest payload: %s", json.dumps(data))
    return []

async def _fetch_calendar_for_place(client: httpx.AsyncClient, place_id: str) -> list[dict]:
    year = datetime.now().year
    params = {"after": f"{year}-01-01", "before": f"{year}-12-31"}
    url = f"{API_BASE_URL}/places/{place_id}/services/{SERVICE_ID}/events"
    try:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        logger.warning("Calendar request failed for %s: %s", place_id, exc)
        return []
    payload = resp.json()
    events = payload.get("events", []) if isinstance(payload, dict) else []
    items = []
    for event in events:
        event_date = event.get("day")
        event_type = event.get("name", "")
        if not event_type and event.get("flags"):
            flag_icons = [flag.get("icon", "") for flag in event["flags"] if isinstance(flag, dict)]
            event_type = ", ".join(filter(None, flag_icons))
        event_type = event_type or "Collection"
        if event_date:
            items.append({"date": event_date, "type": event_type})
    if items:
        logger.debug("Retrieved %d events for %s", len(items), place_id)
    return items

if __name__ == "__main__":
    # Test run for a specific address
    test_address = "150 Alviso St, Santa Clara"
    rows = asyncio.run(fetch_calendar(test_address))
    print(json.dumps(rows, indent=2))


