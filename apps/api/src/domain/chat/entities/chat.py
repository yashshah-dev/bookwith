from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from src.domain.chat.value_objects.book_id import BookId
from src.domain.chat.value_objects.chat_id import ChatId
from src.domain.chat.value_objects.chat_title import ChatTitle
from src.domain.chat.value_objects.user_id import UserId


class Chat(BaseModel):
    id: ChatId = Field(default_factory=lambda: ChatId(value=str(uuid4())))
    user_id: UserId
    title: ChatTitle
    book_id: BookId | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    deleted_at: datetime | None = None

    class Config:
        arbitrary_types_allowed = True  # Allow Value Objects

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Chat):
            return self.id == obj.id
        return False

    def update_title(self, title: ChatTitle) -> None:
        self.title = title
        self.updated_at = datetime.now()

    def update_book_id(self, book_id: BookId | None) -> None:
        self.book_id = book_id
        self.updated_at = datetime.now()

    @classmethod
    def create(cls, user_id: UserId, title: ChatTitle, book_id: BookId | None = None) -> "Chat":
        # Pydantic handles default values, so simply instantiate
        return cls(
            user_id=user_id,
            title=title,
            book_id=book_id,
        )
