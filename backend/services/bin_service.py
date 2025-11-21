import requests
import math
import time
from typing import List, Dict, Tuple, Optional

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

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
    params = {
        "q": address,
        "format": "json",
        "limit": "1",
    }
    headers = {
        "User-Agent": "EcoHero/1.0 (eco-waste-management-app; contact: your-email@example.com)"
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            r = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
            r.raise_for_status()
            data = r.json()
            if not data:
                return None
            return float(data[0]["lat"]), float(data[0]["lon"])
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 503 and attempt < max_retries - 1:
                wait_time = 2 ** attempt  
                time.sleep(wait_time)
                continue
            raise
        except Exception:
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
