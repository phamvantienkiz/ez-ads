"""Meta digital assets (Ad Accounts and Fanpages) endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from app.api.deps import get_meta_client, get_request_id, require_access_token
from app.schemas.asset_schemas import AdAccountItem, PageItem
from app.schemas.common import ResponseMeta, SuccessResponse
from app.services.meta_client import MetaClientService

router = APIRouter(prefix="/meta", tags=["Meta Assets"])


@router.get("/ad-accounts", response_model=SuccessResponse[list[AdAccountItem]])
async def get_ad_accounts(
    request: Request,
    request_id: Annotated[str, Depends(get_request_id)],
    token: Annotated[str, Depends(require_access_token)],
    meta_client: Annotated[MetaClientService, Depends(get_meta_client)],
    fields: str | None = Query("id,name,account_id,currency,account_status"),
) -> SuccessResponse[list[AdAccountItem]]:
    """Fetch list of Ad Accounts the authenticated Facebook user can access."""
    accounts = await meta_client.get_ad_accounts(token=token, fields=fields or "id,name,currency,account_status")
    items = [AdAccountItem(**acc) for acc in accounts]

    return SuccessResponse[list[AdAccountItem]](
        success=True,
        status_code=200,
        message="Tải danh sách tài khoản quảng cáo thành công",
        data=items,
        meta=ResponseMeta(request_id=request_id, total=len(items)),
    )


@router.get("/pages", response_model=SuccessResponse[list[PageItem]])
async def get_pages(
    request: Request,
    request_id: Annotated[str, Depends(get_request_id)],
    token: Annotated[str, Depends(require_access_token)],
    meta_client: Annotated[MetaClientService, Depends(get_meta_client)],
    fields: str | None = Query("id,name,category"),
) -> SuccessResponse[list[PageItem]]:
    """Fetch list of Facebook Pages managed by the authenticated user."""
    pages = await meta_client.get_pages(token=token, fields=fields or "id,name,category")
    items = [PageItem(**p) for p in pages]

    return SuccessResponse[list[PageItem]](
        success=True,
        status_code=200,
        message="Tải danh sách Facebook Page thành công",
        data=items,
        meta=ResponseMeta(request_id=request_id, total=len(items)),
    )
