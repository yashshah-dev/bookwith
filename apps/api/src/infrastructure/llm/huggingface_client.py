"""Hugging Face Inference API client for chat completions."""

import logging
from collections.abc import AsyncIterator, Iterator
from typing import Any

from huggingface_hub import AsyncInferenceClient
from langchain_core.callbacks.manager import AsyncCallbackManagerForLLMRun, CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult

from src.config.app_config import AppConfig

logger = logging.getLogger(__name__)


class HuggingFaceChatClient(BaseChatModel):
    """Hugging Face Inference API client for LangChain.
    
    This client extends BaseChatModel to provide full LangChain compatibility
    including LCEL chain support and streaming capabilities.
    """

    model_name: str
    temperature: float = 0.7
    max_tokens: int = 2048
    api_key: str | None = None
    streaming: bool = True
    _client: AsyncInferenceClient | None = None

    def __init__(
        self,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        streaming: bool = True,
        api_key: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize Hugging Face chat client.
        
        Args:
            model: HuggingFace model ID (e.g., "mistralai/Mistral-7B-Instruct-v0.2")
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            streaming: Whether to enable streaming by default
            api_key: HuggingFace API token (optional for public models)
            **kwargs: Additional arguments for BaseChatModel
        """
        config = AppConfig.get_config()
        
        model_name = model or config.huggingface_llm_model
        token = api_key or config.huggingface_api_key
        
        super().__init__(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=streaming,
            api_key=token,
            **kwargs
        )
        
        # Initialize async client
        self._client = AsyncInferenceClient(token=token if token != "xxx" else None)
        
        logger.info(f"Initialized Hugging Face chat client with model: {model_name}")

    @property
    def _llm_type(self) -> str:
        """Return identifier for this LLM type."""
        return "huggingface-inference"

    def _format_messages_for_hf(self, messages: list[BaseMessage]) -> str:
        """Format LangChain messages for Hugging Face chat models.
        
        Converts LangChain message format to a prompt string suitable for
        different model architectures.
        
        Args:
            messages: List of LangChain messages
            
        Returns:
            Formatted prompt string
        """
        # Check model type for appropriate formatting
        model_lower = self.model_name.lower()
        
        if "gpt" in model_lower and ("gpt2" in model_lower or "gpt-neo" in model_lower or "gpt-j" in model_lower):
            # GPT-2/Neo/J format: Simple conversational format
            parts = []
            for message in messages:
                if isinstance(message, SystemMessage):
                    parts.append(f"{message.content}\n\n")
                elif isinstance(message, HumanMessage):
                    parts.append(f"Human: {message.content}\n\n")
                elif isinstance(message, AIMessage):
                    parts.append(f"Assistant: {message.content}\n\n")
                else:
                    parts.append(f"{message.content}\n\n")
            parts.append("Assistant:")
            return "".join(parts)
            
        elif "flan" in model_lower or "t5" in model_lower:
            # FLAN-T5 format: simple instruction format
            parts = []
            for message in messages:
                if isinstance(message, SystemMessage):
                    parts.append(f"Context: {message.content}")
                elif isinstance(message, HumanMessage):
                    parts.append(f"Question: {message.content}")
                elif isinstance(message, AIMessage):
                    parts.append(f"Answer: {message.content}")
                else:
                    parts.append(message.content)
            return " ".join(parts)
            
        elif "phi-3" in model_lower or "phi3" in model_lower:
            # Phi-3 format
            formatted_parts = []
            for message in messages:
                if isinstance(message, SystemMessage):
                    formatted_parts.append(f"<|system|>\n{message.content}<|end|>\n")
                elif isinstance(message, HumanMessage):
                    formatted_parts.append(f"<|user|>\n{message.content}<|end|>\n")
                elif isinstance(message, AIMessage):
                    formatted_parts.append(f"<|assistant|>\n{message.content}<|end|>\n")
                else:
                    formatted_parts.append(f"<|user|>\n{message.content}<|end|>\n")
            formatted_parts.append("<|assistant|>\n")
            return "".join(formatted_parts)
            
        elif "mistral" in model_lower:
            # Mistral format
            formatted_parts = []
            for message in messages:
                if isinstance(message, SystemMessage):
                    formatted_parts.append(f"<s>[INST] {message.content} [/INST]")
                elif isinstance(message, HumanMessage):
                    formatted_parts.append(f"[INST] {message.content} [/INST]")
                elif isinstance(message, AIMessage):
                    formatted_parts.append(f"{message.content}</s>")
                else:
                    formatted_parts.append(f"[INST] {message.content} [/INST]")
            return "\n".join(formatted_parts)
            
        else:
            # Generic format for other models
            formatted_parts = []
            for message in messages:
                if isinstance(message, SystemMessage):
                    formatted_parts.append(f"System: {message.content}\n")
                elif isinstance(message, HumanMessage):
                    formatted_parts.append(f"Human: {message.content}\n")
                elif isinstance(message, AIMessage):
                    formatted_parts.append(f"Assistant: {message.content}\n")
                else:
                    formatted_parts.append(f"Human: {message.content}\n")
            formatted_parts.append("Assistant:")
            return "\n".join(formatted_parts)

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate chat response (sync - not recommended, use async methods)."""
        raise NotImplementedError("Use async methods (agenerate or astream) for HuggingFace client")

    async def _agenerate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: AsyncCallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate complete chat response asynchronously."""
        prompt = self._format_messages_for_hf(messages)
        
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        
        try:
            # Non-streaming generation
            response = await self._client.text_generation(
                prompt=prompt,
                model=self.model_name,
                max_new_tokens=max_tokens,
                temperature=temperature,
                stream=False,
            )
            
            # text_generation returns a string when stream=False
            content = response if isinstance(response, str) else str(response)
            
            # Create LangChain-compatible output
            message = AIMessage(content=content)
            generation = ChatGeneration(message=message)
            
            return ChatResult(generations=[generation])
            
        except Exception as e:
            logger.error(f"Error generating from Hugging Face API: {str(e)}")
            raise

    def _stream(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        """Stream chat response (sync - not recommended, use async)."""
        raise NotImplementedError("Use async streaming (_astream) for HuggingFace client")

    async def _astream(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: AsyncCallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        """Stream chat completion responses asynchronously."""
        prompt = self._format_messages_for_hf(messages)
        
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        
        try:
            # Stream responses from Hugging Face Inference API
            # text_generation returns an async generator when stream=True
            stream = await self._client.text_generation(
                prompt=prompt,
                model=self.model_name,
                max_new_tokens=max_tokens,
                temperature=temperature,
                stream=True,
            )
            
            async for token in stream:
                chunk = ChatGenerationChunk(message=AIMessageChunk(content=token))
                
                if run_manager:
                    await run_manager.on_llm_new_token(token, chunk=chunk)
                
                yield chunk
                
        except Exception as e:
            logger.error(f"Error streaming from Hugging Face API: {str(e)}")
            raise

