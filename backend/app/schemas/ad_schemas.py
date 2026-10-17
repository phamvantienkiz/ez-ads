"""Ad creation, campaigns, and execution run schemas."""

from typing import Any

from pydantic import Field, field_validator

from app.schemas.common import BaseSchema


class AdCreationRequest(BaseSchema):
    """Payload to initiate the 5-step sequential ad creation pipeline."""

    ad_account_id: str = Field(..., description="Meta Ad Account ID (e.g. act_123456789)")
    page_id: str = Field(..., description="Facebook Fanpage ID")
    campaign_name: str = Field(..., min_length=3, max_length=255, description="Name of the Campaign")
    budget_amount: float = Field(..., gt=0, description="Daily budget amount (> 0)")
    primary_text: str = Field(..., min_length=1, description="Primary ad copy text")
    headline: str = Field(..., min_length=1, description="Ad link headline")
    destination_url: str = Field(..., description="Product landing page URL")
    image_url: str = Field(..., description="Publicly accessible product image URL")
    adset_name: str | None = Field(None, description="Optional custom name for Ad Set")
    ad_name: str | None = Field(None, description="Optional custom name for Ad")

    @field_validator("destination_url", "image_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate URL scheme."""
        v_clean = v.strip()
        if not v_clean.startswith(("http://", "https://")):
            raise ValueError("URL phải bắt đầu bằng http:// hoặc https://")
        return v_clean


class AdResources(BaseSchema):
    """Resource IDs returned during or after the pipeline execution."""

    image_hash: str | None = None
    campaign_id: str | None = None
    adset_id: str | None = None
    creative_id: str | None = None
    ad_id: str | None = None


class AdCreationData(BaseSchema):
    """Data payload for ad creation success or partial failure."""

    run_id: int
    status: str
    ad_account_id: str
    page_id: str
    resources: AdResources
    configuration: dict[str, Any] | None = None


class PartialFailureData(BaseSchema):
    """Data payload returned in case of partial creation failure."""

    run_id: int
    status: str = "partial_failure"
    created_resources: AdResources


class CampaignItem(BaseSchema):
    """Campaign representation fetched from Meta Marketing API."""

    id: str
    name: str
    objective: str
    status: str
    created_time: str | None = None


class AdRunItem(BaseSchema):
    """Historical run item representation stored in ad_creation_runs."""

    id: int
    status: str
    ad_account_id: str
    page_id: str
    campaign_id: str | None = None
    adset_id: str | None = None
    creative_id: str | None = None
    ad_id: str | None = None
    request_summary: str | None = None
    error_message: str | None = None
    created_at: str | None = None
