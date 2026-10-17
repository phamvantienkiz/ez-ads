"""Ad creation, campaigns, and execution history endpoints."""

from typing import Annotated, Any, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse

from app.api.deps import (
    get_ad_service,
    get_meta_client,
    get_request_id,
    get_run_repo,
    require_access_token,
)
from app.core.logging import logger
from app.repositories.run_repository import RunRepository
from app.schemas.ad_schemas import (
    AdCreationData,
    AdCreationRequest,
    AdResources,
    AdRunItem,
    CampaignItem,
)
from app.schemas.common import ErrorDetail, ErrorResponse, ResponseMeta, SuccessResponse
from app.services.ad_service import (
    AdCreationService,
    DoubleSubmitLockedError,
    PartialCreationError,
    SessionNotFoundError,
)
from app.services.meta_client import MetaApiError, MetaClientService

ads_router = APIRouter(prefix="/ads", tags=["Ads"])
campaigns_router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


# =============================================================================
# Campaigns Endpoint
# =============================================================================
@campaigns_router.get("", response_model=SuccessResponse[list[CampaignItem]])
async def get_campaigns(
    request: Request,
    request_id: Annotated[str, Depends(get_request_id)],
    token: Annotated[str, Depends(require_access_token)],
    meta_client: Annotated[MetaClientService, Depends(get_meta_client)],
    ad_account_id: str = Query(..., description="Ad Account ID (e.g. act_123456)"),
    limit: int = Query(25, ge=1, le=100, description="Records limit"),
    status: str | None = Query(None, description="Status filter (ACTIVE, PAUSED, ARCHIVED)"),
) -> SuccessResponse[list[CampaignItem]]:
    """Fetch campaigns directly from Meta Marketing API."""
    try:
        raw_campaigns = await meta_client.get_campaigns(
            token=token,
            ad_account_id=ad_account_id,
            limit=limit,
            status=status,
        )
        items = [CampaignItem(**c) for c in raw_campaigns]

        return SuccessResponse[list[CampaignItem]](
            success=True,
            status_code=200,
            message="Tải danh sách chiến dịch thành công từ Meta API",
            data=items,
            meta=ResponseMeta(
                request_id=request_id,
                count=len(items),
                limit=limit,
                ad_account_id=ad_account_id,
            ),
        )
    except MetaApiError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail={
                "code": exc.code,
                "message": f"Không thể lấy danh sách chiến dịch từ Meta API: {exc.message}",
            },
        ) from exc


# =============================================================================
# Ad Creation Endpoint
# =============================================================================
@ads_router.post(
    "",
    response_model=SuccessResponse[AdCreationData],
    status_code=status.HTTP_201_CREATED,
)
async def create_ad(
    request: Request,
    body: AdCreationRequest,
    request_id: Annotated[str, Depends(get_request_id)],
    ad_service: Annotated[AdCreationService, Depends(get_ad_service)],
    x_idempotency_key: str | None = Header(None, alias="X-Idempotency-Key"),
) -> Any:
    """Execute the 5-step sequential Meta Marketing API pipeline to create an ad."""
    try:
        result = await ad_service.execute_ad_creation_pipeline(body)
        creation_data = AdCreationData(
            run_id=result["run_id"],
            status=result["status"],
            ad_account_id=result["ad_account_id"],
            page_id=result["page_id"],
            resources=AdResources(**result["resources"]),
            configuration=result.get("configuration"),
        )
        return SuccessResponse[AdCreationData](
            success=True,
            status_code=status.HTTP_201_CREATED,
            message="Tạo quảng cáo thành công trên Meta Marketing API (Mặc định trạng thái PAUSED)",
            data=creation_data,
            meta=ResponseMeta(request_id=request_id),
        )
    except DoubleSubmitLockedError as exc:
        logger.warning("[%s] Double submit detected", request_id)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=ErrorResponse(
                success=False,
                status_code=409,
                message=exc.message,
                error=ErrorDetail(code="DOUBLE_SUBMIT_LOCKED", message=exc.message),
                meta=ResponseMeta(request_id=request_id),
            ).model_dump(by_alias=True),
        )
    except PartialCreationError as exc:
        logger.error("[%s] Partial creation failure in pipeline: %s", request_id, exc.message)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "statusCode": 400,
                "message": exc.message,
                "error": {
                    "code": "PARTIAL_CREATION_FAILURE",
                    "failedStep": exc.failed_step,
                    "message": exc.message,
                },
                "data": {
                    "runId": exc.run_id,
                    "status": "partial_failure",
                    "createdResources": {
                        "imageHash": exc.created_resources.get("image_hash"),
                        "campaignId": exc.created_resources.get("campaign_id"),
                        "adsetId": exc.created_resources.get("adset_id"),
                        "creativeId": exc.created_resources.get("creative_id"),
                        "adId": exc.created_resources.get("ad_id"),
                    },
                },
                "meta": {
                    "timestamp": ResponseMeta().timestamp,
                    "requestId": request_id,
                },
            },
        )
    except SessionNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=ErrorResponse(
                success=False,
                status_code=401,
                message=exc.message,
                error=ErrorDetail(code="SESSION_NOT_FOUND", message=exc.message),
                meta=ResponseMeta(request_id=request_id),
            ).model_dump(by_alias=True),
        )
    except MetaApiError as exc:
        logger.error("[%s] Meta API failure: %s", request_id, exc.message)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                success=False,
                status_code=400,
                message=exc.message,
                error=ErrorDetail(code=exc.code, message=exc.message),
                meta=ResponseMeta(request_id=request_id),
            ).model_dump(by_alias=True),
        )


# =============================================================================
# Run History Endpoints
# =============================================================================
@ads_router.get("/runs/latest", response_model=SuccessResponse[Optional[AdRunItem]])
async def get_latest_run(
    request: Request,
    request_id: Annotated[str, Depends(get_request_id)],
    run_repo: Annotated[RunRepository, Depends(get_run_repo)],
) -> SuccessResponse[AdRunItem | None]:
    """Retrieve the most recent ad creation run for dashboard display."""
    run = await run_repo.get_latest_run()
    if not run:
        return SuccessResponse[Optional[AdRunItem]](
            success=True,
            status_code=200,
            message="Chưa có lượt tạo quảng cáo nào trong phiên này",
            data=None,
            meta=ResponseMeta(request_id=request_id),
        )

    return SuccessResponse[Optional[AdRunItem]](
        success=True,
        status_code=200,
        message="Lấy phiên tạo quảng cáo gần nhất thành công",
        data=AdRunItem(**run),
        meta=ResponseMeta(request_id=request_id),
    )


@ads_router.get("/runs/{id}", response_model=SuccessResponse[AdRunItem])
@ads_router.get("/{id}", response_model=SuccessResponse[AdRunItem])
async def get_run_by_id(
    id: int,
    request: Request,
    request_id: Annotated[str, Depends(get_request_id)],
    run_repo: Annotated[RunRepository, Depends(get_run_repo)],
) -> SuccessResponse[AdRunItem]:
    """Retrieve a specific run by ID (supports alias /ads/{id})."""
    run = await run_repo.get_run_by_id(id)
    if not run:
        raise HTTPException(
            status_code=404,
            detail={"code": "RUN_NOT_FOUND", "message": f"Không tìm thấy phiên chạy có ID {id}"},
        )

    return SuccessResponse[AdRunItem](
        success=True,
        status_code=200,
        message="Lấy chi tiết phiên tạo quảng cáo thành công",
        data=AdRunItem(**run),
        meta=ResponseMeta(request_id=request_id),
    )
