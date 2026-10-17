"""FastAPI dependencies for dependency injection."""

from typing import Annotated

from fastapi import Depends, HTTPException, Request

from app.repositories.run_repository import RunRepository, run_repo
from app.repositories.session_repository import SessionRepository, session_repo
from app.services.ad_service import AdCreationService, ad_service
from app.services.meta_auth_service import MetaAuthService, meta_auth_service
from app.services.meta_client import MetaClientService, meta_client


def get_request_id(request: Request) -> str:
    """Extract request id from request.state."""
    return getattr(request.state, "request_id", "req_unknown")


def get_session_repo() -> SessionRepository:
    """Provide session repository."""
    return session_repo


def get_run_repo() -> RunRepository:
    """Provide run repository."""
    return run_repo


def get_meta_client() -> MetaClientService:
    """Provide Meta client service."""
    return meta_client


def get_auth_service() -> MetaAuthService:
    """Provide Meta auth service."""
    return meta_auth_service


def get_ad_service() -> AdCreationService:
    """Provide Ad creation service."""
    return ad_service


async def require_access_token(
    session_repository: Annotated[SessionRepository, Depends(get_session_repo)],
) -> str:
    """Validate that an active, non-expired Meta session exists and return access token."""
    token = await session_repository.get_access_token()
    if not token:
        raise HTTPException(
            status_code=401,
            detail={
                "code": "SESSION_NOT_FOUND",
                "message": "Chưa có phiên kết nối Meta. Vui lòng nhấn Connect Facebook trước",
            },
        )
    return token
