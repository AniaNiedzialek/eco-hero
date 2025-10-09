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
AL_baseline_PATH = DATA_DIR / "state_baselines" / "AL.json"
AR_baseline_PATH = DATA_DIR / "state_baselines" / "AR.json"
FL_baseline_PATH = DATA_DIR / "state_baselines" / "FL.json"
GA_baseline_PATH = DATA_DIR / "state_baselines" / "GA.json"
KY_baseline_PATH = DATA_DIR / "state_baselines" / "KY.json"
LA_baseline_PATH = DATA_DIR / "state_baselines" / "LA.json"
MS_baseline_PATH = DATA_DIR / "state_baselines" / "MS.json"
NC_baseline_PATH = DATA_DIR / "state_baselines" / "NC.json"
SC_baseline_PATH = DATA_DIR / "state_baselines" / "SC.json"
TN_baseline_PATH = DATA_DIR / "state_baselines" / "TN.json"
VA_baseline_PATH = DATA_DIR / "state_baselines" / "VA.json"
WV_baseline_PATH = DATA_DIR / "state_baselines" / "WV.json"
PA_baseline_PATH = DATA_DIR / "state_baselines" / "PA.json"
NY_baseline_PATH = DATA_DIR / "state_baselines" / "NY.json"
NJ_baseline_PATH = DATA_DIR / "state_baselines" / "NJ.json"
CT_baseline_PATH = DATA_DIR / "state_baselines" / "CT.json"
RI_baseline_PATH = DATA_DIR / "state_baselines" / "RI.json"
MA_baseline_PATH = DATA_DIR / "state_baselines" / "MA.json"
VT_baseline_PATH = DATA_DIR / "state_baselines" / "VT.json"
NH_baseline_PATH = DATA_DIR / "state_baselines" / "NH.json"
ME_baseline_PATH = DATA_DIR / "state_baselines" / "ME.json"
MD_baseline_PATH = DATA_DIR / "state_baselines" / "MD.json"
DE_baseline_PATH = DATA_DIR / "state_baselines" / "DE.json"
DC_baseline_PATH = DATA_DIR / "state_baselines" / "DC.json"


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
# for AL
@lru_cache(maxsize=1)
def _load_al_baseline() -> Dict[str, Any]:  
    if not AL_baseline_PATH.exists():
        raise FileNotFoundError(f"AL baseline not found at {AL_baseline_PATH}")
    return json.loads(AL_baseline_PATH.read_text(encoding="utf-8"))     
# for AR
@lru_cache(maxsize=1)
def _load_ar_baseline() -> Dict[str, Any]:
    if not AR_baseline_PATH.exists():
        raise FileNotFoundError(f"AR baseline not found at {AR_baseline_PATH}")
    return json.loads(AR_baseline_PATH.read_text(encoding="utf-8"))     
# for FL
@lru_cache(maxsize=1)
def _load_fl_baseline() -> Dict[str, Any]:  
    if not FL_baseline_PATH.exists():
        raise FileNotFoundError(f"FL baseline not found at {FL_baseline_PATH}")
    return json.loads(FL_baseline_PATH.read_text(encoding="utf-8"))         
# for GA
@lru_cache(maxsize=1)
def _load_ga_baseline() -> Dict[str, Any]:  
    if not GA_baseline_PATH.exists():
        raise FileNotFoundError(f"GA baseline not found at {GA_baseline_PATH}")
    return json.loads(GA_baseline_PATH.read_text(encoding="utf-8"))     
# for KY
@lru_cache(maxsize=1)
def _load_ky_baseline() -> Dict[str, Any]:  
    if not KY_baseline_PATH.exists():
        raise FileNotFoundError(f"KY baseline not found at {KY_baseline_PATH}")
    return json.loads(KY_baseline_PATH.read_text(encoding="utf-8"))     
# for LA
@lru_cache(maxsize=1)               
def _load_la_baseline() -> Dict[str, Any]:          
    if not LA_baseline_PATH.exists():
        raise FileNotFoundError(f"LA baseline not found at {LA_baseline_PATH}")
    return json.loads(LA_baseline_PATH.read_text(encoding="utf-8"))     
