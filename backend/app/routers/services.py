from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.service import Service
from app.schemas.chat import ServiceResponse
from app.services.rag import INDIAN_SCHEMES_KNOWLEDGE

router = APIRouter(prefix="/services", tags=["Government Schemes & Services"])


@router.get("", response_model=List[ServiceResponse], summary="List and search government schemes")
def list_services(
    category: Optional[str] = Query(None, description="Filter by category (e.g. Agriculture, Healthcare, Education, Housing)"),
    department: Optional[str] = Query(None, description="Filter by ministry/department"),
    level: Optional[str] = Query(None, description="Filter by level: Central or State"),
    state: Optional[str] = Query(None, description="Filter by state name"),
    search: Optional[str] = Query(None, description="Keyword search in title and description"),
    db: Session = Depends(get_db)
):
    """
    Search and filter through Indian Central and State Government schemes.
    """
    query = db.query(Service).filter(Service.is_active == True)

    if category:
        query = query.filter(Service.category.ilike(f"%{category}%"))
    if department:
        query = query.filter(Service.department.ilike(f"%{department}%"))
    if level:
        query = query.filter(Service.level.ilike(f"%{level}%"))
    if state and state.lower() != "all india":
        query = query.filter((Service.state == state) | (Service.state == "All India") | (Service.level == "Central"))
    if search:
        query = query.filter(
            (Service.title.ilike(f"%{search}%")) |
            (Service.short_description.ilike(f"%{search}%")) |
            (Service.category.ilike(f"%{search}%"))
        )

    services = query.all()

    # Fallback to the knowledge base when the database has no matching records.
    if not services and (search or not category):
        search_term = (search or "").lower().strip()
        fallback_schemes = [
            scheme for scheme in INDIAN_SCHEMES_KNOWLEDGE
            if not search_term or search_term in " ".join(
                str(value).lower() for value in scheme.values()
            )
        ]
        return [
            ServiceResponse(
                id=s["id"],
                title=s["title"],
                title_hi=s.get("title_hi"),
                short_description=s.get("benefits", "")[:150],
                detailed_description=s.get("benefits"),
                department=s.get("department", "Government of India"),
                category=s.get("category", "Civic Services"),
                level=s.get("level", "Central"),
                state=s.get("state", "All India"),
                eligibility_criteria=s.get("eligibility_criteria"),
                benefits=s.get("benefits"),
                required_documents=s.get("required_documents"),
                application_process=s.get("application_process"),
                application_url=s.get("application_url"),
                helpline=s.get("helpline"),
                is_active=True,
                created_at=None
            ) for s in fallback_schemes
        ]

    return services


@router.get("/categories/all", summary="Get all available categories and departments")
def get_categories_and_departments(db: Session = Depends(get_db)):
    """
    Returns lists of available categories and ministries for easy UI filtering.
    """
    categories = [
        "Agriculture",
        "Healthcare",
        "Housing",
        "Financial Services & Business",
        "Education",
        "Women & Child",
        "Employment & Skill",
        "Social Welfare & Pension"
    ]
    levels = ["Central", "State"]
    return {
        "categories": categories,
        "levels": levels,
        "total_schemes_registered": db.query(Service).count()
    }


@router.get("/{service_id}", response_model=ServiceResponse, summary="Get full details of a specific scheme")
def get_service_detail(service_id: int, db: Session = Depends(get_db)):
    """
    Retrieves full details of a specific scheme including benefits,
    eligibility criteria, required documents, application process, and official links.
    """
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        # Check seeds
        for s in INDIAN_SCHEMES_KNOWLEDGE:
            if s["id"] == service_id:
                return ServiceResponse(
                    id=s["id"],
                    title=s["title"],
                    title_hi=s.get("title_hi"),
                    short_description=s.get("benefits", "")[:150],
                    detailed_description=s.get("benefits"),
                    department=s.get("department", "Government of India"),
                    category=s.get("category", "Civic Services"),
                    level=s.get("level", "Central"),
                    state=s.get("state", "All India"),
                    eligibility_criteria=s.get("eligibility_criteria"),
                    benefits=s.get("benefits"),
                    required_documents=s.get("required_documents"),
                    application_process=s.get("application_process"),
                    application_url=s.get("application_url"),
                    helpline=s.get("helpline"),
                    is_active=True,
                    created_at=None
                )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scheme with ID {service_id} not found."
        )

    return service

