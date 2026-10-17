"""Session repository managing the single active Meta session record (id=1)."""

import time
from typing import Any

from app.core.database import get_db_connection


class SessionRepository:
    """SQLite repository for meta_sessions table."""

    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path

    async def get_session(self) -> dict[str, Any] | None:
        """Retrieve the current active Meta session record if present."""
        async with get_db_connection(self.db_path) as db, db.execute(
            "SELECT id, access_token, token_type, expires_at, created_at, updated_at "
            "FROM meta_sessions WHERE id = 1"
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return dict(row)
            return None

    async def get_access_token(self) -> str | None:
        """Retrieve the access token if session exists and is not expired."""
        session = await self.get_session()
        if not session:
            return None

        expires_at = session.get("expires_at")
        if expires_at and expires_at < int(time.time()):
            return None

        return session.get("access_token")

    async def save_session(
        self,
        access_token: str,
        token_type: str = "bearer",
        expires_in: int | None = None,
    ) -> dict[str, Any]:
        """Insert or replace the single session record with id=1."""
        expires_at = int(time.time()) + expires_in if expires_in else None

        async with get_db_connection(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO meta_sessions (id, access_token, token_type, expires_at, updated_at)
                VALUES (1, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(id) DO UPDATE SET
                    access_token = excluded.access_token,
                    token_type = excluded.token_type,
                    expires_at = excluded.expires_at,
                    updated_at = CURRENT_TIMESTAMP;
                """,
                (access_token, token_type, expires_at),
            )
            await db.commit()

        session = await self.get_session()
        return session or {}

    async def delete_session(self) -> bool:
        """Remove the current session, resetting connection status."""
        async with get_db_connection(self.db_path) as db:
            cursor = await db.execute("DELETE FROM meta_sessions WHERE id = 1")
            await db.commit()
            return cursor.rowcount > 0


session_repo = SessionRepository()
