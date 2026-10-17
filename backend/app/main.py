"""FastAPI main application entrypoint for BAHA Ads Manager."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.endpoints.health import router as root_health_router
from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.database import init_db
from app.core.logging import logger
from app.middlewares import register_middlewares
from app.schemas.common import ErrorDetail, ErrorResponse, ResponseMeta


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifecycle context: initializes database on startup."""
    logger.info("Starting BAHA Ads Manager API Backend [%s]...", settings.ENVIRONMENT)
    await init_db()
    yield
    logger.info("Shutting down BAHA Ads Manager API Backend...")


def create_app() -> FastAPI:
    """Application factory creating and configuring the FastAPI app."""
    app = FastAPI(
        title="BAHA Ads Manager API",
        description="Official Meta Marketing API (v20.0) Integration Backend",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Register cross-cutting middlewares (order: error_handler, cors, logging, request_id)
    register_middlewares(app)

    # -------------------------------------------------------------------------
    # Exception Handlers for Consistent Response Envelope (Pattern 7)
    # -------------------------------------------------------------------------
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "req_unknown")
        detail = exc.detail
        code = "HTTP_ERROR"
        message = str(detail)
        details = []

        if isinstance(detail, dict):
            code = detail.get("code", "HTTP_ERROR")
            message = detail.get("message", message)
            details = detail.get("details", [])

        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                success=False,
                status_code=exc.status_code,
                message=message,
                error=ErrorDetail(code=code, message=message, details=details),
                meta=ResponseMeta(request_id=request_id),
            ).model_dump(by_alias=True),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        request_id = getattr(request.state, "request_id", "req_unknown")
        # Format Pydantic validation errors nicely
        errors = []
        for err in exc.errors():
            loc = " -> ".join(str(part) for part in err.get("loc", []))
            errors.append(f"{loc}: {err.get('msg', 'Invalid')}")

        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                success=False,
                status_code=422,
                message="Dữ liệu đầu vào không hợp lệ",
                error=ErrorDetail(
                    code="VALIDATION_ERROR",
                    message="Kiểm tra lại các trường trong dữ liệu gửi lên",
                    details=errors,
                ),
                meta=ResponseMeta(request_id=request_id),
            ).model_dump(by_alias=True),
        )

    # -------------------------------------------------------------------------
    # Router Mounts: Official v1 and Backward Compatibility Aliases
    # -------------------------------------------------------------------------
    # 1. Root health check
    app.include_router(root_health_router)

    # 2. Official REST API v1: /api/v1/...
    app.include_router(api_v1_router, prefix="/api/v1")

    # 3. Requirement / PRD backward compatible alias: /api/...
    app.include_router(api_v1_router, prefix="/api")

    return app


app = create_app()
