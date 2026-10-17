"""Health check and middleware smoke tests."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_endpoints(client: AsyncClient) -> None:
    """Verify health endpoints under /, /api/v1, and /api aliases."""
    for path in ["/health", "/api/v1/health", "/api/health"]:
        response = await client.get(path)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert data["statusCode"] == 200
        assert data["data"]["status"] == "healthy"
        assert data["data"]["database"] == "connected"
        assert "requestId" in data["meta"]

        # Middleware headers check
        assert "X-Request-ID" in response.headers
        assert "X-Process-Time" in response.headers
