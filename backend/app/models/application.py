from datetime import datetime
# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import relationship

from app.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(50), unique=True, index=True, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    
    # Status lifecycle: DRAFT, SUBMITTED, IN_REVIEW, APPROVED, REJECTED, ACTION_REQUIRED
    status = Column(String(50), default="SUBMITTED", nullable=False, index=True)
    applicant_name = Column(String(255), nullable=True)
    applicant_phone = Column(String(20), nullable=True)
    applicant_aadhaar_last4 = Column(String(4), nullable=True)
    
    documents_submitted = Column(Text, nullable=True)  # JSON or comma-separated document names
    remarks = Column(Text, nullable=True)
    acknowledgement_receipt = Column(String(255), nullable=True)

    submitted_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="applications")
    service = relationship("Service", back_populates="applications")
