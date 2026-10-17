"""Middleware registration registry."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares.cors import get_cors_config
from app.middlewares.error_handler import ErrorHandlingMiddleware
from app.middlewares.logging import RequestLoggingMiddleware
from app.middlewares.request_id import RequestIDMiddleware


def register_middlewares(app: FastAPI) -> None:
    """Register all cross-cutting middlewares in proper execution order."""
    # Starlette adds middleware in reverse order:
    # 1. ErrorHandlingMiddleware (outermost)
    # 2. CORSMiddleware
    # 3. RequestLoggingMiddleware
    # 4. RequestIDMiddleware (innermost)
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(CORSMiddleware, **get_cors_config())
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)
