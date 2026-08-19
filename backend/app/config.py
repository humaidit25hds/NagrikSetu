import os
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


class Settings:
    """
    Application configuration settings.
    """

    # Application
    APP_NAME: str = os.getenv(
        "APP_NAME",
        "Citizen-AI"
    )

    APP_VERSION: str = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )

    DEBUG: bool = os.getenv(
        "DEBUG",
        "False"
    ).lower() == "true"

    # OpenAI
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
        "sqlite:///./citizen_ai.db"
    )

    # API
    API_PREFIX: str = os.getenv(
        "API_PREFIX",
        "/api"
    )

    # CORS
    FRONTEND_URL: str = os.getenv(
        "FRONTEND_URL",
        "http://localhost:3000"
    )


settings = Settings()