# for MS
@lru_cache(maxsize=1)
def _load_ms_baseline() -> Dict[str, Any]:          
    if not MS_baseline_PATH.exists():
        raise FileNotFoundError(f"MS baseline not found at {MS_baseline_PATH}")
    return json.loads(MS_baseline_PATH.read_text(encoding="utf-8"))    
# for NC                
@lru_cache(maxsize=1)
def _load_nc_baseline() -> Dict[str, Any]:          
    if not NC_baseline_PATH.exists():
        raise FileNotFoundError(f"NC baseline not found at {NC_baseline_PATH}")
    return json.loads(NC_baseline_PATH.read_text(encoding="utf-8"))     
# for SC
@lru_cache(maxsize=1)               
def _load_sc_baseline() -> Dict[str, Any]:  
    if not SC_baseline_PATH.exists():
        raise FileNotFoundError(f"SC baseline not found at {SC_baseline_PATH}")
    return json.loads(SC_baseline_PATH.read_text(encoding="utf-8"))
# for TN
@lru_cache(maxsize=1)               
def _load_tn_baseline() -> Dict[str, Any]:  
    if not TN_baseline_PATH.exists():
        raise FileNotFoundError(f"TN baseline not found at {TN_baseline_PATH}")
    return json.loads(TN_baseline_PATH.read_text(encoding="utf-8"))     
# for VA
@lru_cache(maxsize=1)               
def _load_va_baseline() -> Dict[str, Any]:  
    if not VA_baseline_PATH.exists():
        raise FileNotFoundError(f"VA baseline not found at {VA_baseline_PATH}")
    return json.loads(VA_baseline_PATH.read_text(encoding="utf-8"))     
# for WV
@lru_cache(maxsize=1)               
def _load_wv_baseline() -> Dict[str, Any]:  
    if not WV_baseline_PATH.exists():
        raise FileNotFoundError(f"WV baseline not found at {WV_baseline_PATH}")
    return json.loads(WV_baseline_PATH.read_text(encoding="utf-8"))     
# for PA
@lru_cache(maxsize=1)               
def _load_pa_baseline() -> Dict[str, Any]:  
    if not PA_baseline_PATH.exists():
        raise FileNotFoundError(f"PA baseline not found at {PA_baseline_PATH}")
    return json.loads(PA_baseline_PATH.read_text(encoding="utf-8"))
# for NY
@lru_cache(maxsize=1)            
def _load_ny_baseline() -> Dict[str, Any]:  
    if not NY_baseline_PATH.exists():
        raise FileNotFoundError(f"NY baseline not found at {NY_baseline_PATH}")
    return json.loads(NY_baseline_PATH.read_text(encoding="utf-8"))    
# for NJ
@lru_cache(maxsize=1)               
def _load_nj_baseline() -> Dict[str, Any]:  
    if not NJ_baseline_PATH.exists():
        raise FileNotFoundError(f"NJ baseline not found at {NJ_baseline_PATH}")
    return json.loads(NJ_baseline_PATH.read_text(encoding="utf-8"))     
# for CT
@lru_cache(maxsize=1)               
def _load_ct_baseline() -> Dict[str, Any]:  
    if not CT_baseline_PATH.exists():
        raise FileNotFoundError(f"CT baseline not found at {CT_baseline_PATH}")
    return json.loads(CT_baseline_PATH.read_text(encoding="utf-8"))     
# for RI
@lru_cache(maxsize=1)               
def _load_ri_baseline() -> Dict[str, Any]:          
    if not RI_baseline_PATH.exists():
        raise FileNotFoundError(f"RI baseline not found at {RI_baseline_PATH}")
    return json.loads(RI_baseline_PATH.read_text(encoding="utf-8"))    
# for MA
@lru_cache(maxsize=1)               
def _load_ma_baseline() -> Dict[str, Any]:          
    if not MA_baseline_PATH.exists():
        raise FileNotFoundError(f"MA baseline not found at {MA_baseline_PATH}")
    return json.loads(MA_baseline_PATH.read_text(encoding="utf-8"))     
# for VT
@lru_cache(maxsize=1)               
def _load_vt_baseline() -> Dict[str, Any]:  
    if not VT_baseline_PATH.exists():
        raise FileNotFoundError(f"VT baseline not found at {VT_baseline_PATH}")
    return json.loads(VT_baseline_PATH.read_text(encoding="utf-8"))    
