"""Ad creation service orchestrating the 5-step sequential Meta Marketing API pipeline."""

import asyncio
import json
from typing import Any

from app.core.logging import logger
from app.core.security import sanitize_meta_error
from app.repositories.run_repository import RunRepository, run_repo
from app.repositories.session_repository import SessionRepository, session_repo
from app.schemas.ad_schemas import AdCreationRequest
from app.services.meta_client import MetaApiError, MetaClientService, meta_client

ZERO_DECIMAL_CURRENCIES = {"VND", "JPY", "KRW", "CLP", "PYG", "UGX"}

DEFAULT_TARGETING = {
    "geo_locations": {
        "countries": ["VN"],
    },
    "age_min": 18,
    "age_max": 65,
}


def format_meta_budget(amount: float, currency: str = "VND") -> str:
    """
    Convert daily budget amount to Meta Marketing API accepted unit.
    - Currencies with cents (USD, EUR, GBP...): multiply by 100.
    - Zero-decimal currencies (VND, JPY, KRW...): keep integer.
    """
    curr = currency.upper().strip()
    if curr in ZERO_DECIMAL_CURRENCIES:
        return str(int(amount))
    return str(int(amount * 100))


class SessionNotFoundError(Exception):
    """Raised when there is no active Meta session in SQLite."""

    def __init__(self, message: str = "Chưa có phiên kết nối Meta. Vui lòng kết nối trước") -> None:
        self.message = message
        super().__init__(self.message)


class DoubleSubmitLockedError(Exception):
    """Raised when an ad creation request is already running."""

    def __init__(
        self,
        message: str = "Một yêu cầu tạo quảng cáo đang được xử lý. Vui lòng không gửi trùng lặp",
    ) -> None:
        self.message = message
        super().__init__(self.message)


class PartialCreationError(Exception):
    """Raised when intermediate steps succeed but a subsequent step fails."""

    def __init__(
        self,
        message: str,
        failed_step: str,
        created_resources: dict[str, str | None],
        run_id: int,
    ) -> None:
        self.message = message
        self.failed_step = failed_step
        self.created_resources = created_resources
        self.run_id = run_id
        super().__init__(self.message)


