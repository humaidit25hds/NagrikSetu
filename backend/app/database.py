from typing import Generator
# pyrefly: ignore [missing-import]
from sqlalchemy import create_engine, text
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import get_settings

settings = get_settings()

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def check_database_connection() -> str:
    """Return the real database connectivity status."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return "connected"
    except Exception:
        return "disconnected"


def get_db() -> Generator:
    """
    FastAPI dependency yielding a database session per request.
    Automatically closes session after completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
