"""
Core Configuration Module
Contains application-wide settings and configuration
"""

import json
from functools import lru_cache
from typing import Optional, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_str_list(value: Union[str, list]) -> list[str]:
    """Parse list settings from JSON, comma-separated strings, or lists."""
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []
        if text.startswith("["):
            parsed = json.loads(text)
            return [str(item).strip() for item in parsed if str(item).strip()]
        return [item.strip() for item in text.split(",") if item.strip()]
    return value


class Settings(BaseSettings):
    """
    Application Settings
    Loads configuration from environment variables with defaults
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # Application
    APP_NAME: str = "Personal AI Agent Backend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://13.233.184.74",
        "http://localhost:8080",
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # Environment
    ENVIRONMENT: str = "development"

    # Google Gemini Configuration
    GEMINI_API_KEY: Optional[str] = None
    # Using gemini-3-flash-preview (same as Google AI Studio)
    GEMINI_MODEL: str = "gemini-3-flash-preview"

    @field_validator(
        "CORS_ORIGINS",
        "CORS_ALLOW_METHODS",
        "CORS_ALLOW_HEADERS",
        mode="before",
    )
    @classmethod
    def parse_cors_lists(cls, value: Union[str, list]) -> list[str]:
        return _parse_str_list(value)


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached)
    Cache ensures settings are loaded only once
    """
    return Settings()