# for NH
@lru_cache(maxsize=1)               
def _load_nh_baseline() -> Dict[str, Any]:  
    if not NH_baseline_PATH.exists():
        raise FileNotFoundError(f"NH baseline not found at {NH_baseline_PATH}")
    return json.loads(NH_baseline_PATH.read_text(encoding="utf-8"))
# for ME
@lru_cache(maxsize=1)               
def _load_me_baseline() -> Dict[str, Any]:              
    if not ME_baseline_PATH.exists():
        raise FileNotFoundError(f"ME baseline not found at {ME_baseline_PATH}")
    return json.loads(ME_baseline_PATH.read_text(encoding="utf-8"))     
# for MD
@lru_cache(maxsize=1)               
def _load_md_baseline() -> Dict[str, Any]:  
    if not MD_baseline_PATH.exists():
        raise FileNotFoundError(f"MD baseline not found at {MD_baseline_PATH}")
    return json.loads(MD_baseline_PATH.read_text(encoding="utf-8"))     
# for DE
@lru_cache(maxsize=1)               
def _load_de_baseline() -> Dict[str, Any]:  
    if not DE_baseline_PATH.exists():
        raise FileNotFoundError(f"DE baseline not found at {DE_baseline_PATH}")
    return json.loads(DE_baseline_PATH.read_text(encoding="utf-8"))     
