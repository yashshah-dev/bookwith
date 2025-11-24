from abc import ABC, abstractmethod

from src.domain.chat.entities.chat import Chat
from src.domain.chat.value_objects.book_id import BookId
from src.domain.chat.value_objects.chat_id import ChatId
from src.domain.chat.value_objects.user_id import UserId


class ChatRepository(ABC):
    """Chat repository interface."""

    @abstractmethod
    def save(self, chat: Chat) -> None:
        """Save a chat."""

    @abstractmethod
    def find_by_id(self, chat_id: ChatId) -> Chat | None:
        """Find a chat by ID."""

    @abstractmethod
    def find_by_user_id(self, user_id: UserId) -> list[Chat]:
        """Retrieve all chats associated with a user ID."""

    @abstractmethod
    def find_by_book_id(self, book_id: BookId) -> list[Chat]:
        """Retrieve all chats associated with a book ID."""

    @abstractmethod
    def find_by_user_id_and_book_id(self, user_id: UserId, book_id: BookId) -> list[Chat]:
        """Find chats associated with a user ID and book ID."""

    @abstractmethod
    def delete(self, chat_id: ChatId) -> None:
        """Delete a chat by ID."""
