"""Run repository for recording ad creation pipeline execution history."""

from typing import Any

from app.core.database import get_db_connection


class RunRepository:
    """SQLite repository for ad_creation_runs table."""

    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path

    async def create_run(
        self,
        ad_account_id: str,
        page_id: str,
        status: str = "pending",
        request_summary: str | None = None,
    ) -> int:
        """Create a new run record with status 'pending'."""
        async with get_db_connection(self.db_path) as db:
            cursor = await db.execute(
                """
                INSERT INTO ad_creation_runs (
                    ad_account_id, page_id, status, request_summary
                ) VALUES (?, ?, ?, ?)
                """,
                (ad_account_id, page_id, status, request_summary),
            )
            await db.commit()
            return cursor.lastrowid or 0

    async def update_run(
        self,
        run_id: int,
        status: str | None = None,
        campaign_id: str | None = None,
        adset_id: str | None = None,
        creative_id: str | None = None,
        ad_id: str | None = None,
        error_message: str | None = None,
    ) -> None:
        """Update intermediate or final resource IDs and status of a run."""
        updates = []
        params = []

        if status is not None:
            updates.append("status = ?")
            params.append(status)
        if campaign_id is not None:
            updates.append("campaign_id = ?")
            params.append(campaign_id)
        if adset_id is not None:
            updates.append("adset_id = ?")
            params.append(adset_id)
        if creative_id is not None:
            updates.append("creative_id = ?")
            params.append(creative_id)
        if ad_id is not None:
            updates.append("ad_id = ?")
            params.append(ad_id)
        if error_message is not None:
            updates.append("error_message = ?")
            params.append(error_message)

        if not updates:
            return

        params.append(run_id)
        query = f"UPDATE ad_creation_runs SET {', '.join(updates)} WHERE id = ?"

        async with get_db_connection(self.db_path) as db:
            await db.execute(query, tuple(params))
            await db.commit()

    async def get_latest_run(self) -> dict[str, Any] | None:
        """Retrieve the most recent ad creation run."""
        async with get_db_connection(self.db_path) as db, db.execute(
            """
                SELECT id, ad_account_id, page_id, campaign_id, adset_id,
                       creative_id, ad_id, status, request_summary, error_message, created_at
                FROM ad_creation_runs
                ORDER BY created_at DESC, id DESC
                LIMIT 1
                """
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return dict(row)
            return None

    async def get_run_by_id(self, run_id: int) -> dict[str, Any] | None:
        """Retrieve a specific run by ID."""
        async with get_db_connection(self.db_path) as db, db.execute(
            """
                SELECT id, ad_account_id, page_id, campaign_id, adset_id,
                       creative_id, ad_id, status, request_summary, error_message, created_at
                FROM ad_creation_runs
                WHERE id = ?
                """,
            (run_id,),
        ) as cursor:
            row = await cursor.fetchone()
            if row:
                return dict(row)
            return None


run_repo = RunRepository()
