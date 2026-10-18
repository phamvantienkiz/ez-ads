"""Meta OAuth 2.0 authentication and session lifecycle service."""

import urllib.parse
from typing import Any

from app.core.config import settings
from app.core.security import state_manager
from app.repositories.session_repository import SessionRepository, session_repo
from app.services.meta_client import MetaClientService, meta_client

REQUIRED_SCOPES = [
    "ads_management",
    "ads_read",
    "pages_read_engagement",
    "pages_manage_ads",
    "public_profile",
]


class CsrfMismatchError(Exception):
    """Raised when state validation fails."""

    def __init__(self, message: str = "Yêu cầu xác thực không hợp lệ (CSRF detected)") -> None:
        self.message = message
        super().__init__(self.message)


class OAuthAccessDeniedError(Exception):
    """Raised when user denies Facebook OAuth authorization."""

    def __init__(self, message: str = "Người dùng đã từ chối cấp quyền trên Facebook") -> None:
        self.message = message
        super().__init__(self.message)


class MetaAuthService:
    """Service handling OAuth initialization, code/token exchange, and session status."""

    PLACEHOLDER_APP_IDS = {"", "test_meta_app_id", "your_meta_app_id", "none"}
    PLACEHOLDER_SECRETS = {"", "test_meta_app_secret", "your_meta_app_secret", "none"}

    def __init__(
        self,
        client: MetaClientService | None = None,
        repository: SessionRepository | None = None,
    ) -> None:
        self.client = client or meta_client
        self.repo = repository or session_repo

    def _resolve_app_id(self, override_app_id: str | None = None) -> str:
        """Resolve effective Meta App ID, reloading .env if needed."""
        if override_app_id and override_app_id.strip() not in self.PLACEHOLDER_APP_IDS:
            settings.META_APP_ID = override_app_id.strip()
            return settings.META_APP_ID

        current = settings.META_APP_ID.strip()
        if current in self.PLACEHOLDER_APP_IDS:
            try:
                from dotenv import dotenv_values

                env_vals = dotenv_values(".env")
                env_app_id = (env_vals.get("META_APP_ID") or "").strip()
                if env_app_id and env_app_id not in self.PLACEHOLDER_APP_IDS:
                    settings.META_APP_ID = env_app_id
                    return env_app_id
            except Exception:
                pass
        return settings.META_APP_ID.strip()

    def is_valid_app_id(self, app_id: str | None = None) -> bool:
        """Check if the configured Meta App ID is a real numeric Facebook App ID."""
        resolved = self._resolve_app_id(app_id)
        return bool(resolved and resolved not in self.PLACEHOLDER_APP_IDS and resolved.isdigit())

    def _has_real_app_secret(self) -> bool:
        """Check whether a real App Secret is configured."""
        secret = (settings.META_APP_SECRET or "").strip()
        return secret not in self.PLACEHOLDER_SECRETS

    def generate_oauth_url(
        self,
        app_id: str | None = None,
        scope_mode: str = "full",
    ) -> tuple[str, str]:
        """
        Generate cryptographically secure state and construct Meta OAuth URL.
        Uses response_type='token' (Implicit Flow - Option 2) when App Secret is not provided.
        """
        effective_app_id = self._resolve_app_id(app_id)
        state = state_manager.generate_state()

        # Option 2: Use response_type=token when App Secret is unavailable
        response_type = "code" if self._has_real_app_secret() else "token"

        scopes = (
            ["public_profile", "pages_show_list", "pages_read_engagement", "pages_manage_posts"]
            if scope_mode == "page_only"
            else REQUIRED_SCOPES
        )

        params = {
            "client_id": effective_app_id,
            "redirect_uri": settings.META_REDIRECT_URI,
            "scope": ",".join(scopes),
            "state": state,
            "response_type": response_type,
        }
        encoded_params = urllib.parse.urlencode(params)
        auth_url = f"{settings.META_OAUTH_BASE_URL}?{encoded_params}"
        return auth_url, state

    async def save_implicit_token(
        self,
        access_token: str,
        state: str | None = None,
        token_type: str = "bearer",
        expires_in: int | None = None,
    ) -> str:
        """Save token obtained from OAuth Implicit Flow (response_type=token) or Graph Explorer."""
        clean_token = access_token.strip()
        if not clean_token:
            raise ValueError("Access Token không được để trống")

        # Consume state if present in state_manager
        if state:
            state_manager.verify_and_consume(state)

        await self.repo.save_session(
            access_token=clean_token,
            token_type=token_type or "bearer",
            expires_in=expires_in,
        )
        return f"{settings.FRONTEND_URL}/?connected=true"

    async def handle_callback(
        self,
        code: str | None,
        state: str | None,
        error: str | None = None,
        error_description: str | None = None,
    ) -> str:
        """Process callback from Meta. Returns frontend redirect target URL."""
        if error:
            # User canceled or denied permission
            return f"{settings.FRONTEND_URL}/?error={urllib.parse.quote(error)}"

        if not state or not state_manager.verify_and_consume(state):
            raise CsrfMismatchError()

        if not code:
            return f"{settings.FRONTEND_URL}/?error=missing_code"

        # Exchange authorization code for User Access Token
        token_data = await self.client.exchange_oauth_code(code)
        access_token = token_data.get("access_token", "")
        token_type = token_data.get("token_type", "bearer")
        expires_in = token_data.get("expires_in")

        # Persist session with id=1
        await self.repo.save_session(
            access_token=access_token,
            token_type=token_type,
            expires_in=expires_in,
        )

        return f"{settings.FRONTEND_URL}/?connected=true"

    async def get_status(self) -> dict[str, Any]:
        """Check current Meta session status in SQLite."""
        resolved_app_id = self._resolve_app_id()
        app_id_valid = self.is_valid_app_id()
        display_app_id = resolved_app_id if app_id_valid else None

        session = await self.repo.get_session()
        if not session:
            return {
                "connected": False,
                "has_token": False,
                "app_id_configured": app_id_valid,
                "current_app_id": display_app_id,
            }

        token = await self.repo.get_access_token()
        if not token:
            return {
                "connected": False,
                "has_token": False,
                "app_id_configured": app_id_valid,
                "current_app_id": display_app_id,
            }

        return {
            "connected": True,
            "has_token": True,
            "token_type": session.get("token_type", "bearer"),
            "updated_at": session.get("updated_at"),
            "app_id_configured": app_id_valid,
            "current_app_id": display_app_id,
        }

    async def disconnect(self) -> bool:
        """Clear active session from SQLite."""
        return await self.repo.delete_session()


meta_auth_service = MetaAuthService()
