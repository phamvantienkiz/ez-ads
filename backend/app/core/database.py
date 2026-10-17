"""SQLite Database engine and auto-migration logic."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aiosqlite

from app.core.config import settings
from app.core.logging import logger

DDL_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS meta_sessions (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        access_token TEXT NOT NULL,
        token_type TEXT DEFAULT 'bearer',
        expires_at INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS ad_creation_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ad_account_id TEXT NOT NULL,
        page_id TEXT NOT NULL,
        campaign_id TEXT,
        adset_id TEXT,
        creative_id TEXT,
        ad_id TEXT,
        status TEXT NOT NULL CHECK (status IN ('pending', 'success', 'partial_failure', 'failed')),
        request_summary TEXT,
        error_message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_runs_created_at ON ad_creation_runs(created_at DESC);
    """,
]


@asynccontextmanager
async def get_db_connection(db_path: str | None = None) -> AsyncGenerator[aiosqlite.Connection, None]:
    """Provide an asynchronous SQLite connection with Row factory and WAL mode."""
    target_path = db_path or settings.DATABASE_PATH
    async with aiosqlite.connect(target_path) as db:
        db.row_factory = aiosqlite.Row
        await db.execute("PRAGMA journal_mode=WAL;")
        await db.execute("PRAGMA foreign_keys=ON;")
        yield db


async def init_db(db_path: str | None = None) -> None:
    """Execute initial DDL migrations if tables do not exist."""
    target_path = db_path or settings.DATABASE_PATH
    logger.info("Initializing SQLite database at: %s", target_path)
    async with get_db_connection(target_path) as db:
        for statement in DDL_STATEMENTS:
            await db.execute(statement)
        await db.commit()
    logger.info("Database initialized successfully.")
