from functools import lru_cache
from pathlib import Path
from typing import Optional, Dict, Any
import json
import pgeocode

# -------- Paths --------
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
CA_BASELINE_PATH = DATA_DIR / "state_baselines" / "CA.json"
OR_baseline_PATH = DATA_DIR / "state_baselines" / "OR.json"
TX_baseline_PATH = DATA_DIR / "state_baselines" / "TX.json"
WA_baseline_PATH = DATA_DIR / "state_baselines" / "WA.json"
ID_baseline_PATH = DATA_DIR / "state_baselines" / "ID.json"
NV_baseline_PATH = DATA_DIR / "state_baselines" / "NV.json"
UT_baseline_PATH = DATA_DIR / "state_baselines" / "UT.json"
AZ_baseline_PATH = DATA_DIR / "state_baselines" / "AZ.json"
WY_baseline_PATH = DATA_DIR / "state_baselines" / "WY.json"
MT_baseline_PATH = DATA_DIR / "state_baselines" / "MT.json"
CO_baseline_PATH = DATA_DIR / "state_baselines" / "CO.json"
NM_baseline_PATH = DATA_DIR / "state_baselines" / "NM.json"
ND_baseline_PATH = DATA_DIR / "state_baselines" / "ND.json"
SD_baseline_PATH = DATA_DIR / "state_baselines" / "SD.json"
NE_baseline_PATH = DATA_DIR / "state_baselines" / "NE.json"
KS_baseline_PATH = DATA_DIR / "state_baselines" / "KS.json"
OK_baseline_PATH = DATA_DIR / "state_baselines" / "OK.json"
AK_baseline_PATH = DATA_DIR / "state_baselines" / "AK.json"
HI_baseline_PATH = DATA_DIR / "state_baselines" / "HI.json"
WI_baseline_PATH = DATA_DIR / "state_baselines" / "WI.json"
MN_baseline_PATH = DATA_DIR / "state_baselines" / "MN.json"
IL_baseline_PATH = DATA_DIR / "state_baselines" / "IL.json"
IN_baseline_PATH = DATA_DIR / "state_baselines" / "IN.json"
OH_baseline_PATH = DATA_DIR / "state_baselines" / "OH.json"
IA_baseline_PATH = DATA_DIR / "state_baselines" / "IA.json"
MO_baseline_PATH = DATA_DIR / "state_baselines" / "MO.json"
MI_baseline_PATH = DATA_DIR / "state_baselines" / "MI.json"

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

# for OR
@lru_cache(maxsize=1)
def _load_or_baseline() -> Dict[str, Any]:
    if not OR_baseline_PATH.exists():
        raise FileNotFoundError(f"OR baseline not found at {OR_baseline_PATH}")
    return json.loads(OR_baseline_PATH.read_text(encoding="utf-8"))

# for TX
@lru_cache(maxsize=1)
def _load_tx_baseline() -> Dict[str, Any]:
    if not TX_baseline_PATH.exists():
        raise FileNotFoundError(f"TX baseline not found at {TX_baseline_PATH}")
    return json.loads(TX_baseline_PATH.read_text(encoding="utf-8"))

# for WA
@lru_cache(maxsize=1)
def _load_wa_baseline() -> Dict[str, Any]:
    if not WA_baseline_PATH.exists():
        raise FileNotFoundError(f"WA baseline not found at {WA_baseline_PATH}")
    return json.loads(WA_baseline_PATH.read_text(encoding="utf-8"))

# for ID
@lru_cache(maxsize=1)
def _load_id_baseline() -> Dict[str, Any]: 
    if not ID_baseline_PATH.exists():
        raise FileNotFoundError(f"ID baseline not found at {ID_baseline_PATH}")
    return json.loads(ID_baseline_PATH.read_text(encoding="utf-8"))

# for NV
@lru_cache(maxsize=1)
def _load_nv_baseline() -> Dict[str, Any]:
    if not NV_baseline_PATH.exists():
        raise FileNotFoundError(f"NV baseline not found at {NV_baseline_PATH}")
    return json.loads(NV_baseline_PATH.read_text(encoding="utf-8"))

# for UT
@lru_cache(maxsize=1)
def _load_ut_baseline() -> Dict[str, Any]:
    if not UT_baseline_PATH.exists():
        raise FileNotFoundError(f"UT baseline not found at {UT_baseline_PATH}")
    return json.loads(UT_baseline_PATH.read_text(encoding="utf-8")) 

