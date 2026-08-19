from contextlib import asynccontextmanager
# pyrefly: ignore [missing-import]
import uvicorn
# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from starlette.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import engine, Base, SessionLocal
from app.models.service import Service
from app.routers.chat import router as chat_router
from app.routers.services import router as services_router
from app.routers.applications import router as applications_router
from app.services.rag import INDIAN_SCHEMES_KNOWLEDGE

settings = get_settings()


def seed_database():
    """
    Seeds initial Indian Government Schemes into the database if not already populated.
    """
    db = SessionLocal()
    try:
        count = db.query(Service).count()
        if count == 0:
            for s in INDIAN_SCHEMES_KNOWLEDGE:
                service = Service(
                    id=s["id"],
                    title=s["title"],
                    title_hi=s.get("title_hi"),
                    short_description=s.get("benefits", "")[:200],
                    detailed_description=f"{s.get('benefits')}\n\nEligibility:\n{s.get('eligibility_criteria')}",
                    department=s["department"],
                    category=s["category"],
                    level=s.get("level", "Central"),
                    state=s.get("state", "All India"),
                    eligibility_criteria=s.get("eligibility_criteria"),
                    benefits=s.get("benefits"),
                    required_documents=s.get("required_documents"),
                    application_process=s.get("application_process"),
                    application_url=s.get("application_url"),
                    helpline=s.get("helpline"),
                    is_active=True,
                )
                db.add(service)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"Warning: Error seeding initial schemes: {e}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables
    Base.metadata.create_all(bind=engine)
    # Seed initial civic knowledge
    seed_database()
    yield


app = FastAPI(
    title=f"{settings.APP_NAME} - Indian Civic & Government Services AI Platform",
    description="AI-powered civic assistant connecting Indian citizens with Government Schemes (Sarkari Yojana), eligibility checks, document guidance, and application tracking.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS if isinstance(settings.ALLOWED_ORIGINS, list) else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers under /api/v1 prefix
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(services_router, prefix=settings.API_V1_STR)
app.include_router(applications_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Health & Status"])
def root():
    return {
        "app": settings.APP_NAME,
        "tagline": "Empowering Citizens with AI for Indian Government Services (नागरिक सेतु)",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "chat": f"{settings.API_V1_STR}/chat",
            "eligibility": f"{settings.API_V1_STR}/chat/eligibility",
            "services": f"{settings.API_V1_STR}/services",
            "applications": f"{settings.API_V1_STR}/applications",
        }
    }


@app.get("/health", tags=["Health & Status"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database": "connected"
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)