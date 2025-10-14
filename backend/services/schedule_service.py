from repositories import schedule_repository
from database.db import SessionLocal
import json

def get_schedule_by_address_and_zip(address: str, zip_code: str):
    db = SessionLocal()
    try:
        result = schedule_repository.get_by_address_and_zip(db, address, zip_code)
        return result
    finally:
        db.close()

def add_schedule(data: dict):
    db = SessionLocal()
    try:
        return schedule_repository.create_schedule(db, data)
    finally:
        db.close()