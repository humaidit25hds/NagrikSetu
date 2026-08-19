
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the sender: 'user', 'assistant', or 'system'")
    content: str = Field(..., description="Message text content")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)


class UserDemographics(BaseModel):
    age: Optional[int] = Field(None, description="Age in years")
    gender: Optional[str] = Field(None, description="Male / Female / Other")
    state: Optional[str] = Field(None, description="Indian State / UT")
    district: Optional[str] = Field(None, description="District name")
    annual_income: Optional[float] = Field(None, description="Annual household income in INR")
    occupation: Optional[str] = Field(None, description="Farmer, Student, Artisan, Small Business, etc.")
    category: Optional[str] = Field(None, description="General / OBC / SC / ST / EWS")
    is_differently_abled: Optional[str] = Field("No", description="Yes / No")
    land_holding_acres: Optional[float] = Field(0.0, description="Cultivable land in acres")


class SchemeCard(BaseModel):
    id: Optional[int] = None
    title: str
    title_hi: Optional[str] = None
    department: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = "Central"
    state: Optional[str] = None
    benefits: Optional[str] = None
    eligibility_summary: Optional[str] = None
    application_url: Optional[str] = None
    helpline: Optional[str] = None
    match_score: Optional[float] = 1.0


class SourceDocument(BaseModel):
    title: str
    url: Optional[str] = None
    snippet: str
    relevance_score: Optional[float] = 1.0


class ChatRequest(BaseModel):
    message: str = Field(..., description="User query / citizen prompt")
    conversation_history: Optional[List[ChatMessage]] = Field(default_factory=list)
    user_profile: Optional[UserDemographics] = None
    language: Optional[str] = Field(default="en", description="Response language: 'en' (English), 'hi' (Hindi), 'hinglish'")


class ChatResponse(BaseModel):
    response: str = Field(..., description="AI civic assistant markdown answer")
    language: str = "en"
    recommended_schemes: List[SchemeCard] = Field(default_factory=list)
    source_documents: List[SourceDocument] = Field(default_factory=list)
    suggested_followups: List[str] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


# Eligibility Schemas
class EligibilityCriteriaItem(BaseModel):
    criterion: str
    met: bool
    reason: str


class EligibilityCheckRequest(BaseModel):
    scheme_id: Optional[int] = None
    scheme_name: Optional[str] = None
    demographics: UserDemographics


class EligibilityResult(BaseModel):
    scheme_id: Optional[int] = None
    scheme_title: str
    status: str = Field(..., description="'ELIGIBLE', 'LIKELY_ELIGIBLE', 'INELIGIBLE', 'NEED_MORE_INFO'")
    match_score_percent: int
    matched_criteria: List[EligibilityCriteriaItem] = Field(default_factory=list)
    unmet_criteria: List[EligibilityCriteriaItem] = Field(default_factory=list)
    required_documents: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)
    application_url: Optional[str] = None


# Service Schemas
class ServiceResponse(BaseModel):
    id: int
    title: str
    title_hi: Optional[str] = None
    short_description: str
    detailed_description: Optional[str] = None
    department: str
    category: str
    level: str
    state: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    benefits: Optional[str] = None
    required_documents: Optional[str] = None
    application_process: Optional[str] = None
    application_url: Optional[str] = None
    helpline: Optional[str] = None
    is_active: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Application Tracking Schemas
class ApplicationCreateRequest(BaseModel):
    service_id: int
    applicant_name: str
    applicant_phone: str
    applicant_email: Optional[str] = None
    applicant_aadhaar_last4: Optional[str] = None
    user_demographics: Optional[UserDemographics] = None
    documents_submitted: Optional[List[str]] = Field(default_factory=list)
    remarks: Optional[str] = None


class ApplicationResponse(BaseModel):
    id: int
    tracking_number: str
    service_id: int
    service_title: Optional[str] = None
    applicant_name: Optional[str] = None
    applicant_phone: Optional[str] = None
    status: str
    remarks: Optional[str] = None
    documents_submitted: Optional[str] = None
    submitted_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
