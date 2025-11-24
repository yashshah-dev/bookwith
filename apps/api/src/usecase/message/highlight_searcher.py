"""Highlight search service."""

import logging

from src.infrastructure.memory.memory_vector_store import MemoryVectorStore

logger = logging.getLogger(__name__)


class HighlightSearcher:
    """Service for searching book highlights (annotations)."""

    def __init__(self) -> None:
        """Initialize highlight search service."""
        self.memory_vector_store = MemoryVectorStore()

    def search_relevant_highlights(self, question: str, user_id: str, book_id: str, limit: int = 3) -> list[str]:
        """Search for highlight texts related to the question."""
        if not (user_id and book_id):
            return ["No highlights found"]

        # Vectorize the question
        query_vector = self.memory_vector_store.encode_text(question)

        # Search highlights
        try:
            highlights = self.memory_vector_store.search_highlights(user_id=user_id, book_id=book_id, query_vector=query_vector, limit=limit)
        except Exception as e:
            logger.error(f"Failed to search highlights: {e}")
            return ["Search error occurred"]

        if not highlights:
            return ["No highlights found"]

        # Format highlight texts
        highlight_texts = []
        for h in highlights:
            highlight_text = h["content"]
            if h.get("notes"):
                highlight_text += f"\n{h['notes']}"
            highlight_texts.append(f"[Highlight]{highlight_text}")

        return highlight_texts
