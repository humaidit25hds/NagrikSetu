
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    title_hi = Column(String(255), nullable=True)  # Hindi representation
    short_description = Column(String(500), nullable=False)
    detailed_description = Column(Text, nullable=True)
    
    # Classification
    department = Column(String(200), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)  # Agriculture, Healthcare, Education, Housing, Social Welfare, Business
    level = Column(String(50), default="Central", index=True)   # Central / State / Municipal
    state = Column(String(100), nullable=True, index=True)      # Applicable state if State level
    
    # Eligibility & Process Specifications (JSON or Markdown formatted text)
    eligibility_criteria = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)
    required_documents = Column(Text, nullable=True)
    application_process = Column(Text, nullable=True)
    
    # Links & Support
    application_url = Column(String(500), nullable=True)
    helpline = Column(String(100), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    applications = relationship("Application", back_populates="service")