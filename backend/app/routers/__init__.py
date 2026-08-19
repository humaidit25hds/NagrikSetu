"""API routers for NagrikSetu"""
from app.routers.chat import router as chat_router
from app.routers.services import router as services_router
from app.routers.applications import router as applications_router

__all__ = ["chat_router", "services_router", "applications_router"]
