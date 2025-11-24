from datetime import datetime
from typing import Any

from pydantic import Field

from src.domain.message.value_objects.sender_type import SenderTypeEnum
from src.presentation.api.schemas.base_schema import BaseSchemaModel


class MessageBase(BaseSchemaModel):
    """Base message model."""

    content: str = Field(..., description="Message content")
    chat_id: str = Field(..., description="Chat ID to which the message belongs")


class MessageCreate(MessageBase):
    """Message creation request model."""

    sender_id: str = Field(..., description="Sender ID")
    metadata: dict[str, Any] | None = Field(None, description="Additional message information")
    book_id: str | None = Field(None, description="Book ID to which the message belongs")


class MessageUpdate(BaseSchemaModel):
    """Message update request model."""

    content: str | None = Field(None, description="Message content")
    sender_type: SenderTypeEnum | None = Field(None, description="Sender type")
    metadata: dict[str, Any] | None = Field(None, description="Additional message information")


class MessageBulkDelete(BaseSchemaModel):
    """Multiple message deletion request model."""

    message_ids: list[str] = Field(..., description="List of message IDs to delete")


class MessageResponse(BaseSchemaModel):
    """Message response model."""

    id: str
    content: str
    sender_id: str
    sender_type: SenderTypeEnum
    chat_id: str
    created_at: datetime
    metadata: dict[str, Any] | None = None


class MessageListResponse(BaseSchemaModel):
    """Message list response model."""

    messages: list[MessageResponse]
    total: int


class FailedMessageIdsResponse(BaseSchemaModel):
    """Failed message ID response model."""

    failed_ids: list[str]
