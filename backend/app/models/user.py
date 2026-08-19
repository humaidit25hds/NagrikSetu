
from datetime import datetime
# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, Float, DateTime
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=True)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    
    # Citizen Profile for Scheme Eligibility Matching
    age = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)  # Male, Female, Other
    state = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    annual_income = Column(Float, nullable=True)  # in INR
    occupation = Column(String(100), nullable=True)  # Farmer, Student, Artisan, Self-Employed, Unemployed, etc.
    category = Column(String(100), nullable=True)  # General, OBC, SC, ST, EWS
    is_differently_abled = Column(String(10), default="No")  # Yes, No
    land_holding_acres = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")
