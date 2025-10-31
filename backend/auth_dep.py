# backend/auth_dep.py
# Authorization dependency to verify Firebase ID tokens
from fastapi import HTTPException, Request
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin once uses Json
if not firebase_admin._apps:
    cred = credentials.Certificate("backend/firebase_service_account.json")
    firebase_admin.initialize_app(cred)

async def get_current_user(req: Request):
    auth_header = req.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    id_token = auth_header.split(" ", 1)[1]
    try:
        decoded = auth.verify_id_token(id_token)
        return {"uid": decoded["uid"], "email": decoded.get("email")}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
