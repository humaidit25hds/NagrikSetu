# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, status
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    EligibilityCheckRequest,
    EligibilityResult,
)
from app.services.rag import RAGService
from app.services.eligibility import EligibilityService
from app.services.ai import AIService

router = APIRouter(prefix="/chat", tags=["Civic AI Chatbot"])


@router.post("", response_model=ChatResponse, summary="Send message to NagrikSetu AI Civic Assistant")
async def chat_with_assistant(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Main conversational endpoint for citizens to inquire about Indian government schemes,
    eligibility criteria, required documents, and step-by-step application guidance.
    """
    try:
        rag_service = RAGService(db=db)
        eligibility_service = EligibilityService(db=db)
        ai_service = AIService(rag_service=rag_service, eligibility_service=eligibility_service)

        response = await ai_service.generate_chat_response(
            message=request.message,
            conversation_history=request.conversation_history,
            user_profile=request.user_profile,
            language=request.language or "en"
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your civic request: {str(e)}"
        )


@router.post("/eligibility", response_model=EligibilityResult, summary="Check eligibility for a scheme")
def check_scheme_eligibility(
    request: EligibilityCheckRequest,
    db: Session = Depends(get_db)
):
    """
    Evaluates citizen demographic profile against specific government scheme rules
    and returns matched criteria, unmet criteria, document checklist, and application roadmap.
    """
    eligibility_service = EligibilityService(db=db)
    result = eligibility_service.evaluate(
        scheme_id=request.scheme_id,
        scheme_name=request.scheme_name,
        demographics=request.demographics
    )
    return result