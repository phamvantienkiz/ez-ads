"""CORS middleware configuration."""

from typing import Any

from app.core.config import settings


def get_cors_config() -> dict[str, Any]:
    """Return CORS middleware keyword arguments from settings."""
    return {
        "allow_origins": settings.BACKEND_CORS_ORIGINS or ["*"],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
        "expose_headers": ["X-Request-ID", "X-Process-Time"],
    }
