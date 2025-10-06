from functools import lru_cache
from pathlib import Path
from typing import Optional, Dict, Any
import json
import pgeocode

# -------- Paths --------
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CA_BASELINE_PATH = DATA_DIR / "state_baselines" / "CA.json"

# -------- Models --------
class RegionInfo:
    def __init__(self, zip_code: str, state_code: str, city: Optional[str]):
        self.zip_code = zip_code
        self.state_code = state_code
        self.city = city

# -------- Helpers --------
@lru_cache(maxsize=1)
def _load_ca_baseline() -> Dict[str, Any]:
    if not CA_BASELINE_PATH.exists():
        raise FileNotFoundError(f"CA baseline not found at {CA_BASELINE_PATH}")
    return json.loads(CA_BASELINE_PATH.read_text(encoding="utf-8"))

def resolve_region(zip_code: str) -> Optional[RegionInfo]:
    z = zip_code.strip()
    if not z.isdigit() or len(z) != 5:
        return None

    # Geocode ZIP
    rec = pgeocode.Nominatim("us").query_postal_code(z)
    if rec is None or rec.empty:
        return None

    # Extract state and city from record
    state_code = rec.get("state_code") if "state_code" in rec else None
    city = rec.get("city") if "city" in rec else None

    if not state_code:
        return None

    return RegionInfo(zip_code=z, state_code=state_code, city=city)

def _merge_rules(dest: Dict[str, Any], src: Dict[str, Any]) -> None:
    if not src: # nothing to merge
        return
    
    # Merge rules
    for k, v in src.items():
        # If key exists in destination with dest[k] is a dict and v is a dict
        # dest[k] dict, v dict -> key exists in both dest and src -> merge
        if k in dest and isinstance(dest[k], dict) and isinstance(v, dict):
            dest[k].update(v)
        else:
            dest[k] = v

# -------- Public API --------
def extract_rules_for_zip(zip_code: str) -> Dict[str, Any]:
    region = resolve_region(zip_code) # Get region for ZIP
    if not region:
        return {
            "zip": zip_code,
            "match_level": None,
            "region": None,
            "rules": None,
            "summary": "Invalid or unknown ZIP."
        }

    merged_rules: Dict[str, Any] = {}
    summary_parts = []
    match_level = None
    match_name = None

    # Apply statewide baseline
    match region.state_code:
        case  "CA": # California
            ca = _load_ca_baseline()
            if ca and ca.get("rules"):
                _merge_rules(merged_rules, ca["rules"]) # Merge ca rules to merged_rules
                summary_parts.append("Applied California statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "CA" # Set match name
        case _: # Invalid state code
            summary_parts.append(f"No baseline rules for state {region.state_code}.")

    # Final payload
    return {
        "zip": region.zip_code,
        "match_level": match_level,
        "match_name": match_name,
        "region": {
            "state": region.state_code,
            "city": region.city
        },
        "summary": " ".join(summary_parts) or None,
        "rules": merged_rules or None
    }
