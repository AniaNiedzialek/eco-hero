"""
Run this file to initialize the database or to add new tables
"""
from database import Base, engine
from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# -------- Database --------
DATABASE_URL = "sqlite:///./backend/database.db"

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -------- Models --------
class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    schedule = Column(JSON)
    created_at = Column(DateTime, default=func.now())

# -------- Initialize --------
def init_db():
    Base.metadata.create_all(bind=engine, checkfirst=True)
    print("Database initialized")

if __name__ == "__main__":
    init_db()