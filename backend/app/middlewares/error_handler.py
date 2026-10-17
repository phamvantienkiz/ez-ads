"""Global unhandled exception handling middleware returning consistent error envelope."""

from datetime import UTC, datetime

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.logging import logger
from app.core.security import sanitize_meta_error


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Catch-all middleware for unhandled exceptions to prevent server crashes."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            request_id = getattr(request.state, "request_id", "req_unknown")
            safe_message = sanitize_meta_error(str(exc))
            logger.exception("[%s] Unhandled server error: %s", request_id, safe_message)

            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "statusCode": 500,
                    "message": "Đã xảy ra lỗi máy chủ nội bộ. Vui lòng thử lại sau",
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "details": [safe_message],
                    },
                    "meta": {
                        "timestamp": datetime.now(UTC).isoformat(),
                        "requestId": request_id,
                    },
                },
            )
