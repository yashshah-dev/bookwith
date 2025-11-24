from typing import Literal, Self

from pydantic import Field
from pydantic_settings import BaseSettings

TEST_USER_ID = "91527c9d-48aa-41d0-bb85-dc96f26556a0"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


class AppConfig(BaseSettings):
    gcs_emulator_host: str | None = Field(default=None, description="Cloud Storage Emulator Host")
    database_url: str = Field(description="Database URL")
    gcp_project_id: str = Field(default="bookwith", description="Google Cloud Project ID")
    gcs_bucket_name: str = Field(default="bookwith-bucket", description="GCS bucket name")
    gemini_api_key: str | None = Field(default=None, description="Gemini API Key")
    openai_api_key: str | None = Field(default=None, description="OpenAI API Key")
    
    # AI Provider Configuration
    embedding_provider: Literal["openai", "huggingface", "ollama"] = Field(
        default="huggingface", 
        description="Embedding provider to use"
    )
    llm_provider: Literal["openai", "huggingface", "ollama"] = Field(
        default="ollama", 
        description="LLM provider to use"
    )
    
    # Ollama Configuration
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        description="Ollama server URL"
    )
    ollama_model: str = Field(
        default="llama3.2",
        description="Ollama model name (e.g., llama3.2, mistral, phi3, gemma2)"
    )
    ollama_embedding_model: str = Field(
        default="nomic-embed-text",
        description="Ollama embedding model"
    )
    
    # Hugging Face Configuration
    huggingface_api_key: str | None = Field(default=None, description="Hugging Face API Key (optional for public models)")
    huggingface_embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2", 
        description="Hugging Face embedding model"
    )
    huggingface_llm_model: str = Field(
        default="gpt2",
        description="Hugging Face LLM model for Inference API"
    )

    @classmethod
    def get_config(cls) -> Self:
        return cls()
