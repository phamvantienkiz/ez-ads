"""Integration tests for Meta OAuth 2.0 and session management (US-001)."""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from app.core.security import state_manager
from app.repositories.session_repository import session_repo


@pytest.mark.asyncio
async def test_meta_connect_generates_oauth_url(client: AsyncClient) -> None:
    """AC1: GET /api/v1/meta/connect returns valid Facebook OAuth URL."""
    response = await client.get("/api/v1/meta/connect")
    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert "authUrl" in body["data"]

    auth_url = body["data"]["authUrl"]
    assert "https://www.facebook.com/v20.0/dialog/oauth" in auth_url
    assert "ads_management" in auth_url
    assert "state=baha_" in auth_url


@pytest.mark.asyncio
async def test_meta_callback_user_denied(client: AsyncClient) -> None:
    """AC3: Negative path - User canceled or denied permission on Facebook."""
    response = await client.get("/api/v1/meta/callback?error=access_denied", follow_redirects=False)
    assert response.status_code == 302
    assert "error=access_denied" in response.headers["location"]

    # Verify no garbage session was saved
    session = await session_repo.get_session()
    assert session is None


@pytest.mark.asyncio
async def test_meta_callback_csrf_mismatch(client: AsyncClient) -> None:
    """AC4: Security - CSRF State mismatch or missing state."""
    response = await client.get("/api/v1/meta/callback?code=mock_code&state=fake_state_123")
    assert response.status_code == 400

    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "OAUTH_CSRF_MISMATCH"


@pytest.mark.asyncio
async def test_meta_callback_happy_path(client: AsyncClient) -> None:
    """AC1: Happy path - Exchange authorization code for token, save session (id=1)."""
    # Pre-generate valid state
    state = state_manager.generate_state()

    mock_token_data = {
        "access_token": "mock_facebook_user_access_token_123",
        "token_type": "bearer",
        "expires_in": 5184000,
    }

    with patch("app.services.meta_client.MetaClientService.exchange_oauth_code", new_callable=AsyncMock) as mock_exchange:
        mock_exchange.return_value = mock_token_data

        response = await client.get(
            f"/api/v1/meta/callback?code=valid_auth_code&state={state}",
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert "connected=true" in response.headers["location"]

    # Verify session is persisted in SQLite with id=1
    session = await session_repo.get_session()
    assert session is not None
    assert session["id"] == 1
    assert session["access_token"] == "mock_facebook_user_access_token_123"

    # Test status endpoint confirms connected
    status_resp = await client.get("/api/v1/meta/status")
    assert status_resp.status_code == 200
    status_body = status_resp.json()
    assert status_body["data"]["connected"] is True
    assert status_body["data"]["hasToken"] is True


@pytest.mark.asyncio
async def test_meta_disconnect_flow(client: AsyncClient) -> None:
    """Verify session disconnection resets system to disconnected."""
    # First save a dummy session
    await session_repo.save_session("dummy_token")

    status_before = await client.get("/api/v1/meta/status")
    assert status_before.json()["data"]["connected"] is True

    # Call disconnect
    disc_resp = await client.post("/api/v1/meta/disconnect")
    assert disc_resp.status_code == 200
    assert disc_resp.json()["data"]["connected"] is False

    # Check status again
    status_after = await client.get("/api/v1/meta/status")
    assert status_after.json()["data"]["connected"] is False
