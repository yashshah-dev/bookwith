"""Weaviate collection management service."""

import logging

from weaviate.classes.config import Configure, DataType, Property

from src.infrastructure.memory.base_vector_store import BaseVectorStore
from src.infrastructure.memory.retry_decorator import retry_on_error

logger = logging.getLogger(__name__)


class CollectionManager(BaseVectorStore):
    """Service for creating and managing Weaviate collections."""

    def __init__(self) -> None:
        """Initialize collection management service."""
        super().__init__()
        self._ensure_collections()

    @retry_on_error(max_retries=3, initial_delay=1)
    def _ensure_collections(self) -> None:
        """Ensure Weaviate collections exist."""
        try:
            self._create_chat_memory_collection()
            self._create_book_content_collection()
            self._create_book_annotation_collection()
        except Exception as e:
            logger.error(f"Collection creation error: {str(e)}")
            raise

    def _create_chat_memory_collection(self) -> None:
        """Create ChatMemory collection."""
        if not self.client.collections.exists(self.CHAT_MEMORY_COLLECTION_NAME):
            self.client.collections.create(
                name=self.CHAT_MEMORY_COLLECTION_NAME,
                multi_tenancy_config=Configure.multi_tenancy(
                    enabled=True,
                    auto_tenant_activation=True,
                    auto_tenant_creation=True,
                ),
                vectorizer_config=None,
                properties=[
                    Property(
                        name="chat_id",
                        data_type=DataType.TEXT,
                        description="Chat ID",
                        index_searchable=True,
                    ),
                    Property(
                        name="content",
                        data_type=DataType.TEXT,
                        description="Message/summary content",
                    ),
                    Property(
                        name="created_at",
                        data_type=DataType.DATE,
                        description="Creation timestamp",
                    ),
                    Property(
                        name="is_summarized",
                        data_type=DataType.BOOL,
                        description="Summarized flag (message only)",
                    ),
                    Property(
                        name="memory_type",
                        data_type=DataType.TEXT,
                        description="Memory type (message, summary)",
                        index_searchable=True,
                    ),
                    Property(
                        name="message_id",
                        data_type=DataType.TEXT,
                        description="Original message ID",
                    ),
                    Property(
                        name="sender",
                        data_type=DataType.TEXT,
                        description="Sender type (user, assistant, system)",
                        index_searchable=True,
                    ),
                    Property(
                        name="user_id",
                        data_type=DataType.TEXT,
                        description="User ID",
                        index_searchable=True,
                    ),
                ],
            )

    def _create_book_content_collection(self) -> None:
        """Create BookContent collection."""
        if not self.client.collections.exists(self.BOOK_CONTENT_COLLECTION_NAME):
            self.client.collections.create(
                name=self.BOOK_CONTENT_COLLECTION_NAME,
                vectorizer_config=None,
                properties=[
                    Property(name="content", data_type=DataType.TEXT),
                    Property(name="book_id", data_type=DataType.TEXT, index_searchable=True, description="Book ID"),
                ],
                multi_tenancy_config=Configure.multi_tenancy(
                    enabled=True,
                    auto_tenant_activation=True,
                    auto_tenant_creation=True,
                ),
            )

    def _create_book_annotation_collection(self) -> None:
        """Create BookAnnotation collection."""
        if not self.client.collections.exists(self.BOOK_ANNOTATION_COLLECTION_NAME):
            self.client.collections.create(
                name=self.BOOK_ANNOTATION_COLLECTION_NAME,
                vectorizer_config=None,
                multi_tenancy_config=Configure.multi_tenancy(
                    enabled=True,
                    auto_tenant_activation=True,
                    auto_tenant_creation=True,
                ),
                properties=[
                    Property(
                        name="annotation_id",
                        data_type=DataType.TEXT,
                        description="Annotation ID",
                        index_searchable=True,
                    ),
                    Property(
                        name="book_id",
                        data_type=DataType.TEXT,
                        description="Book ID",
                        index_searchable=True,
                    ),
                    Property(
                        name="book_title",
                        data_type=DataType.TEXT,
                        description="Book title",
                        index_searchable=True,
                    ),
                    Property(
                        name="content",
                        data_type=DataType.TEXT,
                        description="Highlighted text content",
                    ),
                    Property(
                        name="created_at",
                        data_type=DataType.DATE,
                        description="Creation timestamp",
                    ),
                    Property(
                        name="notes",
                        data_type=DataType.TEXT,
                        description="Notes",
                    ),
                    Property(
                        name="user_id",
                        data_type=DataType.TEXT,
                        description="User ID",
                        index_searchable=True,
                    ),
                ],
            )
