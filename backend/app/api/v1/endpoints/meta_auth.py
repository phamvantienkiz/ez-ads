"""Meta OAuth 2.0 authentication endpoints."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from app.api.deps import get_auth_service, get_request_id
from app.core.config import settings
from app.core.logging import logger
from app.schemas.auth_schemas import (
    MetaConnectData,
    MetaDisconnectData,
    MetaStatusData,
    MetaTokenCallbackRequest,
)
from app.schemas.common import ErrorDetail, ErrorResponse, ResponseMeta, SuccessResponse
from app.services.meta_auth_service import (
    CsrfMismatchError,
    MetaAuthService,
)

router = APIRouter(prefix="/meta", tags=["Meta Auth"])

IMPLICIT_OAUTH_BRIDGE_HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8" />
  <title>Đang kết nối Meta...</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #F5F5F7;
      color: #0B0B0F;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
    }}
    .card {{
      background: #fff;
      padding: 28px 32px;
      border-radius: 24px;
      box-shadow: 0 8px 24px rgba(16, 16, 24, 0.06);
      text-align: center;
      max-width: 420px;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h3 style="margin: 0 0 8px 0;">Đang hoàn tất kết nối Facebook...</h3>
    <p id="msg" style="color: #6B6B76; font-size: 14px; margin: 0;">Đang lưu phiên làm việc an toàn vào hệ thống.</p>
  </div>
  <script>
    (async function() {{
      const frontendUrl = "{frontend_url}";
      const hash = window.location.hash ? window.location.hash.substring(1) : "";
      const params = new URLSearchParams(hash);
      const accessToken = params.get("access_token");
      const state = params.get("state");
      const expiresIn = params.get("expires_in");
      const error = params.get("error") || params.get("error_reason");

      if (error) {{
        window.location.replace(frontendUrl + "/?error=" + encodeURIComponent(error));
        return;
      }}

      if (!accessToken) {{
        window.location.replace(frontendUrl + "/?error=missing_token");
        return;
      }}

      try {{
        const res = await fetch("/api/v1/meta/token-callback", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{
            access_token: accessToken,
            state: state,
            expires_in: expiresIn ? parseInt(expiresIn, 10) : null,
            token_type: "bearer"
          }})
        }});
        if (res.ok) {{
          window.location.replace(frontendUrl + "/?connected=true");
        }} else {{
          window.location.replace(frontendUrl + "/?error=token_save_failed");
        }}
      }} catch (e) {{
        window.location.replace(frontendUrl + "/?error=network_error");
      }}
    }})();
  </script>
</body>
</html>
"""


@router.get("/connect", response_model=SuccessResponse[MetaConnectData])
async def meta_connect(
    request: Request,
    request_id: Annotated[str, Depends(get_request_id)],
    auth_service: Annotated[MetaAuthService, Depends(get_auth_service)],
    app_id: str | None = Query(None, description="Optional Meta App ID override"),
    scope_mode: str = Query("full", description="Scope mode: full or page_only"),
) -> SuccessResponse[MetaConnectData]:
    """Generate CSRF state and return official Meta OAuth authorization URL."""
    auth_url, _ = auth_service.generate_oauth_url(app_id=app_id, scope_mode=scope_mode)
    app_id_valid = auth_service.is_valid_app_id(app_id)
    resolved_id = auth_service._resolve_app_id(app_id)
    return SuccessResponse[MetaConnectData](
        success=True,
        status_code=200,
        message="Khởi tạo URL OAuth thành công (Chế độ không cần App Secret)",
        data=MetaConnectData(
            auth_url=auth_url,
            app_id_configured=app_id_valid,
            current_app_id=resolved_id if app_id_valid else None,
        ),
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
    """
    Handle OAuth redirect callback from Meta.
    Supports both Authorization Code flow (?code=...) and Implicit Token flow (#access_token=...).
    """
    # If redirected from response_type=token, parameters are in URL hash (#access_token=...)
    if code is None and error is None and state is None:
        html_content = IMPLICIT_OAUTH_BRIDGE_HTML.format(frontend_url=settings.FRONTEND_URL.rstrip("/"))
        return HTMLResponse(content=html_content, status_code=200)

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


@router.post("/token-callback", response_model=SuccessResponse[MetaStatusData])
async def meta_token_callback(
    request: Request,
    body: MetaTokenCallbackRequest,
    request_id: Annotated[str, Depends(get_request_id)],
    auth_service: Annotated[MetaAuthService, Depends(get_auth_service)],
) -> Any:
    """Save access token from Implicit OAuth flow (response_type=token) or direct input."""
    try:
        await auth_service.save_implicit_token(
            access_token=body.access_token,
            state=body.state,
            token_type=body.token_type,
            expires_in=body.expires_in,
        )
        status_dict = await auth_service.get_status()
        return SuccessResponse[MetaStatusData](
            success=True,
            status_code=200,
            message="Đã lưu phiên kết nối Meta thành công (Không cần App Secret)",
            data=MetaStatusData(
                connected=True,
                has_token=True,
                token_type=status_dict.get("token_type", "bearer"),
                updated_at=status_dict.get("updated_at"),
                app_id_configured=status_dict.get("app_id_configured", True),
                current_app_id=status_dict.get("current_app_id"),
            ),
            meta=ResponseMeta(request_id=request_id),
        )
    except Exception as exc:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                success=False,
                status_code=400,
                message=f"Không thể lưu Access Token: {exc}",
                error=ErrorDetail(code="TOKEN_SAVE_FAILED", message=str(exc)),
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
            app_id_configured=status_dict.get("app_id_configured", False),
            current_app_id=status_dict.get("current_app_id"),
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
