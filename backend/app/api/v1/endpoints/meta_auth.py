"""Meta OAuth 2.0 authentication endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse, Response

from app.api.deps import get_auth_service, get_request_id
from app.core.logging import logger
from app.schemas.auth_schemas import MetaConnectData, MetaDisconnectData, MetaStatusData
from app.schemas.common import ErrorDetail, ErrorResponse, ResponseMeta, SuccessResponse
from app.services.meta_auth_service import (
    CsrfMismatchError,
    MetaAuthService,
)

router = APIRouter(prefix="/meta", tags=["Meta Auth"])


@router.get("/connect", response_model=SuccessResponse[MetaConnectData])
async def meta_connect(
    request: Request,
    request_id: Annotated[str, Depends(get_request_id)],
    auth_service: Annotated[MetaAuthService, Depends(get_auth_service)],
) -> SuccessResponse[MetaConnectData]:
    """Generate CSRF state and return official Meta OAuth authorization URL."""
    auth_url, _ = auth_service.generate_oauth_url()
    return SuccessResponse[MetaConnectData](
        success=True,
        status_code=200,
        message="Khởi tạo URL OAuth thành công",
        data=MetaConnectData(auth_url=auth_url),
        meta=ResponseMeta(request_id=request_id),
    )


@router.get("/callback")
async def meta_callback(
    request: Request,
    request_id: Annotated[str, Depends(get_request_id)],
    auth_service: Annotated[MetaAuthService, Depends(get_auth_service)],
    code: str | None = Query(None, description="OAuth code from Facebook"),
    state: str | None = Query(None, description="CSRF state nonce"),
    error: str | None = Query(None, description="Error code if user denied"),
    error_description: str | None = Query(None, description="Description of the error"),
) -> Response:
    """Handle OAuth redirect callback from Meta."""
    try:
        redirect_target = await auth_service.handle_callback(
            code=code,
            state=state,
            error=error,
            error_description=error_description,
        )
        return RedirectResponse(url=redirect_target, status_code=302)
    except CsrfMismatchError:
        logger.warning("[%s] CSRF State mismatch during OAuth callback", request_id)
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                success=False,
                status_code=400,
                message="Yêu cầu xác thực không hợp lệ (CSRF detected)",
                error=ErrorDetail(
                    code="OAUTH_CSRF_MISMATCH",
                    message="Mã nonce bảo vệ CSRF không khớp hoặc đã hết hạn",
                ),
                meta=ResponseMeta(request_id=request_id),
            ).model_dump(by_alias=True),
        )
    except Exception as exc:
        logger.error("[%s] Error during Meta OAuth code exchange: %s", request_id, str(exc))
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                success=False,
                status_code=400,
                message="Không thể hoàn tất kết nối Meta: kiểm tra lại mã xác thực",
                error=ErrorDetail(
                    code="OAUTH_EXCHANGE_FAILED",
                    message=str(exc),
                ),
                meta=ResponseMeta(request_id=request_id),
            ).model_dump(by_alias=True),
        )


@router.get("/status", response_model=SuccessResponse[MetaStatusData])
async def meta_status(
    request: Request,
    request_id: Annotated[str, Depends(get_request_id)],
    auth_service: Annotated[MetaAuthService, Depends(get_auth_service)],
) -> SuccessResponse[MetaStatusData]:
    """Check current Meta connection and token validity status."""
    status_dict = await auth_service.get_status()
    is_connected = status_dict.get("connected", False)

    return SuccessResponse[MetaStatusData](
        success=True,
        status_code=200,
        message="Trạng thái phiên kết nối Meta" if is_connected else "Chưa có phiên kết nối Meta",
        data=MetaStatusData(
            connected=is_connected,
            has_token=status_dict.get("has_token", False),
            token_type=status_dict.get("token_type"),
            updated_at=status_dict.get("updated_at"),
        ),
        meta=ResponseMeta(request_id=request_id),
    )


@router.post("/disconnect", response_model=SuccessResponse[MetaDisconnectData])
async def meta_disconnect(
    request: Request,
    request_id: Annotated[str, Depends(get_request_id)],
    auth_service: Annotated[MetaAuthService, Depends(get_auth_service)],
) -> SuccessResponse[MetaDisconnectData]:
    """Clear Meta session and disconnect account."""
    await auth_service.disconnect()
    return SuccessResponse[MetaDisconnectData](
        success=True,
        status_code=200,
        message="Đã ngắt kết nối Meta thành công",
        data=MetaDisconnectData(connected=False),
        meta=ResponseMeta(request_id=request_id),
    )
