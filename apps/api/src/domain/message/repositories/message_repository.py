from abc import ABC, abstractmethod

from src.domain.message.entities.message import Message
from src.domain.message.value_objects.message_id import MessageId


class MessageRepository(ABC):
    @abstractmethod
    def save(self, message: Message) -> None:
        """Save a message."""

    @abstractmethod
    def find_by_id(self, message_id: MessageId) -> Message | None:
        """Find a message by ID."""

    @abstractmethod
    def find_all(self) -> list[Message]:
        """Retrieve all messages."""

    @abstractmethod
    def find_by_chat_id(self, chat_id: str) -> list[Message]:
        """Find messages by chat ID."""

    @abstractmethod
    def find_latest_by_chat_id(self, chat_id: str, limit: int) -> list[Message]:
        """Retrieve the latest messages by chat ID with a specified limit."""

    @abstractmethod
    def find_by_sender_id(self, sender_id: str) -> list[Message]:
        """Find messages by sender ID."""

    @abstractmethod
    def delete(self, message_id: MessageId) -> None:
        """Delete a message by ID."""

    @abstractmethod
    def bulk_delete(self, message_ids: list[MessageId]) -> list[MessageId]:
        """Bulk delete multiple messages. Return a list of message IDs that failed to delete."""

    @abstractmethod
    def count_by_chat_id(self, chat_id: str) -> int:
        """Get the count of messages related to a chat ID."""

    @abstractmethod
    def find_chat_ids_by_user_id(self, user_id: str) -> list[str]:
        """Get chat IDs related to a user ID."""
