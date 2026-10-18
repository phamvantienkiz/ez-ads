"""OAuth and Session schemas."""


from app.schemas.common import BaseSchema


class MetaConnectData(BaseSchema):
    """Payload returned when initializing OAuth connect."""

    auth_url: str
    app_id_configured: bool = True
    current_app_id: str | None = None


class MetaTokenCallbackRequest(BaseSchema):
    """Payload for OAuth Implicit Flow (response_type=token) or direct token save."""

    access_token: str
    state: str | None = None
    token_type: str = "bearer"
    expires_in: int | None = None


class MetaStatusData(BaseSchema):
    """Payload representing Meta connection status."""

    connected: bool
    has_token: bool
    token_type: str | None = None
    updated_at: str | None = None
    app_id_configured: bool = True
    current_app_id: str | None = None


class MetaDisconnectData(BaseSchema):
    """Payload returned when disconnecting Meta."""

    connected: bool = False
