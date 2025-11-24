"""Prompt building service."""

import logging
from typing import Any

import tiktoken
from tiktoken.core import Encoding

from src.config.app_config import AppConfig
from src.domain.message.entities.message import Message
from src.infrastructure.memory.memory_retrieval_service import MemoryRetrievalService

logger = logging.getLogger(__name__)

# Tiktoken encoder (for token counting)
TIKTOKEN_ENCODING: Encoding | None = None
try:
    TIKTOKEN_ENCODING = tiktoken.get_encoding("cl100k_base")  # Encoding for GPT-4
except Exception as e:
    logger.warning(f"Failed to initialize tiktoken: {str(e)}")


class PromptBuilderService:
    """Service specialized for prompt building."""

    def __init__(self, memory_retrieval_service: MemoryRetrievalService | None = None) -> None:
        """Initialize prompt building service."""
        self.config = AppConfig.get_config()
        self.memory_retrieval = memory_retrieval_service or MemoryRetrievalService()

    def build_memory_prompt(self, buffer: list[Message], user_query: str, user_id: str, chat_id: str) -> str:
        """Build prompt based on memory.

        Args:
            buffer: Latest message buffer
            user_query: User's question/query
            user_id: User ID
            chat_id: Chat ID

        Returns:
            Constructed prompt

        """
        # Search for related memories
        chat_memories = self.memory_retrieval.search_relevant_memories(user_id=user_id, chat_id=chat_id, query=user_query)

        # Build prompt
        return self._create_memory_prompt(buffer=buffer, chat_memories=chat_memories, user_query=user_query)

    def _create_memory_prompt(
        self,
        buffer: list[Message],
        chat_memories: list[dict[str, Any]],
        user_query: str,
    ) -> str:
        """Create prompt from memory and buffer."""
        system_prompt = (
            "Please answer the question considering the user's profile information, past conversations, and recent chat history. "
            "Strive to provide consistent and personalized responses while utilizing the provided information."
        )

        prompt_parts = [system_prompt]

        # Add past conversation memories
        if chat_memories:
            memory_items = [
                self.memory_retrieval.format_memory_item(
                    mem,
                    f"[Past {'message' if mem.get('type') == 'message' else 'summary'} by "
                    f"{'User' if mem.get('sender') == 'user' else 'AI' if mem.get('sender') == 'assistant' else 'System'}]: ",
                )
                for mem in chat_memories
            ]
            prompt_parts.append("\n--- Related Past Conversations ---\n" + "\n".join(memory_items))

        # Add recent chat history
        if buffer:
            history_items = [
                f"{'User' if msg.sender_type.value == 'user' else 'AI'}: {msg.content.value}" for msg in reversed(buffer) if not msg.is_deleted
            ]
            prompt_parts.append("\n--- Recent Chat History (Oldest First) ---\n" + "\n".join(history_items))

        prompt_parts.append(f"\nUser: {user_query}\nAI:")

        # Combine prompts
        full_prompt = "\n".join(prompt_parts)

        # Apply token limit
        return self._apply_token_limit(full_prompt, prompt_parts)

    def _apply_token_limit(self, full_prompt: str, prompt_parts: list[str]) -> str:
        """Apply token limit to adjust prompt."""
        estimated_tokens = self._estimate_tokens(full_prompt)
        max_tokens = 8192

        if estimated_tokens > max_tokens:
            # Always keep system prompt and query parts
            required = prompt_parts[0] + prompt_parts[-1]
            remain_tokens = max_tokens - self._estimate_tokens(required)

            # Truncate history/memory parts evenly
            middle_parts = prompt_parts[1:-1]
            if middle_parts:
                per_part = max(remain_tokens // len(middle_parts), 1)
                truncated = [self._truncate_text_to_tokens(p, per_part) for p in middle_parts]
                full_prompt = prompt_parts[0] + "\n" + "\n".join(truncated) + prompt_parts[-1]

        return full_prompt

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count of text."""
        if TIKTOKEN_ENCODING:
            return len(TIKTOKEN_ENCODING.encode(text))
        # Fallback: Simple token count estimation
        return len(text) // 4

    def _truncate_text_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text based on token limit."""
        if TIKTOKEN_ENCODING:
            tokens = TIKTOKEN_ENCODING.encode(text)
            if len(tokens) <= max_tokens:
                return text
            return TIKTOKEN_ENCODING.decode(tokens[:max_tokens]) + "..."

        # Fallback: Truncate by approximate character count
        char_per_token = 4  # Average characters per token
        max_chars = max_tokens * char_per_token
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "..."