# for AZ
@lru_cache(maxsize=1)
def _load_az_baseline() -> Dict[str, Any]:
    if not AZ_baseline_PATH.exists():
        raise FileNotFoundError(f"AZ baseline not found at {AZ_baseline_PATH}")
    return json.loads(AZ_baseline_PATH.read_text(encoding="utf-8"))
# for WY
@lru_cache(maxsize=1)
def _load_wy_baseline() -> Dict[str, Any]:
    if not WY_baseline_PATH.exists():
        raise FileNotFoundError(f"WY baseline not found at {WY_baseline_PATH}")
    return json.loads(WY_baseline_PATH.read_text(encoding="utf-8")) 

# for MT
@lru_cache(maxsize=1)
def _load_mt_baseline() -> Dict[str, Any]:
    if not MT_baseline_PATH.exists():
        raise FileNotFoundError(f"MT baseline not found at {MT_baseline_PATH}")
    return json.loads(MT_baseline_PATH.read_text(encoding="utf-8"))

# for CO
@lru_cache(maxsize=1)      
def _load_co_baseline() -> Dict[str, Any]:
    if not CO_baseline_PATH.exists():
        raise FileNotFoundError(f"CO baseline not found at {CO_baseline_PATH}")
    return json.loads(CO_baseline_PATH.read_text(encoding="utf-8"))
# for NM
@lru_cache(maxsize=1)
def _load_nm_baseline() -> Dict[str, Any]:
    if not NM_baseline_PATH.exists():
        raise FileNotFoundError(f"NM baseline not found at {NM_baseline_PATH}")
    return json.loads(NM_baseline_PATH.read_text(encoding="utf-8"))
# for ND
@lru_cache(maxsize=1)
def _load_nd_baseline() -> Dict[str, Any]:
    if not ND_baseline_PATH.exists():
        raise FileNotFoundError(f"ND baseline not found at {ND_baseline_PATH}")
    return json.loads(ND_baseline_PATH.read_text(encoding="utf-8"))
# for SD
@lru_cache(maxsize=1)
def _load_sd_baseline() -> Dict[str, Any]:  
    if not SD_baseline_PATH.exists():
        raise FileNotFoundError(f"SD baseline not found at {SD_baseline_PATH}")
    return json.loads(SD_baseline_PATH.read_text(encoding="utf-8"))
# for NE
@lru_cache(maxsize=1)
def _load_ne_baseline() -> Dict[str, Any]:
    if not NE_baseline_PATH.exists():
        raise FileNotFoundError(f"NE baseline not found at {NE_baseline_PATH}")
    return json.loads(NE_baseline_PATH.read_text(encoding="utf-8"))
# for KS
@lru_cache(maxsize=1)
def _load_ks_baseline() -> Dict[str, Any]:
    if not KS_baseline_PATH.exists():
        raise FileNotFoundError(f"KS baseline not found at {KS_baseline_PATH}")
    return json.loads(KS_baseline_PATH.read_text(encoding="utf-8"))
# for OK
@lru_cache(maxsize=1)
def _load_ok_baseline() -> Dict[str, Any]:          
    if not OK_baseline_PATH.exists():
        raise FileNotFoundError(f"OK baseline not found at {OK_baseline_PATH}")
    return json.loads(OK_baseline_PATH.read_text(encoding="utf-8"))
# for AK
@lru_cache(maxsize=1)
def _load_ak_baseline() -> Dict[str, Any]:  
    if not AK_baseline_PATH.exists():
        raise FileNotFoundError(f"AK baseline not found at {AK_baseline_PATH}")
    return json.loads(AK_baseline_PATH.read_text(encoding="utf-8"))
# for HI
@lru_cache(maxsize=1)
def _load_hi_baseline() -> Dict[str, Any]:          
    if not HI_baseline_PATH.exists():
        raise FileNotFoundError(f"HI baseline not found at {HI_baseline_PATH}")
    return json.loads(HI_baseline_PATH.read_text(encoding="utf-8"))     
# for WI
@lru_cache(maxsize=1)
def _load_wi_baseline() -> Dict[str, Any]:        
    if not WI_baseline_PATH.exists():
        raise FileNotFoundError(f"WI baseline not found at {WI_baseline_PATH}")
    return json.loads(WI_baseline_PATH.read_text(encoding="utf-8")) 
# for MN
@lru_cache(maxsize=1)
def _load_mn_baseline() -> Dict[str, Any]:
    if not MN_baseline_PATH.exists():
        raise FileNotFoundError(f"MN baseline not found at {MN_baseline_PATH}")
    return json.loads(MN_baseline_PATH.read_text(encoding="utf-8"))
