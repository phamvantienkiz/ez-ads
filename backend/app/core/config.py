"""Application configuration using Pydantic Settings."""


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings read from environment variables or .env file."""

    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Database
    DATABASE_PATH: str = "baha_ads_manager.db"

    # Meta Marketing API Credentials (v20.0)
    META_APP_ID: str = ""
    META_APP_SECRET: str = ""
    META_REDIRECT_URI: str = "http://localhost:8000/api/meta/callback"
    META_API_VERSION: str = "v20.0"
    META_GRAPH_BASE_URL: str = "https://graph.facebook.com/v20.0"
    META_OAUTH_BASE_URL: str = "https://www.facebook.com/v20.0/dialog/oauth"
    META_API_TIMEOUT: float = 30.0

    # Frontend URL for OAuth redirects
    FRONTEND_URL: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
