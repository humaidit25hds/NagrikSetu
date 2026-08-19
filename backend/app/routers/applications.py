import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.service import Service
from app.models.application import Application
from app.schemas.chat import ApplicationCreateRequest, ApplicationResponse

router = APIRouter(prefix="/applications", tags=["Citizen Applications & Tracking"])


@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED, summary="Submit a scheme application")
def submit_application(
    request: ApplicationCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Submits a new civic scheme application on behalf of the citizen and issues
    a unique NagrikSetu tracking ID (e.g., NS-2026-AB12C).
    """
    # 1. Find or create user
    user = db.query(User).filter(User.phone_number == request.applicant_phone).first()
    if not user:
        user = User(
            full_name=request.applicant_name,
            phone_number=request.applicant_phone,
            email=request.applicant_email,
            age=request.user_demographics.age if request.user_demographics else None,
            gender=request.user_demographics.gender if request.user_demographics else None,
            state=request.user_demographics.state if request.user_demographics else None,
            district=request.user_demographics.district if request.user_demographics else None,
            annual_income=request.user_demographics.annual_income if request.user_demographics else None,
            occupation=request.user_demographics.occupation if request.user_demographics else None,
            category=request.user_demographics.category if request.user_demographics else None,
            land_holding_acres=request.user_demographics.land_holding_acres if request.user_demographics else 0.0,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # 2. Check if scheme exists in DB, or auto-seed if needed
    service = db.query(Service).filter(Service.id == request.service_id).first()
    if not service:
        # Create a stub service record if seeded ID is referenced
        service = Service(
            id=request.service_id,
            title=f"Scheme #{request.service_id}",
            short_description="Government Welfare Scheme",
            department="Government Department",
            category="Civic Welfare"
        )
        db.add(service)
        db.commit()
        db.refresh(service)

    # 3. Generate unique tracking reference number
    unique_suffix = uuid.uuid4().hex[:6].upper()
    tracking_no = f"NS-2026-{unique_suffix}"

    docs_str = ", ".join(request.documents_submitted) if request.documents_submitted else "Aadhaar Card, Bank Details"

    application = Application(
        tracking_number=tracking_no,
        user_id=user.id,
        service_id=service.id,
        applicant_name=request.applicant_name,
        applicant_phone=request.applicant_phone,
        applicant_aadhaar_last4=request.applicant_aadhaar_last4,
        documents_submitted=docs_str,
        status="SUBMITTED",
        remarks="Application received successfully. Awaiting initial document verification.",
    )
    db.add(application)
    db.commit()
    db.refresh(application)

    return ApplicationResponse(
        id=application.id,
        tracking_number=application.tracking_number,
        service_id=service.id,
        service_title=service.title,
        applicant_name=application.applicant_name,
        applicant_phone=application.applicant_phone,
        status=application.status,
        remarks=application.remarks,
        documents_submitted=application.documents_submitted,
        submitted_at=application.submitted_at,
        updated_at=application.updated_at,
    )


@router.get("/track/{tracking_number}", response_model=ApplicationResponse, summary="Track application status by tracking number")
def track_application(tracking_number: str, db: Session = Depends(get_db)):
    """
    Retrieves real-time status, timeline, and remarks for a given NagrikSetu application tracking number.
    """
    app_record = db.query(Application).filter(Application.tracking_number == tracking_number.strip().upper()).first()
    if not app_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application with tracking number '{tracking_number}' was not found. Please check and re-enter."
        )

    service_title = app_record.service.title if app_record.service else "Government Scheme"

    return ApplicationResponse(
        id=app_record.id,
        tracking_number=app_record.tracking_number,
        service_id=app_record.service_id,
        service_title=service_title,
        applicant_name=app_record.applicant_name,
        applicant_phone=app_record.applicant_phone,
        status=app_record.status,
        remarks=app_record.remarks,
        documents_submitted=app_record.documents_submitted,
        submitted_at=app_record.submitted_at,
        updated_at=app_record.updated_at,
    )


@router.get("/user/{phone_number}", response_model=List[ApplicationResponse], summary="Get all applications for a citizen")
def get_user_applications(phone_number: str, db: Session = Depends(get_db)):
    """
    Returns all scheme applications submitted by a citizen using their mobile number.
    """
    user = db.query(User).filter(User.phone_number == phone_number.strip()).first()
    if not user:
        return []

    applications = db.query(Application).filter(Application.user_id == user.id).all()
    results = []
    for app in applications:
        results.append(
            ApplicationResponse(
                id=app.id,
                tracking_number=app.tracking_number,
                service_id=app.service_id,
                service_title=app.service.title if app.service else None,
                applicant_name=app.applicant_name,
                applicant_phone=app.applicant_phone,
                status=app.status,
                remarks=app.remarks,
                documents_submitted=app.documents_submitted,
                submitted_at=app.submitted_at,
                updated_at=app.updated_at,
            )
        )
    return results
