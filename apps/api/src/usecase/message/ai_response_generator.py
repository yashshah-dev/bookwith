"""AI response generation service."""

from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Any

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from weaviate.classes.query import Filter

from src.config.app_config import AppConfig
from src.infrastructure.llm.huggingface_client import HuggingFaceChatClient
from src.infrastructure.vector import get_book_content_vector_store
from src.usecase.message.highlight_searcher import HighlightSearcher

if TYPE_CHECKING:
    from langchain_core.runnables import RunnableSerializable


class AIResponseGenerator:
    """Service for generating and streaming AI responses."""

    def __init__(self) -> None:
        """Initialize the AI response generation service."""
        self.highlight_searcher = HighlightSearcher()
        self.config = AppConfig.get_config()

    def _create_llm(self) -> ChatOpenAI | HuggingFaceChatClient | ChatOllama:
        """Create LLM instance based on configured provider.
        
        Returns:
            ChatOpenAI, HuggingFaceChatClient, or ChatOllama instance
        """
        if self.config.llm_provider == "openai":
            if not self.config.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when using OpenAI LLM")
            return ChatOpenAI(model_name="gpt-4o", streaming=True)
        elif self.config.llm_provider == "ollama":
            return ChatOllama(
                base_url=self.config.ollama_base_url,
                model=self.config.ollama_model,
                temperature=0.7,
            )
        else:  # huggingface
            return HuggingFaceChatClient()

    async def stream_ai_response(
        self,
        question: str,
        user_id: str,
        book_id: str | None = None,
    ) -> AsyncGenerator[str]:
        """Stream the LLM response."""
        model = self._create_llm()

        # If book_id is not provided, return memory-based response only
        if book_id is None:
            async for chunk in self._stream_memory_based_response(question, model):
                yield chunk
            return

        # If book_id is provided, combine memory-based and RAG-based responses
        async for chunk in self._stream_hybrid_response(question, user_id, book_id, model):
            yield chunk

    async def _stream_memory_based_response(
        self, question: str, model: ChatOpenAI | HuggingFaceChatClient | ChatOllama
    ) -> AsyncGenerator[str]:
        """Stream memory-based response."""
        # Add strong system prompt to enforce English responses
        english_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant that MUST respond ONLY in English.

CRITICAL RULE: You must write your entire response in English language. Never use Japanese, Chinese, Korean, or any other language. 
Even if the user writes in another language, you must respond in English only.

Example:
User: "こんにちは" (Japanese)
You: "Hello! How can I help you today?"

User: "你好" (Chinese)
You: "Hi! What can I do for you?"

Always write in English. This is mandatory."""),
            ("human", "{question}")
        ])
        
        basic_chain: RunnableSerializable[Any, str] = english_prompt | model | StrOutputParser()

        async for chunk in basic_chain.astream({"question": question}):
            yield chunk

    async def _stream_hybrid_response(
        self, question: str, user_id: str, book_id: str, model: ChatOpenAI | HuggingFaceChatClient | ChatOllama
    ) -> AsyncGenerator[str]:
        """Stream combined memory-based and RAG-based response."""
        # Get book content vector store
        vector_store = get_book_content_vector_store()
        vector_store_retriever = vector_store.as_retriever(
            search_kwargs={"k": 4, "tenant": user_id, "filters": Filter.by_property("book_id").equal(book_id)}
        )

        # Search for relevant highlights
        highlight_texts = self.highlight_searcher.search_relevant_highlights(question, user_id, book_id)

        # Build hybrid chain
        hybrid_chain: RunnableSerializable[Any, str] = (
            {
                "book_content": vector_store_retriever | self._format_documents_as_string,
                "highlight_texts": lambda _: highlight_texts,
                "question": lambda _: question,
            }
            | ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are a polite and helpful assistant. 

CRITICAL RULE: You MUST respond ONLY in English language. Never use Japanese, Chinese, Korean, or any other language.
Even if the book content or user's question is in another language, your response must be in English only.

Please answer the user's question by considering the following information sources:
1. The conversation history (included in the question)
2. Related book content (provided as context information)
3. User's highlighted sections (if relevant)

Consider both the conversation context and book information to provide a consistent and appropriate response.
If book information or highlights are relevant, prioritize using them.
If the context doesn't contain relevant information, base your answer only on the conversation context.

Related information from the book:
{book_content}

Highlighted sections:
{highlight_texts}

Remember: Your entire response must be written in English language only.
                        """,
                    ),
                    ("human", "Question with conversation context: {question}"),
                ]
            )
            | model
            | StrOutputParser()
        )

        async for chunk in hybrid_chain.astream(question):
            yield chunk

    def _format_documents_as_string(self, documents: list[Document]) -> str:
        """Format list of documents as a string."""
        return "\n\n".join(doc.page_content for doc in documents)
