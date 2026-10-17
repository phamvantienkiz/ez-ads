"""Integration tests for campaigns and 5-step ad creation pipeline (US-004, US-006, US-007, US-008)."""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from app.repositories.run_repository import run_repo
from app.repositories.session_repository import session_repo
from app.services.meta_client import MetaApiError


@pytest.mark.asyncio
async def test_get_campaigns_success(client: AsyncClient) -> None:
    """US-007 AC1: Query actual campaigns under Ad Account."""
    await session_repo.save_session("valid_token_123")

    mock_campaigns = [
        {
            "id": "120210000000001",
            "name": "BAHA Traffic Demo Campaign",
            "objective": "OUTCOME_TRAFFIC",
            "status": "PAUSED",
            "created_time": "2026-10-17T14:45:00+0700",
        }
    ]

    with patch("app.services.meta_client.MetaClientService.get_campaigns", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_campaigns

        response = await client.get("/api/v1/campaigns?ad_account_id=act_123456789")
        assert response.status_code == 200

        body = response.json()
        assert body["success"] is True
        assert len(body["data"]) == 1
        assert body["data"][0]["id"] == "120210000000001"
        assert body["meta"]["count"] == 1


@pytest.mark.asyncio
async def test_create_ad_validation_errors(client: AsyncClient) -> None:
    """US-004 AC3, AC4: Validation checks for invalid URL and negative budget."""
    await session_repo.save_session("valid_token_123")

    # Invalid URL scheme
    invalid_payload = {
        "adAccountId": "act_123456789",
        "pageId": "100200300400",
        "campaignName": "Polo Campaign",
        "budgetAmount": -100,  # Negative budget
        "primaryText": "Test description",
        "headline": "Test Headline",
        "destinationUrl": "ftp://invalid-url.com",  # Invalid protocol
        "imageUrl": "not_a_valid_url",
    }

    response = await client.post("/api/v1/ads", json=invalid_payload)
    assert response.status_code == 422
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_create_ad_full_pipeline_success(client: AsyncClient) -> None:
    """US-006 AC1: Happy path - 5 API calls in order, 201 Created, SQLite status='success'."""
    await session_repo.save_session("valid_token_123")

    payload = {
        "adAccountId": "act_123456789",
        "pageId": "100200300400",
        "campaignName": "BAHA Polo Shirt Traffic Campaign",
        "budgetAmount": 50000,
        "primaryText": "Áo Polo cao cấp từ BAHA.",
        "headline": "Áo Polo Nam Classic",
        "destinationUrl": "https://baha.vn/products/polo",
        "imageUrl": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800",
    }

    with patch("app.services.meta_client.MetaClientService.upload_ad_image", new_callable=AsyncMock) as m_img, \
         patch("app.services.meta_client.MetaClientService.create_campaign", new_callable=AsyncMock) as m_cmp, \
         patch("app.services.meta_client.MetaClientService.create_adset", new_callable=AsyncMock) as m_adset, \
         patch("app.services.meta_client.MetaClientService.create_adcreative", new_callable=AsyncMock) as m_cre, \
         patch("app.services.meta_client.MetaClientService.create_ad", new_callable=AsyncMock) as m_ad:

        m_img.return_value = "img_hash_987654321"
        m_cmp.return_value = "cmp_1001"
        m_adset.return_value = "adset_2002"
        m_cre.return_value = "cre_3003"
        m_ad.return_value = "ad_4004"

        response = await client.post("/api/v1/ads", json=payload)
        assert response.status_code == 201

        body = response.json()
        assert body["success"] is True
        assert body["data"]["status"] == "success"
        resources = body["data"]["resources"]
        assert resources["imageHash"] == "img_hash_987654321"
        assert resources["campaignId"] == "cmp_1001"
        assert resources["adsetId"] == "adset_2002"
        assert resources["creativeId"] == "cre_3003"
        assert resources["adId"] == "ad_4004"

        # Verify DB record
        run_id = body["data"]["runId"]
        saved_run = await run_repo.get_run_by_id(run_id)
        assert saved_run is not None
        assert saved_run["status"] == "success"
        assert saved_run["ad_id"] == "ad_4004"


@pytest.mark.asyncio
async def test_create_ad_image_hash_failure(client: AsyncClient) -> None:
    """US-006 AC2: Negative path - Image upload failure stops pipeline immediately."""
    await session_repo.save_session("valid_token_123")

    payload = {
        "adAccountId": "act_123456789",
        "pageId": "100200300400",
        "campaignName": "BAHA Fail Image Campaign",
        "budgetAmount": 50000,
        "primaryText": "Primary text",
        "headline": "Headline",
        "destinationUrl": "https://baha.vn/products/fail",
        "imageUrl": "https://baha.vn/broken-image.jpg",
    }

    with patch("app.services.meta_client.MetaClientService.upload_ad_image", new_callable=AsyncMock) as m_img:
        m_img.side_effect = MetaApiError(code="META_IMAGE_HASH_FAILED", message="Failed to load image from URL")

        response = await client.post("/api/v1/ads", json=payload)
        assert response.status_code == 400

        body = response.json()
        assert body["success"] is False
        assert body["error"]["code"] == "META_IMAGE_HASH_FAILED"

        # Verify SQLite has run marked as failed
        latest_run = await run_repo.get_latest_run()
        assert latest_run is not None
        assert latest_run["status"] == "failed"
        assert latest_run["campaign_id"] is None


@pytest.mark.asyncio
async def test_create_ad_partial_failure_handling(client: AsyncClient) -> None:
    """US-006 AC3: Partial failure - Campaign and AdSet succeed, Creative fails."""
    await session_repo.save_session("valid_token_123")

    payload = {
        "adAccountId": "act_123456789",
        "pageId": "100200300400",
        "campaignName": "BAHA Partial Failure Campaign",
        "budgetAmount": 50000,
        "primaryText": "Primary text",
        "headline": "Headline",
        "destinationUrl": "https://baha.vn/products/blocked",
        "imageUrl": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800",
    }

    with patch("app.services.meta_client.MetaClientService.upload_ad_image", new_callable=AsyncMock) as m_img, \
         patch("app.services.meta_client.MetaClientService.create_campaign", new_callable=AsyncMock) as m_cmp, \
         patch("app.services.meta_client.MetaClientService.create_adset", new_callable=AsyncMock) as m_adset, \
         patch("app.services.meta_client.MetaClientService.create_adcreative", new_callable=AsyncMock) as m_cre:

        m_img.return_value = "img_hash_partial"
        m_cmp.return_value = "cmp_partial_1"
        m_adset.return_value = "adset_partial_2"
        # Step 4 raises an error
        m_cre.side_effect = MetaApiError(code="META_CREATIVE_ERROR", message="Destination URL violates community standards")

        response = await client.post("/api/v1/ads", json=payload)
        assert response.status_code == 400

        body = response.json()
        assert body["success"] is False
        assert body["error"]["code"] == "PARTIAL_CREATION_FAILURE"
        assert body["error"]["failedStep"] == "create_creative"

        # Resources created before failure are preserved
        created = body["data"]["createdResources"]
        assert created["campaignId"] == "cmp_partial_1"
        assert created["adsetId"] == "adset_partial_2"
        assert created["creativeId"] is None
        assert created["adId"] is None

        # Verify DB record
        latest_run = await run_repo.get_latest_run()
        assert latest_run is not None
        assert latest_run["status"] == "partial_failure"
        assert latest_run["campaign_id"] == "cmp_partial_1"
        assert latest_run["adset_id"] == "adset_partial_2"


@pytest.mark.asyncio
async def test_get_run_endpoints_and_aliases(client: AsyncClient) -> None:
    """US-008 AC1, AC2: Latest run and /ads/{id} alias test."""
    # When no run exists
    empty_resp = await client.get("/api/v1/ads/runs/latest")
    assert empty_resp.status_code == 200
    assert empty_resp.json()["data"] is None

    # Insert a run
    run_id = await run_repo.create_run(
        ad_account_id="act_12345",
        page_id="998877",
        status="success",
    )
    await run_repo.update_run(run_id, campaign_id="cmp_test", ad_id="ad_test")

    # Get latest
    latest_resp = await client.get("/api/v1/ads/runs/latest")
    assert latest_resp.status_code == 200
    assert latest_resp.json()["data"]["id"] == run_id

    # Get by id via standard route
    id_resp = await client.get(f"/api/v1/ads/runs/{run_id}")
    assert id_resp.status_code == 200
    assert id_resp.json()["data"]["campaignId"] == "cmp_test"

    # Get by id via alias route /api/ads/{id}
    alias_resp = await client.get(f"/api/ads/{run_id}")
    assert alias_resp.status_code == 200
    assert alias_resp.json()["data"]["campaignId"] == "cmp_test"
