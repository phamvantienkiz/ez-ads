"""Health check endpoint verifying application and database connectivity."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.api.deps import get_request_id
from app.core.config import settings
from app.core.database import get_db_connection
from app.schemas.common import ResponseMeta, SuccessResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=SuccessResponse[dict[str, Any]])
async def health_check(
    request: Request,
    request_id: Annotated[str, Depends(get_request_id)],
) -> SuccessResponse[dict[str, Any]]:
    """Check health status of backend and verify SQLite connection."""
    db_status = "connected"
    try:
        async with get_db_connection() as db, db.execute("SELECT 1") as cursor:
            await cursor.fetchone()
    except Exception:
        db_status = "disconnected"

    return SuccessResponse[dict[str, Any]](
        success=True,
        status_code=200,
        message="Hệ thống hoạt động bình thường",
        data={
            "status": "healthy" if db_status == "connected" else "degraded",
            "version": "1.0.0",
            "database": db_status,
            "environment": settings.ENVIRONMENT,
        },
        meta=ResponseMeta(request_id=request_id),
    )
