from typing import Any, Optional

from pymongo import MongoClient
from pymongo.database import Database

from app.config import get_settings

settings = get_settings()

_client: Optional[MongoClient[Any]] = None


def get_mongo_client() -> Optional[MongoClient[Any]]:
    """Return the shared MongoDB client when MongoDB is configured."""
    global _client
    if not settings.MONGODB_URI:
        return None
    if _client is None:
        _client = MongoClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=settings.MONGODB_TIMEOUT_MS,
            connectTimeoutMS=settings.MONGODB_TIMEOUT_MS,
        )
    return _client


def get_mongo_database() -> Optional[Database[Any]]:
    """Return the configured MongoDB database handle."""
    client = get_mongo_client()
    return client[settings.MONGODB_DB_NAME] if client else None


def check_mongo_connection() -> dict[str, Any]:
    """Ping MongoDB without exposing connection details."""
    client = get_mongo_client()
    if client is None:
        return {"configured": False, "status": "not_configured"}

    try:
        client.admin.command("ping")
        return {
            "configured": True,
            "status": "connected",
            "database": settings.MONGODB_DB_NAME,
        }
    except Exception as error:
        return {
            "configured": True,
            "status": "unavailable",
            "error": type(error).__name__,
        }
