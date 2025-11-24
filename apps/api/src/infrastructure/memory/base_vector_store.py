"""Vector store base class."""

import logging
import os

import weaviate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from weaviate.classes.init import AdditionalConfig, Timeout

from src.config.app_config import AppConfig
from src.infrastructure.memory.retry_decorator import retry_on_error

logger = logging.getLogger(__name__)


class BaseVectorStore:
    """Vector store base class.

    Manages shared Weaviate client and embedding models.
    """

    # Collection name constants
    CHAT_MEMORY_COLLECTION_NAME = "ChatMemory"
    BOOK_CONTENT_COLLECTION_NAME = "BookContent"
    BOOK_ANNOTATION_COLLECTION_NAME = "BookAnnotation"

    # Memory type definitions
    TYPE_MESSAGE = "message"
    TYPE_SUMMARY = "summary"

    # Shared singleton instances
    _shared_client: weaviate.WeaviateClient | None = None
    _shared_embedding_model: OpenAIEmbeddings | HuggingFaceEmbeddings | OllamaEmbeddings | None = None

    def __init__(self) -> None:
        """Initialize base vector store."""
        self.config = AppConfig.get_config()

        # Keep Weaviate client as shared instance
        if BaseVectorStore._shared_client is None:
            BaseVectorStore._shared_client = self._create_client()

        self.client = BaseVectorStore._shared_client

        # Keep embedding model as shared instance as well
        if BaseVectorStore._shared_embedding_model is None:
            if self.config.embedding_provider == "openai":
                if not self.config.openai_api_key:
                    raise ValueError("OPENAI_API_KEY is required when using OpenAI embeddings")
                BaseVectorStore._shared_embedding_model = OpenAIEmbeddings(
                    model="text-embedding-3-small", 
                    max_retries=2
                )
                logger.info("Using OpenAI embeddings: text-embedding-3-small")
            elif self.config.embedding_provider == "ollama":
                # Ollama embeddings
                BaseVectorStore._shared_embedding_model = OllamaEmbeddings(
                    base_url=self.config.ollama_base_url,
                    model=self.config.ollama_embedding_model
                )
                logger.info(f"Using Ollama embeddings: {self.config.ollama_embedding_model} at {self.config.ollama_base_url}")
            else:  # huggingface
                # Set HF token if available (for private models or rate limiting)
                if self.config.huggingface_api_key:
                    os.environ["HF_TOKEN"] = self.config.huggingface_api_key
                
                BaseVectorStore._shared_embedding_model = HuggingFaceEmbeddings(
                    model_name=self.config.huggingface_embedding_model,
                    model_kwargs={"device": "cpu"},
                    encode_kwargs={"normalize_embeddings": True}
                )
                logger.info(f"Using Hugging Face embeddings: {self.config.huggingface_embedding_model}")

        self.embedding_model = BaseVectorStore._shared_embedding_model

    @retry_on_error(max_retries=5, initial_delay=2)
    def _create_client(self) -> weaviate.WeaviateClient:
        """Create Weaviate client."""
        try:
            return weaviate.connect_to_local(additional_config=AdditionalConfig(timeout=Timeout(init=30, query=60, insert=120)))
        except Exception as e:
            logger.error(f"Weaviate connection error: {str(e)}")
            raise

    @retry_on_error(max_retries=2)
    def encode_text(self, text: str) -> list[float]:
        """Vectorize text."""
        return self.embedding_model.embed_query(text)

    @classmethod
    def get_client(cls) -> weaviate.WeaviateClient:
        """Return shared Weaviate client."""
        if cls._shared_client is None:
            # _shared_client is created during instantiation
            cls()
        return cls._shared_client  # type: ignore[return-value]

    @classmethod
    def get_embedding_model(cls) -> OpenAIEmbeddings | HuggingFaceEmbeddings | OllamaEmbeddings:
        """Return shared embedding model."""
        if cls._shared_embedding_model is None:
            cls()
        return cls._shared_embedding_model  # type: ignore[return-value]
