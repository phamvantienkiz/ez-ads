"""OAuth and Session schemas."""


from app.schemas.common import BaseSchema


class MetaConnectData(BaseSchema):
    """Payload returned when initializing OAuth connect."""

    auth_url: str


class MetaStatusData(BaseSchema):
    """Payload representing Meta connection status."""

    connected: bool
    has_token: bool
    token_type: str | None = None
    updated_at: str | None = None


class MetaDisconnectData(BaseSchema):
    """Payload returned when disconnecting Meta."""

    connected: bool = False
