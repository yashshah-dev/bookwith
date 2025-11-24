from langchain_weaviate.vectorstores import WeaviateVectorStore

from src.infrastructure.memory.memory_vector_store import MemoryVectorStore


def get_book_content_vector_store() -> WeaviateVectorStore:
    """Get VectorStore for BookContent.

    Reuse the shared client/Embedding already created in MemoryVectorStore,
    preventing unnecessary connections or duplicate model loading.
    """
    try:
        return WeaviateVectorStore(
            client=MemoryVectorStore.get_client(),
            text_key="content",
            index_name=MemoryVectorStore.BOOK_CONTENT_COLLECTION_NAME,
            embedding=MemoryVectorStore.get_embedding_model(),
        )
    except Exception:
        raise
