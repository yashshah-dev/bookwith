from datetime import datetime

from pydantic import Field

from src.presentation.api.schemas.base_schema import BaseSchemaModel


class ChatCreateRequest(BaseSchemaModel):
    user_id: str = Field(..., description="User ID")
    title: str | None = Field(None, description="Chat title", max_length=255)
    book_id: str | None = Field(None, description="Related book ID")


class ChatUpdateTitleRequest(BaseSchemaModel):
    title: str = Field(..., description="Chat title to update", max_length=255)


class ChatResponse(BaseSchemaModel):
    id: str = Field(..., description="Chat ID")
    user_id: str = Field(..., description="User ID")
    title: str = Field(..., description="Chat title")
    book_id: str | None = Field(None, description="Related book ID")
    created_at: datetime = Field(..., description="Creation date and time")
    updated_at: datetime = Field(..., description="Update date and time")


class ChatsResponse(BaseSchemaModel):
    chats: list[ChatResponse] = Field(..., description="Chat list")
