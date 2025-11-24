"""Message processing service."""

from typing import Any

from src.domain.message.entities.message import Message
from src.domain.message.repositories.message_repository import MessageRepository
from src.domain.message.value_objects.message_content import MessageContent
from src.domain.message.value_objects.sender_type import SenderType
from src.infrastructure.memory.memory_service import MemoryService


class MessageProcessor:
    """Service for saving and vectorizing messages."""

    def __init__(self, message_repository: MessageRepository, memory_service: MemoryService) -> None:
        """Initialize message processing service."""
        self.message_repository = message_repository
        self.memory_service = memory_service

    def save_user_message(self, content: str, sender_id: str, chat_id: str, metadata: dict[str, Any] | None = None) -> Message:
        """Save and vectorize user message."""
        meta = metadata or {}

        user_message = Message.create(
            content=MessageContent(content),
            sender_id=sender_id,
            sender_type=SenderType.user(),
            chat_id=chat_id,
            metadata=meta,
        )

        # Save message
        self.message_repository.save(user_message)

        # Vectorize message
        self.memory_service.vectorize_message(user_message)

        return user_message

    def save_ai_message(self, content: str, sender_id: str, chat_id: str, metadata: dict[str, Any] | None = None) -> Message:
        """Save and vectorize AI message."""
        meta = metadata or {}

        ai_message = Message.create(
            content=MessageContent(content),
            sender_id=sender_id,
            sender_type=SenderType.assistant(),
            chat_id=chat_id,
            metadata=meta,
        )

        # Save message
        self.message_repository.save(ai_message)

        # Vectorize AI response as well
        self.memory_service.vectorize_message(ai_message)

        return ai_message

    def process_summarization(self, chat_id: str, sender_id: str) -> None:
        """Execute chat summarization if needed."""
        # Get message count for chat
        message_count = self.message_repository.count_by_chat_id(chat_id)

        # Execute summarization if needed
        self.memory_service.summarize_chat(
            chat_id=chat_id,
            user_id=sender_id,
            message_count=message_count,
        )

    def get_latest_messages(self, chat_id: str) -> list[Message]:
        """Get latest messages and return sorted in chronological order."""
        # Get required number in newest-first order (descending)
        latest_messages = self.message_repository.find_latest_by_chat_id(chat_id, limit=5)

        # Re-sort in chronological order (ascending)
        return sorted(latest_messages, key=lambda msg: msg.created_at)
