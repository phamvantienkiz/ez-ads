"""Request logging middleware calculating execution duration and logging access."""

import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import logger


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log access logs and inject X-Process-Time header."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()
        request_id = getattr(request.state, "request_id", "req_unknown")

        response = await call_next(request)

        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"

        logger.info(
            "[%s] %s %s completed with status %d in %.4fs",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )

        return response
