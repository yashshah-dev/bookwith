"""Memory retrieval service."""

import logging
from typing import Any

from src.config.app_config import AppConfig
from src.infrastructure.memory.memory_vector_store import MemoryVectorStore

logger = logging.getLogger(__name__)


class MemoryRetrievalService:
    """Service specialized for memory retrieval."""

    def __init__(self, memory_store: MemoryVectorStore | None = None) -> None:
        """Initialize memory retrieval service."""
        self.config = AppConfig.get_config()
        self.memory_store = memory_store or MemoryVectorStore()

    def search_relevant_memories(self, user_id: str, chat_id: str, query: str, chat_limit: int | None = None) -> list[dict[str, Any]]:
        """Search for memories related to user query.

        Args:
            user_id: User ID
            chat_id: Chat ID
            query: User's question/query
            chat_limit: Number of chat memories to retrieve

        Returns:
            Chat memory list

        """
        if chat_limit is None:
            chat_limit = 3

        try:
            query_vector = self.memory_store.encode_text(query)
            return self.memory_store.search_chat_memories(user_id=user_id, chat_id=chat_id, query_vector=query_vector, limit=chat_limit)
        except Exception as e:
            logger.error(f"Error occurred during memory search: {str(e)}", exc_info=True)
            return []

    def format_memory_item(self, memory: dict[str, Any], prefix: str = "") -> str:
        """Format memory item."""
        content = memory.get("content", "N/A")

        # Get relevance
        certainty = None
        if "_additional" in memory and isinstance(memory["_additional"], dict):
            certainty = memory["_additional"].get("certainty")

        # Display if relevance exists
        formatted = f"{prefix}{content}"
        if certainty is not None:
            formatted += f" (relevance: {certainty:.2f})"

        return formatted