# for IL
@lru_cache(maxsize=1)
def _load_il_baseline() -> Dict[str, Any]:          
    if not IL_baseline_PATH.exists():
        raise FileNotFoundError(f"IL baseline not found at {IL_baseline_PATH}")
    return json.loads(IL_baseline_PATH.read_text(encoding="utf-8"))
# for IN
@lru_cache(maxsize=1)
def _load_in_baseline() -> Dict[str, Any]:
    if not IN_baseline_PATH.exists():
        raise FileNotFoundError(f"IN baseline not found at {IN_baseline_PATH}")
    return json.loads(IN_baseline_PATH.read_text(encoding="utf-8"))
# for OH
@lru_cache(maxsize=1)
def _load_oh_baseline() -> Dict[str, Any]:
    if not OH_baseline_PATH.exists():
        raise FileNotFoundError(f"OH baseline not found at {OH_baseline_PATH}")
    return json.loads(OH_baseline_PATH.read_text(encoding="utf-8"))
# for IA
@lru_cache(maxsize=1)
def _load_ia_baseline() -> Dict[str, Any]:  
    if not IA_baseline_PATH.exists():
        raise FileNotFoundError(f"IA baseline not found at {IA_baseline_PATH}")
    return json.loads(IA_baseline_PATH.read_text(encoding="utf-8"))
# for MO
@lru_cache(maxsize=1)
def _load_mo_baseline() -> Dict[str, Any]:
    if not MO_baseline_PATH.exists():
        raise FileNotFoundError(f"MO baseline not found at {MO_baseline_PATH}")
    return json.loads(MO_baseline_PATH.read_text(encoding="utf-8"))
# for MI
@lru_cache(maxsize=1)
def _load_mi_baseline() -> Dict[str, Any]:  
    if not MI_baseline_PATH.exists():
        raise FileNotFoundError(f"MI baseline not found at {MI_baseline_PATH}")
    return json.loads(MI_baseline_PATH.read_text(encoding="utf-8"))     