# for DC
@lru_cache(maxsize=1)               
def _load_dc_baseline() -> Dict[str, Any]:  
    if not DC_baseline_PATH.exists():
        raise FileNotFoundError(f"DC baseline not found at {DC_baseline_PATH}")
    return json.loads(DC_baseline_PATH.read_text(encoding="utf-8"))     


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
        case "AL": # Alabama    
            al = _load_al_baseline()        
            if al and al.get("rules"):  # Merge al rules to merged_rules        
                _merge_rules(merged_rules, al["rules"]) 
                summary_parts.append("Applied Alabama statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "AL" # Set match name      
        case "AR": # Arkansas    
            ar = _load_ar_baseline()        
            if ar and ar.get("rules"):  # Merge ar rules to merged_rules    
                _merge_rules(merged_rules, ar["rules"]) 
                summary_parts.append("Applied Arkansas statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "AR" # Set match name
        case "FL": # Florida    
            fl = _load_fl_baseline()        
            if fl and fl.get("rules"):  # Merge fl rules to merged_rules    
                _merge_rules(merged_rules, fl["rules"]) 
                summary_parts.append("Applied Florida statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "FL" # Set match name      
        case "GA": # Georgia    
            ga = _load_ga_baseline()
            if ga and ga.get("rules"):  # Merge ga rules to merged_rules        
                _merge_rules(merged_rules, ga["rules"]) 
                summary_parts.append("Applied Georgia statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "GA" # Set match name    
        case "KY": # Kentucky   
            ky = _load_ky_baseline()        
            if ky and ky.get("rules"):  # Merge ky rules to merged_rules    
                _merge_rules(merged_rules, ky["rules"]) 
                summary_parts.append("Applied Kentucky statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "KY" # Set match name
        case "LA": # Louisiana
            la = _load_la_baseline()        
            if la and la.get("rules"):  # Merge la rules to merged_rules    
                _merge_rules(merged_rules, la["rules"]) 
                summary_parts.append("Applied Louisiana statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "LA" # Set match name
        case "MS": # Mississippi
            ms = _load_ms_baseline()        
            if ms and ms.get("rules"):  # Merge ms rules to merged_rules
                _merge_rules(merged_rules, ms["rules"]) 
                summary_parts.append("Applied Mississippi statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "MS" # Set match name
        case "NC": # North Carolina
            nc = _load_nc_baseline()

            if nc and nc.get("rules"):  # Merge nc rules to merged_rules    
                _merge_rules(merged_rules, nc["rules"]) 
                summary_parts.append("Applied North Carolina statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "NC" # Set match name
        case "SC": # South Carolina
            sc = _load_sc_baseline()        
            if sc and sc.get("rules"):  # Merge sc rules to merged_rules    
                _merge_rules(merged_rules, sc["rules"]) 
                summary_parts.append("Applied South Carolina statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "SC" # Set match name
        case "TN": # Tennessee
            tn = _load_tn_baseline()        
            if tn and tn.get("rules"):  # Merge tn rules to merged_rules        
                _merge_rules(merged_rules, tn["rules"]) 
                summary_parts.append("Applied Tennessee statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "TN" # Set match name
        case "VA": # Virginia   
            va = _load_va_baseline()        
            if va and va.get("rules"):  # Merge va rules to merged_rules    
                _merge_rules(merged_rules, va["rules"]) 
                summary_parts.append("Applied Virginia statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "VA" # Set match name
        case "WV": # West Virginia
            wv = _load_wv_baseline()        
            if wv and wv.get("rules"):  # Merge wv rules to merged  
                _merge_rules(merged_rules, wv["rules"]) 
                summary_parts.append("Applied West Virginia statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "WV" # Set match name
        case "PA": # Pennsylvania
            pa = _load_pa_baseline()        
            if pa and pa.get("rules"):  # Merge pa rules to merged_rules    
                _merge_rules(merged_rules, pa["rules"]) 
                summary_parts.append("Applied Pennsylvania statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "PA" # Set match name  
        case "NY": # New York
            ny = _load_ny_baseline()        
            if ny and ny.get("rules"):  # Merge ny rules to merged_rules        
                _merge_rules(merged_rules, ny["rules"]) 
                summary_parts.append("Applied New York statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "NY" # Set match name
        case "NJ": # New Jersey
            nj = _load_nj_baseline()        
            if nj and nj.get("rules"):  # Merge nj rules to merged_rules    
                _merge_rules(merged_rules, nj["rules"]) 
                summary_parts.append("Applied New Jersey statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "NJ" # Set match name
        case "CT": # Connecticut
            ct = _load_ct_baseline()        
            if ct and ct.get("rules"):  # Merge ct rules to merged_rules    
                _merge_rules(merged_rules, ct["rules"]) 
                summary_parts.append("Applied Connecticut statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "CT" # Set match name      
        case "RI": # Rhode Island   
            ri = _load_ri_baseline()        
            if ri and ri.get("rules"):  # Merge ri rules to merged_rules    
                _merge_rules(merged_rules, ri["rules"]) 
                summary_parts.append("Applied Rhode Island statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "RI" # Set match name  
        case "MA": # Massachusetts
            ma = _load_ma_baseline()        
            if ma and ma.get("rules"):  # Merge ma rules to merged_rules        
                _merge_rules(merged_rules, ma["rules"]) 
                summary_parts.append("Applied Massachusetts statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "MA" # Set match name      
        case "VT": # Vermont
            vt = _load_vt_baseline()        
            if vt and vt.get("rules"):  # Merge vt rules to merged_rules            
                _merge_rules(merged_rules, vt["rules"]) 
                summary_parts.append("Applied Vermont statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "VT" # Set match name    
        case "NH": # New Hampshire      
            nh = _load_nh_baseline()        
            if nh and nh.get("rules"):  # Merge nh rules to merged_rules        
                _merge_rules(merged_rules, nh["rules"]) 
                summary_parts.append("Applied New Hampshire statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "NH" # Set match name      
        case "ME": # Maine
            me = _load_me_baseline()        
            if me and me.get("rules"):  # Merge me rules to merged_rules        
                _merge_rules(merged_rules, me["rules"]) 
                summary_parts.append("Applied Maine statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "ME" # Set match name      
        case "MD": # Maryland       
            md = _load_md_baseline()        
            if md and md.get("rules"):  # Merge md rules to merged_rules        
                _merge_rules(merged_rules, md["rules"]) 
                summary_parts.append("Applied Maryland statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "MD" # Set match name  
        case "DE": # Delaware
            de = _load_de_baseline()        
            if de and de.get("rules"):  # Merge de rules to merged_rules        
                _merge_rules(merged_rules, de["rules"]) 
                summary_parts.append("Applied Delaware statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "DE" # Set match name  
        case "DC": # District of Columbia
            dc = _load_dc_baseline()        
            if dc and dc.get("rules"):  # Merge dc rules to merged_rules    
                _merge_rules(merged_rules, dc["rules"]) 
                summary_parts.append("Applied District of Columbia statewide baseline.") # Add to summary
                match_level = "state" # Set match level
                match_name = "DC" # Set match name      

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
