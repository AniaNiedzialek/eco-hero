from sqlalchemy.orm import Session
from database.models import Schedule
from sqlalchemy.orm import Session
from database.models import Schedule
from sqlalchemy.exc import SQLAlchemyError

def get_by_address_and_zip(db: Session, address: str, zip_code: str):
    try:
        return db.query(Schedule).filter(Schedule.address == address, Schedule.zip_code == zip_code).first()
    except SQLAlchemyError:
        return None

def create_schedule(db: Session, data: dict):
    new_schedule = Schedule(
        address=data.get("address"),
        city=data.get("city"),
        state=data.get("state"),
        zip_code=data.get("zip_code"),
        schedule=data.get("schedule"),
    )
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule