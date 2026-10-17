"""API v1 Router aggregating all endpoint subrouters."""

from fastapi import APIRouter

from app.api.v1.endpoints.ads import ads_router, campaigns_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.meta_assets import router as meta_assets_router
from app.api.v1.endpoints.meta_auth import router as meta_auth_router

api_v1_router = APIRouter()

api_v1_router.include_router(health_router)
api_v1_router.include_router(meta_auth_router)
api_v1_router.include_router(meta_assets_router)
api_v1_router.include_router(ads_router)
api_v1_router.include_router(campaigns_router)
