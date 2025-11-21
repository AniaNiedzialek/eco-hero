import requests
import math
import time
import os
from typing import List, Dict, Tuple, Optional

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

def haversine_meters(lat1, lon1, lat2, lon2):
    R = 6371000.0 # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def haversine_miles(lat1, lon1, lat2, lon2):
    return haversine_meters(lat1, lon1, lat2, lon2) / 1609.34

def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Geocode an address using Google Maps Geocoding API.
    Requires GOOGLE_MAPS_API_KEY environment variable.
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set")
    
    params = {
        "address": address,
        "key": GOOGLE_API_KEY,
    }
    
    try:
        r = requests.get(GOOGLE_GEOCODE_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        if data.get("status") == "OK" and data.get("results"):
            location = data["results"][0]["geometry"]["location"]
            return float(location["lat"]), float(location["lng"])
        elif data.get("status") == "ZERO_RESULTS":
            print(f"Address not found: {address}")
            return None
        else:
            print(f"Geocoding failed with status: {data.get('status')}")
            return None
            
    except Exception as e:
        print(f"Geocoding error: {e}")
        raise
    
    return None

def find_bins_near(lat: float, lon: float, radius_miles: int = 20, max_results: int = 10) -> List[Dict]:
    radius_m = radius_miles * 1609.34

    q = f"""
    [out:json][timeout:25];
    (
        node["amenity"="waste_basket"](around:{radius_m},{lat},{lon});
        node["amenity"="litter_bin"](around:{radius_m},{lat},{lon});
        node["amenity"="bin"](around:{radius_m},{lat},{lon});
        node["amenity"="rubbish_bin"](around:{radius_m},{lat},{lon});
    );
    out center;
    """
    headers = {"User-Agent": "eco-hero/1.0"}
    response = requests.post(OVERPASS_URL, data=q, headers=headers, timeout=10)
    response.raise_for_status()
    payload = response.json()
    elements = payload.get("elements", [])
    results = []
    for element in elements:
        el_lat = element.get("lat") or (element.get("center") or {}).get("lat")
        el_lon = element.get("lon") or (element.get("center") or {}).get("lon")
        if el_lat is None or el_lon is None:
            continue
        
        dist = haversine_miles(lat, lon, el_lat, el_lon)

        results.append({
            "id": element.get("id"),
            "lat": el_lat,
            "lon": el_lon,
            "tags": element.get("tags", {}),
            "distance_miles": round(dist, 1)
        })

    # Sort by distance
    results.sort(key=lambda r: r["distance_miles"])
    return results[:max_results]

if __name__ == "__main__":
    addr = "150 Alviso St, Santa Clara, CA"
    geoc = geocode_address(addr)
    if geoc:
        lat, lon = geoc
        bins = find_bins_near(lat, lon, radius_miles=20, max_results=10)
        print(f"Found {len(bins)} bins near {addr}:")
        for b in bins:
            print(b)
    else:
        print("Geocode failed")
