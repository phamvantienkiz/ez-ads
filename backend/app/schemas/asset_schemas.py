"""Meta Digital Assets (Ad Accounts and Pages) schemas."""


from app.schemas.common import BaseSchema


class AdAccountItem(BaseSchema):
    """Ad Account details returned from Meta API."""

    id: str
    account_id: str
    name: str
    currency: str
    account_status: int | None = None


class PageItem(BaseSchema):
    """Facebook Page details returned from Meta API."""

    id: str
    name: str
    category: str | None = None
