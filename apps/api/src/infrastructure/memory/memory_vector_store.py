"""Integrated vector store management class."""

import logging
from typing import Any

import weaviate
from fastapi import UploadFile
from langchain_openai import OpenAIEmbeddings

from src.infrastructure.memory.base_vector_store import BaseVectorStore
from src.infrastructure.memory.book_annotation_store import BookAnnotationStore
from src.infrastructure.memory.book_content_store import BookContentStore
from src.infrastructure.memory.chat_memory_store import ChatMemoryStore
from src.infrastructure.memory.collection_manager import CollectionManager
from src.infrastructure.memory.vector_crud_service import VectorCrudService

logger = logging.getLogger(__name__)


class MemoryVectorStore(BaseVectorStore):
    """Integrated vector store management class for chat memory, book content, and annotations.

    Integrates functions of each specialized service while maintaining existing interfaces.
    """

    def __init__(self) -> None:
        """Initialize vector store integrated management class."""
        super().__init__()

        # Initialize collections
        self.collection_manager = CollectionManager()

        # Initialize each specialized service
        self.chat_memory = ChatMemoryStore()
        self.book_content = BookContentStore()
        self.book_annotation = BookAnnotationStore()
        self.crud_service = VectorCrudService()

    # Chat memory related methods (delegated to ChatMemoryStore)
    def search_chat_memories(self, user_id: str, chat_id: str, query_vector: list[float], limit: int = 5) -> list[dict[str, Any]]:
        """Vector search for related memories by chat ID."""
        return self.chat_memory.search_chat_memories(user_id, chat_id, query_vector, limit)

    def get_unsummarized_messages(self, user_id: str, chat_id: str, max_count: int = 100) -> list[dict[str, Any]]:
        """Get unsummarized messages."""
        return self.chat_memory.get_unsummarized_messages(user_id, chat_id, max_count)

    def mark_messages_as_summarized(self, user_id: str, chat_id: str, message_ids: list[str]) -> None:
        """Mark specified messages as summarized."""
        self.chat_memory.mark_messages_as_summarized(user_id, chat_id, message_ids)

    # Book content related methods (delegated to BookContentStore)
    async def create_book_vector_index(self, file: UploadFile, user_id: str, book_id: str) -> dict:
        """Process EPUB file and vector index it in BookContent collection."""
        return await self.book_content.create_book_vector_index(file, user_id, book_id)

    # Annotation related methods (delegated to BookAnnotationStore)
    def search_highlights(self, user_id: str, book_id: str, query_vector: list[float], limit: int = 3) -> list[dict[str, Any]]:
        """Vector search highlights (BookAnnotation collection)."""
        return self.book_annotation.search_highlights(user_id, book_id, query_vector, limit)

    # CRUD operations (delegated to VectorCrudService)
    def add_memory(self, vector: list[float], metadata: dict, user_id: str, collection_name: str) -> str:
        """Add memory to appropriate vector store collection."""
        return self.crud_service.add_memory(vector, metadata, user_id, collection_name)

    def delete_memory(self, user_id: str, collection_name: str, target: str, key: str) -> None:
        """Delete memory."""
        self.crud_service.delete_memory(user_id, collection_name, target, key)

    def update_memory(self, user_id: str, collection_name: str, target: str, key: str, properties: dict, vector: list[float]) -> None:
        """Update memory."""
        self.crud_service.update_memory(user_id, collection_name, target, key, properties, vector)

    def delete_book_data(self, user_id: str, book_id: str) -> None:
        """Delete all vector data related to a book."""
        self.crud_service.delete_book_data(user_id, book_id)

    # Class methods for backward compatibility (inherited from BaseVectorStore)
    @classmethod
    def get_client(cls) -> weaviate.WeaviateClient:
        """Return shared Weaviate client."""
        return super().get_client()

    @classmethod
    def get_embedding_model(cls) -> OpenAIEmbeddings:
        """Return shared embedding model."""
        return super().get_embedding_model()
