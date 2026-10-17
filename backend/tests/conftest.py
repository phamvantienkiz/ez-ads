"""Pytest configuration and fixtures for backend tests."""

import os
import tempfile
from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.core.database import init_db
from app.main import app
from app.repositories.run_repository import run_repo
from app.repositories.session_repository import session_repo


@pytest.fixture(autouse=True)
async def setup_test_db() -> AsyncGenerator[str, None]:
    """Create a temporary SQLite database for each test run and clean up afterwards."""
    temp_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(temp_dir, "test_baha.db")

    # Override settings and repositories
    original_db = settings.DATABASE_PATH
    settings.DATABASE_PATH = test_db_path
    session_repo.db_path = test_db_path
    run_repo.db_path = test_db_path

    # Initialize tables
    await init_db(test_db_path)

    yield test_db_path

    # Restore
    settings.DATABASE_PATH = original_db
    session_repo.db_path = original_db
    run_repo.db_path = original_db

    # Clean up test database files
    for ext in ["", "-wal", "-shm"]:
        file_to_remove = f"{test_db_path}{ext}"
        if os.path.exists(file_to_remove):
            try:
                os.remove(file_to_remove)
            except OSError:
                pass


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Provide an asynchronous HTTP test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
