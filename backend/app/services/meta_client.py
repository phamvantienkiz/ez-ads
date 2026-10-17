"""HTTP Client service for Meta Marketing API (v20.0) using httpx.AsyncClient."""

from typing import Any

import httpx

from app.core.config import settings
from app.core.security import sanitize_meta_error


class MetaApiError(Exception):
    """Exception raised when Meta Marketing API returns an error."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        raw_error: dict[str, Any] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.raw_error = raw_error or {}
        super().__init__(self.message)


class MetaTimeoutError(MetaApiError):
    """Exception raised when request to Meta Marketing API times out."""

    def __init__(self, message: str = "Kết nối đến Meta API quá thời gian chờ (Timeout)") -> None:
        super().__init__(
            code="META_API_TIMEOUT",
            message=message,
            status_code=504,
        )


class MetaClientService:
    """Async HTTP Client interfacing with Meta Graph API & Marketing API v20.0."""

    def __init__(self, timeout: float | None = None) -> None:
        self.base_url = settings.META_GRAPH_BASE_URL.rstrip("/")
        self.timeout = timeout or settings.META_API_TIMEOUT

    def _normalize_act_id(self, ad_account_id: str) -> str:
        """Ensure ad account ID has 'act_' prefix."""
        clean_id = ad_account_id.strip()
        if not clean_id.startswith("act_"):
            return f"act_{clean_id}"
        return clean_id

    def _parse_error(self, response: httpx.Response) -> MetaApiError:
        """Extract and sanitize Meta API error."""
        try:
            data = response.json()
            err_dict = data.get("error", {})
            raw_msg = (
                err_dict.get("error_user_msg")
                or err_dict.get("message")
                or response.text
            )
            meta_code = str(err_dict.get("code", "META_API_ERROR"))
        except Exception:
            raw_msg = response.text or "Unknown Meta API error"
            meta_code = "META_API_ERROR"

        clean_msg = sanitize_meta_error(raw_msg)
        return MetaApiError(
            code=f"META_ERR_{meta_code}",
            message=clean_msg,
            status_code=response.status_code,
            raw_error={"status_code": response.status_code, "detail": clean_msg},
        )

    async def exchange_oauth_code(self, code: str) -> dict[str, Any]:
        """Exchange authorization code for a User Access Token."""
        url = f"{self.base_url}/oauth/access_token"
        params = {
            "client_id": settings.META_APP_ID,
            "client_secret": settings.META_APP_SECRET,
            "redirect_uri": settings.META_REDIRECT_URI,
            "code": code,
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(url, params=params)
                if not resp.is_success:
                    raise self._parse_error(resp)
                return resp.json()
        except httpx.TimeoutException as exc:
            raise MetaTimeoutError() from exc

    async def get_ad_accounts(
        self,
        token: str,
        fields: str = "id,name,account_id,currency,account_status",
    ) -> list[dict[str, Any]]:
        """Fetch list of Ad Accounts the user has access to."""
        url = f"{self.base_url}/me/adaccounts"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"fields": fields, "limit": 100}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(url, headers=headers, params=params)
                if not resp.is_success:
                    raise self._parse_error(resp)

                data = resp.json().get("data", [])
                accounts = []
                for acc in data:
                    raw_id = acc.get("id", "")
                    clean_account_id = acc.get("account_id") or raw_id.replace("act_", "")
                    accounts.append({
                        "id": raw_id if raw_id.startswith("act_") else f"act_{raw_id}",
                        "account_id": clean_account_id,
                        "name": acc.get("name", "Unnamed Account"),
                        "currency": acc.get("currency", "VND"),
                        "account_status": acc.get("account_status", 1),
                    })
                return accounts
        except httpx.TimeoutException as exc:
            raise MetaTimeoutError() from exc

    async def get_pages(
        self,
        token: str,
        fields: str = "id,name,category",
    ) -> list[dict[str, Any]]:
        """Fetch list of Facebook Pages managed by the user."""
        url = f"{self.base_url}/me/accounts"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"fields": fields, "limit": 100}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(url, headers=headers, params=params)
                if not resp.is_success:
                    raise self._parse_error(resp)

                data = resp.json().get("data", [])
                pages = []
                for p in data:
                    pages.append({
                        "id": str(p.get("id")),
                        "name": p.get("name", "Unnamed Page"),
                        "category": p.get("category"),
                    })
                return pages
        except httpx.TimeoutException as exc:
            raise MetaTimeoutError() from exc

    async def get_campaigns(
        self,
        token: str,
        ad_account_id: str,
        limit: int = 25,
        status: str | None = None,
    ) -> list[dict[str, Any]]:
        """Fetch list of actual campaigns under the specified Ad Account."""
        act_id = self._normalize_act_id(ad_account_id)
        url = f"{self.base_url}/{act_id}/campaigns"
        headers = {"Authorization": f"Bearer {token}"}
        params: dict[str, Any] = {
            "fields": "id,name,objective,status,created_time",
            "limit": limit,
        }
        if status:
            params["filtering"] = f"[{{'field':'effective_status','operator':'IN','value':['{status.upper()}']}}]"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(url, headers=headers, params=params)
                if not resp.is_success:
                    raise self._parse_error(resp)

                data = resp.json().get("data", [])
                campaigns = []
                for cmp in data:
                    campaigns.append({
                        "id": str(cmp.get("id")),
                        "name": cmp.get("name", "Unnamed Campaign"),
                        "objective": cmp.get("objective", "OUTCOME_TRAFFIC"),
                        "status": cmp.get("status", "PAUSED"),
                        "created_time": cmp.get("created_time"),
                    })
                return campaigns
        except httpx.TimeoutException as exc:
            raise MetaTimeoutError() from exc

    async def upload_ad_image(
        self,
        token: str,
        ad_account_id: str,
        image_url: str,
    ) -> str:
        """Step 1: Upload image by public URL to get image_hash."""
        act_id = self._normalize_act_id(ad_account_id)
        url = f"{self.base_url}/{act_id}/adimages"
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"url": image_url}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(url, headers=headers, data=payload)
                if not resp.is_success:
                    raise self._parse_error(resp)

                data = resp.json()
                images = data.get("images", {})
                # Look for image hash by url or pick first item
                if image_url in images and "hash" in images[image_url]:
                    return images[image_url]["hash"]
                for img_info in images.values():
                    if isinstance(img_info, dict) and "hash" in img_info:
                        return img_info["hash"]

                raise MetaApiError(
                    code="META_IMAGE_HASH_FAILED",
                    message="Không tìm thấy hash của hình ảnh trong phản hồi từ Meta API",
                )
        except httpx.TimeoutException as exc:
            raise MetaTimeoutError() from exc

    async def create_campaign(
        self,
        token: str,
        ad_account_id: str,
        name: str,
        objective: str = "OUTCOME_TRAFFIC",
        status: str = "PAUSED",
    ) -> str:
        """Step 2: Create a Campaign."""
        act_id = self._normalize_act_id(ad_account_id)
        url = f"{self.base_url}/{act_id}/campaigns"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "name": name,
            "objective": objective,
            "status": status,
            "special_ad_categories": [],
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(url, headers=headers, json=payload)
                if not resp.is_success:
                    raise self._parse_error(resp)
                campaign_id = resp.json().get("id")
                if not campaign_id:
                    raise MetaApiError(
                        code="META_CAMPAIGN_CREATE_FAILED",
                        message="Meta không trả về campaign_id",
                    )
                return str(campaign_id)
        except httpx.TimeoutException as exc:
            raise MetaTimeoutError() from exc

    async def create_adset(
        self,
        token: str,
        ad_account_id: str,
        campaign_id: str,
        name: str,
        daily_budget: str,
        targeting: dict[str, Any],
        status: str = "PAUSED",
    ) -> str:
        """Step 3: Create an Ad Set with formatted daily_budget."""
        act_id = self._normalize_act_id(ad_account_id)
        url = f"{self.base_url}/{act_id}/adsets"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "name": name,
            "campaign_id": campaign_id,
            "daily_budget": daily_budget,
            "billing_event": "IMPRESSIONS",
            "optimization_goal": "LINK_CLICKS",
            "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
            "targeting": targeting,
            "status": status,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(url, headers=headers, json=payload)
                if not resp.is_success:
                    raise self._parse_error(resp)
                adset_id = resp.json().get("id")
                if not adset_id:
                    raise MetaApiError(
                        code="META_ADSET_CREATE_FAILED",
                        message="Meta không trả về adset_id",
                    )
                return str(adset_id)
        except httpx.TimeoutException as exc:
            raise MetaTimeoutError() from exc

    async def create_adcreative(
        self,
        token: str,
        ad_account_id: str,
        name: str,
        page_id: str,
        link: str,
        message: str,
        headline: str,
        image_hash: str,
    ) -> str:
        """Step 4: Create an Ad Creative linking page, image_hash, link, and CTA."""
        act_id = self._normalize_act_id(ad_account_id)
        url = f"{self.base_url}/{act_id}/adcreatives"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "name": name,
            "object_story_spec": {
                "page_id": page_id,
                "link_data": {
                    "link": link,
                    "message": message,
                    "name": headline,
                    "image_hash": image_hash,
                    "call_to_action": {
                        "type": "LEARN_MORE"
                    },
                },
            },
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(url, headers=headers, json=payload)
                if not resp.is_success:
                    raise self._parse_error(resp)
                creative_id = resp.json().get("id")
                if not creative_id:
                    raise MetaApiError(
                        code="META_CREATIVE_CREATE_FAILED",
                        message="Meta không trả về creative_id",
                    )
                return str(creative_id)
        except httpx.TimeoutException as exc:
            raise MetaTimeoutError() from exc

    async def create_ad(
        self,
        token: str,
        ad_account_id: str,
        name: str,
        adset_id: str,
        creative_id: str,
        status: str = "PAUSED",
    ) -> str:
        """Step 5: Create the final Ad entity."""
        act_id = self._normalize_act_id(ad_account_id)
        url = f"{self.base_url}/{act_id}/ads"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        payload = {
            "name": name,
            "adset_id": adset_id,
            "creative": {
                "creative_id": creative_id,
            },
            "status": status,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(url, headers=headers, json=payload)
                if not resp.is_success:
                    raise self._parse_error(resp)
                ad_id = resp.json().get("id")
                if not ad_id:
                    raise MetaApiError(
                        code="META_AD_CREATE_FAILED",
                        message="Meta không trả về ad_id",
                    )
                return str(ad_id)
        except httpx.TimeoutException as exc:
            raise MetaTimeoutError() from exc


meta_client = MetaClientService()
