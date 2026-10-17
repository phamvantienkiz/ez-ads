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
    """Service handling OAuth initialization, code exchange, and session status."""

    def __init__(
        self,
        client: MetaClientService | None = None,
        repository: SessionRepository | None = None,
    ) -> None:
        self.client = client or meta_client
        self.repo = repository or session_repo

    def generate_oauth_url(self) -> tuple[str, str]:
        """Generate cryptographically secure state and construct Meta OAuth URL."""
        state = state_manager.generate_state()
        params = {
            "client_id": settings.META_APP_ID,
            "redirect_uri": settings.META_REDIRECT_URI,
            "scope": ",".join(REQUIRED_SCOPES),
            "state": state,
            "response_type": "code",
        }
        encoded_params = urllib.parse.urlencode(params)
        auth_url = f"{settings.META_OAUTH_BASE_URL}?{encoded_params}"
        return auth_url, state

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
        session = await self.repo.get_session()
        if not session:
            return {"connected": False, "has_token": False}

        token = await self.repo.get_access_token()
        if not token:
            return {"connected": False, "has_token": False}

        return {
            "connected": True,
            "has_token": True,
            "token_type": session.get("token_type", "bearer"),
            "updated_at": session.get("updated_at"),
        }

    async def disconnect(self) -> bool:
        """Clear active session from SQLite."""
        return await self.repo.delete_session()


meta_auth_service = MetaAuthService()
