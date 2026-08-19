import os
from typing import List
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


class Settings:
    """
    Application configuration settings for NagrikSetu.
    """

    # Application
    APP_NAME: str = os.getenv(
        "APP_NAME",
        "NagrikSetu"
    )

    APP_VERSION: str = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )

    APP_ENV: str = os.getenv(
        "APP_ENV",
        "development"
    )

    DEBUG: bool = os.getenv(
        "DEBUG",
        "False"
    ).lower() == "true"

    # Server
    HOST: str = os.getenv(
        "HOST",
        "0.0.0.0"
    )

    PORT: int = int(os.getenv(
        "PORT",
        "8000"
    ))

    # AI provider
    GEMINI_API_KEY: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    )

    DEFAULT_MODEL: str = os.getenv(
        "DEFAULT_MODEL",
        "gemini-3.6-flash"
    )

    OPENAI_API_KEY: str = os.getenv(
        "OPENAI_API_KEY",
        ""
    )

    OPENAI_MODEL: str = os.getenv(
        "OPENAI_MODEL",
        "gpt-4o-mini"
    )

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./nagriksetu.db"
    )

    # MongoDB (secondary document database)
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "NagrikSetu")
    MONGODB_TIMEOUT_MS: int = int(os.getenv("MONGODB_TIMEOUT_MS", "5000"))

    # API
    API_PREFIX: str = os.getenv(
        "API_PREFIX",
        "/api"
    )

    API_V1_STR: str = os.getenv(
        "API_V1_STR",
        "/api/v1"
    )

    # CORS & Security
    ALLOWED_ORIGINS: List[str] = [
        origin.strip() for origin in os.getenv(
            "ALLOWED_ORIGINS",
            "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000"
        ).split(",")
    ]

    FRONTEND_URL: str = os.getenv(
        "FRONTEND_URL",
        "http://localhost:3000"
    )


def get_settings() -> Settings:
    """Get application settings singleton"""
    return Settings()


settings = get_settings()