# ----Finish adding the states here----


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
        case "OR": # Oregon
            ore = _load_or_baseline()
            if ore and ore.get("rules"):
                _merge_rules(merged_rules, ore["rules"]) # Merge or rules to merged_rules
                summary_parts.append("Applied Oregon statewide bsaeline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "OR" # Set match name
        # TODO: Add other states here
        case "TX": # Texas
            tx = _load_tx_baseline()
            if tx and tx.get("rules"):
                _merge_rules(merged_rules, tx["rules"]) # Merge tx rules to merged_rules
                summary_parts.append("Applied Texas statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "TX" # Set match name
        case "WA": # Washington
            wa = _load_wa_baseline()
            if wa and wa.get("rules"):
                _merge_rules(merged_rules, wa["rules"]) # Merge wa rules to merged_rules
                summary_parts.append("Applied Washington statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "WA" # Set match name
        case "ID": # Idaho
            id = _load_id_baseline()
            if id and id.get("rules"):  # Merge id rules to merged_rules
                _merge_rules(merged_rules, id["rules"]) 
                summary_parts.append("Applied Idaho statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "ID" # Set match name
        case "NV": # Nevada
            nv = _load_nv_baseline()
            if nv and nv.get("rules"):  # Merge nv rules to merged_rules
                _merge_rules(merged_rules, nv["rules"]) 
                summary_parts.append("Applied Nevada statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "NV" # Set match name
        case "UT": # Utah
            ut = _load_ut_baseline()
            if ut and ut.get("rules"):  # Merge ut rules to merged_rules
                _merge_rules(merged_rules, ut["rules"]) 
                summary_parts.append("Applied Utah statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "UT" # Set match name
        case "AZ": # Arizona
            az = _load_az_baseline()
            if az and az.get("rules"):  # Merge az rules to merged_rules        
                _merge_rules(merged_rules, az["rules"]) 
                summary_parts.append("Applied Arizona statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "AZ" # Set match name
        case "WY": # Wyoming
            wy = _load_wy_baseline()
            if wy and wy.get("rules"):  # Merge wy rules to merged_rules        
                _merge_rules(merged_rules, wy["rules"]) 
                summary_parts.append("Applied Wyoming statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "WY" # Set match name
        case "MT": # Montana
            mt = _load_mt_baseline()
            if mt and mt.get("rules"):  # Merge mt rules to merged_rules                
                _merge_rules(merged_rules, mt["rules"]) 
                summary_parts.append("Applied Montana statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "MT" # Set match name
        case "CO": # Colorado
            co = _load_co_baseline()
            if co and co.get("rules"):  # Merge co rules to merged_rules                
                _merge_rules(merged_rules, co["rules"]) 
                summary_parts.append("Applied Colorado statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "CO" # Set match name
        case "NM": # New Mexico
            nm = _load_nm_baseline()        
            if nm and nm.get("rules"):  # Merge nm rules to merged_rules                
                _merge_rules(merged_rules, nm["rules"]) 
                summary_parts.append("Applied New Mexico statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "NM" # Set match name
        case "ND": # North Dakota
            nd = _load_nd_baseline()        
            if nd and nd.get("rules"):  # Merge nd rules to merged_rules                
                _merge_rules(merged_rules, nd["rules"]) 
                summary_parts.append("Applied North Dakota statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "ND" # Set match name
        case "SD": # South Dakota
            sd = _load_sd_baseline()        
            if sd and sd.get("rules"):  # Merge sd rules to merged_rules        
                _merge_rules(merged_rules, sd["rules"]) 
                summary_parts.append("Applied South Dakota statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "SD" # Set match name      
        case "NE": # Nebraska
            ne = _load_ne_baseline()        
            if ne and ne.get("rules"):  # Merge ne rules to merged_rules            
                _merge_rules(merged_rules, ne["rules"]) 
                summary_parts.append("Applied Nebraska statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "NE" # Set match name
        case "KS": # Kansas
            ks = _load_ks_baseline()        
            if ks and ks.get("rules"):  # Merge ks rules to merged_rules            
                _merge_rules(merged_rules, ks["rules"]) 
                summary_parts.append("Applied Kansas statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "KS" # Set match name
        case "OK": # Oklahoma
            ok = _load_ok_baseline()        
            if ok and ok.get("rules"):  # Merge ok rules to merged_rules        
                _merge_rules(merged_rules, ok["rules"]) 
                summary_parts.append("Applied Oklahoma statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "OK" # Set match name          
        case "AK": # Alaska
            ak = _load_ak_baseline()        
            if ak and ak.get("rules"):  # Merge ak rules to merged_rules    
                _merge_rules(merged_rules, ak["rules"]) 
                summary_parts.append("Applied Alaska statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "AK" # Set match name          
        case "HI": # Hawaii
            hi = _load_hi_baseline()        
            if hi and hi.get("rules"):  # Merge hi rules to merged_rules        
                _merge_rules(merged_rules, hi["rules"]) 
                summary_parts.append("Applied Hawaii statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "HI" # Set match name  
        case "WI": # Wisconsin
            wi = _load_wi_baseline()        
            if wi and wi.get("rules"):  # Merge wi rules to merged_rules        
                _merge_rules(merged_rules, wi["rules"]) 
                summary_parts.append("Applied Wisconsin statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "WI" # Set match name  
        case "MN": # Minnesota
            mn = _load_mn_baseline()        
            if mn and mn.get("rules"):  # Merge mn rules to merged_rules                
                _merge_rules(merged_rules, mn["rules"]) 
                summary_parts.append("Applied Minnesota statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "MN" # Set match name  
        case "IL": # Illinois
            il = _load_il_baseline()        
            if il and il.get("rules"):  # Merge il rules to merged_rules        
                _merge_rules(merged_rules, il["rules"]) 
                summary_parts.append("Applied Illinois statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "IL" # Set match name              

        case "IN": # Indiana    
            ind = _load_in_baseline()        
            if ind and ind.get("rules"):  # Merge in rules to merged_rules        
                _merge_rules(merged_rules, ind["rules"]) 
                summary_parts.append("Applied Indiana statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "IN" # Set match name          
        case "OH": # Ohio    
            oh = _load_oh_baseline()
            if oh and oh.get("rules"):  # Merge oh rules to merged_rules        
                _merge_rules(merged_rules, oh["rules"]) 
                summary_parts.append("Applied Ohio statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "OH" # Set match name                            
        case "IA": # Iowa    
            ia = _load_ia_baseline()        
            if ia and ia.get("rules"):  # Merge ia rules to merged_rules    
                _merge_rules(merged_rules, ia["rules"]) 
                summary_parts.append("Applied Iowa statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "IA" # Set match name      
        case "MO": # Missouri    
            mo = _load_mo_baseline()        
            if mo and mo.get("rules"):  # Merge mo rules to merged_rules        
                _merge_rules(merged_rules, mo["rules"]) 
                summary_parts.append("Applied Missouri statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "MO" # Set match name
        case "MI": # Michigan    
            mi = _load_mi_baseline()        
            if mi and mi.get("rules"):  # Merge mi rules to merged_rules    
                _merge_rules(merged_rules, mi["rules"]) 
                summary_parts.append("Applied Michigan statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "MI" # Set match name      
        
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
