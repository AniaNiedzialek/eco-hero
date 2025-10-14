from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from database.db import Base

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    schedule = Column(JSON)
    created_at = Column(DateTime, default=func.now())