class AdCreationService:
    """Service orchestrating the 5 API calls in order."""

    def __init__(
        self,
        client: MetaClientService | None = None,
        session_repository: SessionRepository | None = None,
        run_repository: RunRepository | None = None,
    ) -> None:
        self.client = client or meta_client
        self.session_repo = session_repository or session_repo
        self.run_repo = run_repository or run_repo
        self._lock = asyncio.Lock()

    async def execute_ad_creation_pipeline(
        self,
        request: AdCreationRequest,
        currency: str = "VND",
    ) -> dict[str, Any]:
        """Execute the 5-step ad creation pipeline with strict safety invariants."""
        # AC5: Double submit lock check
        if self._lock.locked():
            raise DoubleSubmitLockedError()

        async with self._lock:
            # Check active session token
            token = await self.session_repo.get_access_token()
            if not token:
                raise SessionNotFoundError()

            # Record initial run in SQLite
            summary = {
                "campaign_name": request.campaign_name,
                "budget_amount": request.budget_amount,
                "currency": currency,
                "headline": request.headline,
                "destination_url": request.destination_url,
                "image_url": request.image_url,
            }
            run_id = await self.run_repo.create_run(
                ad_account_id=request.ad_account_id,
                page_id=request.page_id,
                status="pending",
                request_summary=json.dumps(summary, ensure_ascii=False),
            )

            created_resources: dict[str, str | None] = {
                "image_hash": None,
                "campaign_id": None,
                "adset_id": None,
                "creative_id": None,
                "ad_id": None,
            }

            # -------------------------------------------------------------
            # Step 1: Upload Image & Get Hash
            # -------------------------------------------------------------
            logger.info("Pipeline [Run %d] Step 1: Uploading image: %s", run_id, request.image_url)
            try:
                image_hash = await self.client.upload_ad_image(
                    token=token,
                    ad_account_id=request.ad_account_id,
                    image_url=request.image_url,
                )
                created_resources["image_hash"] = image_hash
            except (MetaApiError, Exception) as exc:
                err_msg = sanitize_meta_error(str(exc))
                await self.run_repo.update_run(
                    run_id=run_id,
                    status="failed",
                    error_message=f"Lỗi tại bước tải ảnh: {err_msg}",
                )
                raise MetaApiError(
                    code="META_IMAGE_HASH_FAILED",
                    message=f"Không thể tải hình ảnh từ URL đã cung cấp: {err_msg}",
                ) from exc

            # -------------------------------------------------------------
            # Step 2: Create Campaign (Default: PAUSED, OUTCOME_TRAFFIC)
            # -------------------------------------------------------------
            logger.info("Pipeline [Run %d] Step 2: Creating campaign: %s", run_id, request.campaign_name)
            try:
                campaign_id = await self.client.create_campaign(
                    token=token,
                    ad_account_id=request.ad_account_id,
                    name=request.campaign_name,
                    objective="OUTCOME_TRAFFIC",
                    status="PAUSED",
                )
                created_resources["campaign_id"] = campaign_id
                await self.run_repo.update_run(run_id=run_id, campaign_id=campaign_id)
            except (MetaApiError, Exception) as exc:
                err_msg = sanitize_meta_error(str(exc))
                await self.run_repo.update_run(
                    run_id=run_id,
                    status="failed",
                    error_message=f"Lỗi tạo chiến dịch: {err_msg}",
                )
                raise MetaApiError(
                    code="META_CAMPAIGN_CREATE_FAILED",
                    message=f"Lỗi khi tạo chiến dịch trên Meta: {err_msg}",
                ) from exc

            # -------------------------------------------------------------
            # Step 3: Create Ad Set (Default: PAUSED, VN, 18-65)
            # -------------------------------------------------------------
            adset_name = request.adset_name or f"{request.campaign_name} - AdSet"
            formatted_budget = format_meta_budget(request.budget_amount, currency)
            logger.info("Pipeline [Run %d] Step 3: Creating AdSet: %s (budget: %s)", run_id, adset_name, formatted_budget)
            try:
                adset_id = await self.client.create_adset(
                    token=token,
                    ad_account_id=request.ad_account_id,
                    campaign_id=campaign_id,
                    name=adset_name,
                    daily_budget=formatted_budget,
                    targeting=DEFAULT_TARGETING,
                    status="PAUSED",
                )
                created_resources["adset_id"] = adset_id
                await self.run_repo.update_run(run_id=run_id, adset_id=adset_id)
            except (MetaApiError, Exception) as exc:
                err_msg = sanitize_meta_error(str(exc))
                await self.run_repo.update_run(
                    run_id=run_id,
                    status="partial_failure",
                    error_message=f"Lỗi tạo Ad Set: {err_msg}",
                )
                raise PartialCreationError(
                    message=f"Chiến dịch đã tạo một phần: Campaign ID ({campaign_id}) đã tạo nhưng Nhóm quảng cáo gặp lỗi: {err_msg}",
                    failed_step="create_adset",
                    created_resources=created_resources,
                    run_id=run_id,
                ) from exc

            # -------------------------------------------------------------
            # Step 4: Create Ad Creative
            # -------------------------------------------------------------
            creative_name = f"{request.campaign_name} - Creative"
            logger.info("Pipeline [Run %d] Step 4: Creating Creative: %s", run_id, creative_name)
            try:
                creative_id = await self.client.create_adcreative(
                    token=token,
                    ad_account_id=request.ad_account_id,
                    name=creative_name,
                    page_id=request.page_id,
                    link=request.destination_url,
                    message=request.primary_text,
                    headline=request.headline,
                    image_hash=image_hash,
                )
                created_resources["creative_id"] = creative_id
                await self.run_repo.update_run(run_id=run_id, creative_id=creative_id)
            except (MetaApiError, Exception) as exc:
                err_msg = sanitize_meta_error(str(exc))
                await self.run_repo.update_run(
                    run_id=run_id,
                    status="partial_failure",
                    error_message=f"Lỗi tạo Creative: {err_msg}",
                )
                raise PartialCreationError(
                    message=f"Chiến dịch đã tạo một phần: Campaign ID ({campaign_id}) và Ad Set ID ({adset_id}) đã được tạo nhưng Mẫu quảng cáo (Creative) gặp lỗi: {err_msg}",
                    failed_step="create_creative",
                    created_resources=created_resources,
                    run_id=run_id,
                ) from exc

            # -------------------------------------------------------------
            # Step 5: Create Ad
            # -------------------------------------------------------------
            ad_name = request.ad_name or f"{request.campaign_name} - Ad"
            logger.info("Pipeline [Run %d] Step 5: Creating Ad: %s", run_id, ad_name)
            try:
                ad_id = await self.client.create_ad(
                    token=token,
                    ad_account_id=request.ad_account_id,
                    name=ad_name,
                    adset_id=adset_id,
                    creative_id=creative_id,
                    status="PAUSED",
                )
                created_resources["ad_id"] = ad_id
                await self.run_repo.update_run(
                    run_id=run_id,
                    ad_id=ad_id,
                    status="success",
                )
            except (MetaApiError, Exception) as exc:
                err_msg = sanitize_meta_error(str(exc))
                await self.run_repo.update_run(
                    run_id=run_id,
                    status="partial_failure",
                    error_message=f"Lỗi tạo Ad: {err_msg}",
                )
                raise PartialCreationError(
                    message=f"Chiến dịch đã tạo một phần: Campaign ({campaign_id}), Ad Set ({adset_id}), Creative ({creative_id}) đã tạo nhưng Quảng cáo (Ad) gặp lỗi: {err_msg}",
                    failed_step="create_ad",
                    created_resources=created_resources,
                    run_id=run_id,
                ) from exc

            logger.info("Pipeline [Run %d] Completed successfully!", run_id)
            return {
                "run_id": run_id,
                "status": "success",
                "ad_account_id": request.ad_account_id,
                "page_id": request.page_id,
                "resources": created_resources,
                "configuration": {
                    "objective": "OUTCOME_TRAFFIC",
                    "status": "PAUSED",
                    "billing_event": "IMPRESSIONS",
                    "optimization_goal": "LINK_CLICKS",
                    "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
                    "targeting": DEFAULT_TARGETING,
                    "cta": "LEARN_MORE",
                },
            }


ad_service = AdCreationService()
