"""Integration tests for Meta digital assets: Ad Accounts & Pages (US-002, US-003)."""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from app.repositories.session_repository import session_repo


@pytest.mark.asyncio
async def test_get_ad_accounts_unauthorized_without_session(client: AsyncClient) -> None:
    """Verify 401 when no session exists."""
    response = await client.get("/api/v1/meta/ad-accounts")
    assert response.status_code == 401

    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "SESSION_NOT_FOUND"


@pytest.mark.asyncio
async def test_get_ad_accounts_success(client: AsyncClient) -> None:
    """AC1: Fetch ad accounts with valid active session."""
    await session_repo.save_session("valid_token_123")

    mock_accounts = [
        {
            "id": "act_123456789",
            "account_id": "123456789",
            "name": "BAHA Commerce Store",
            "currency": "VND",
            "account_status": 1,
        },
        {
            "id": "act_987654321",
            "account_id": "987654321",
            "name": "BAHA Global Test",
            "currency": "USD",
            "account_status": 1,
        },
    ]

    with patch("app.services.meta_client.MetaClientService.get_ad_accounts", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_accounts

        response = await client.get("/api/v1/meta/ad-accounts")
        assert response.status_code == 200

        body = response.json()
        assert body["success"] is True
        assert len(body["data"]) == 2
        assert body["data"][0]["id"] == "act_123456789"
        assert body["data"][0]["currency"] == "VND"
        assert body["meta"]["total"] == 2


@pytest.mark.asyncio
async def test_get_pages_success(client: AsyncClient) -> None:
    """AC1: Fetch managed Facebook pages with valid session."""
    await session_repo.save_session("valid_token_123")

    mock_pages = [
        {
            "id": "100200300400",
            "name": "BAHA Fashion Brand",
            "category": "Clothing (Brand)",
        }
    ]

    with patch("app.services.meta_client.MetaClientService.get_pages", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_pages

        response = await client.get("/api/v1/meta/pages")
        assert response.status_code == 200

        body = response.json()
        assert body["success"] is True
        assert len(body["data"]) == 1
        assert body["data"][0]["id"] == "100200300400"
        assert body["data"][0]["name"] == "BAHA Fashion Brand"
