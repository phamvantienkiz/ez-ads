"""Common schema components and Consistent Response Envelope (Pattern 7)."""

from datetime import UTC, datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema configured for camelCase and snake_case interop."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
        from_attributes=True,
    )


class ResponseMeta(BaseSchema):
    """Response metadata included in all envelopes."""

    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
    request_id: str = "req_default"
    total: int | None = None
    count: int | None = None
    limit: int | None = None
    ad_account_id: str | None = None


class ErrorDetail(BaseSchema):
    """Structured error detail representation."""

    code: str
    message: str | None = None
    failed_step: str | None = None
    details: list[Any] = Field(default_factory=list)


class SuccessResponse(BaseSchema, Generic[T]):
    """Standard success response envelope."""

    success: bool = True
    status_code: int = 200
    message: str = "Thao tác thành công"
    data: T
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


class ErrorResponse(BaseSchema):
    """Standard error response envelope."""

    success: bool = False
    status_code: int = 400
    message: str = "Yêu cầu không hợp lệ"
    error: ErrorDetail
    data: Any | None = None
    meta: ResponseMeta = Field(default_factory=ResponseMeta)
