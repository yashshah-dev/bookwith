# Hugging Face Integration Guide

This document explains the Hugging Face API integration added to the BookWith API as an alternative to OpenAI.

## Overview

The application now supports two AI providers:
- **OpenAI** (requires paid API key with credits)
- **Hugging Face** (free tier available, runs locally for embeddings)

## What Was Added

### 1. Dependencies (`pyproject.toml`)
```toml
huggingface-hub = "^0.26.0"           # HuggingFace Inference API client
sentence-transformers = "^3.3.1"      # Local embedding models
langchain-huggingface = "^0.1.2"      # LangChain integration
```

### 2. Configuration (`src/config/app_config.py`)
New configuration options:
- `EMBEDDING_PROVIDER`: Choose "openai" or "huggingface"
- `LLM_PROVIDER`: Choose "openai" or "huggingface"
- `HUGGINGFACE_API_KEY`: Optional API token for higher rate limits
- `HUGGINGFACE_EMBEDDING_MODEL`: Model for embeddings (default: all-MiniLM-L6-v2)
- `HUGGINGFACE_LLM_MODEL`: Model for chat (default: Mistral-7B-Instruct-v0.2)

### 3. Base Vector Store (`src/infrastructure/memory/base_vector_store.py`)
- Now supports both OpenAI and Hugging Face embeddings
- Automatically selects provider based on `EMBEDDING_PROVIDER` setting
- Hugging Face embeddings run **locally** (no API calls needed)

### 4. Hugging Face Chat Client (`src/infrastructure/llm/huggingface_client.py`)
- New LangChain-compatible chat model
- Extends `BaseChatModel` for full LCEL support
- Supports streaming responses
- Uses Hugging Face Inference API (free tier available)

### 5. AI Response Generator (`src/usecase/message/ai_response_generator.py`)
- Updated to dynamically create LLM based on provider setting
- Works with both OpenAI and Hugging Face clients seamlessly

## Environment Configuration

### Current Setup (.env)
```bash
####################################################
# AI Provider Configuration
####################################################
# Choose embedding provider: "openai" or "huggingface"
EMBEDDING_PROVIDER=huggingface

# Choose LLM provider: "openai" or "huggingface"
LLM_PROVIDER=huggingface

####################################################
# Hugging Face Settings
####################################################
# Optional: HuggingFace API token (leave as xxx if not needed)
HUGGINGFACE_API_KEY=xxx

# Embedding model (runs locally, no API key needed)
HUGGINGFACE_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Chat model (uses free Inference API, optional token for higher limits)
HUGGINGFACE_LLM_MODEL=mistralai/Mistral-7B-Instruct-v0.2
```

## Installation

### Install Dependencies
```bash
cd /Users/yash/Documents/practice/bookwith/apps/api
make configure
# or: poetry install
```

This will install:
- `huggingface-hub`: For API access
- `sentence-transformers`: For local embedding generation
- `langchain-huggingface`: For LangChain integration

### First Run
On first run with Hugging Face embeddings, the model will be downloaded automatically:
- Model: `sentence-transformers/all-MiniLM-L6-v2` (~80MB)
- Cached in: `~/.cache/huggingface/hub/`
- Only downloaded once

## Usage

### Start the API Server
```bash
cd /Users/yash/Documents/practice/bookwith/apps/api
make run
```

The server will:
1. Load configuration from `.env`
2. Initialize Hugging Face embedding model (local)
3. Initialize Hugging Face Inference API client
4. Start accepting requests

### Switching Providers

#### Use Hugging Face (Free, Local Embeddings)
```bash
# In .env file
EMBEDDING_PROVIDER=huggingface
LLM_PROVIDER=huggingface
```

#### Use OpenAI (Paid, Requires Credits)
```bash
# In .env file
EMBEDDING_PROVIDER=openai
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-your-key-here
```

#### Mix Providers
```bash
# Use HF for embeddings, OpenAI for chat
EMBEDDING_PROVIDER=huggingface
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-your-key-here
```

## Recommended Models

### Embedding Models (Local)
| Model | Size | Quality | Speed |
|-------|------|---------|-------|
| `sentence-transformers/all-MiniLM-L6-v2` | 80MB | Good | Fast ⚡ (default) |
| `sentence-transformers/all-mpnet-base-v2` | 420MB | Better | Medium |
| `BAAI/bge-small-en-v1.5` | 130MB | Good | Fast |
| `BAAI/bge-base-en-v1.5` | 440MB | Better | Medium |

### Chat Models (Inference API)
| Model | Quality | Rate Limit |
|-------|---------|------------|
| `mistralai/Mistral-7B-Instruct-v0.2` | Excellent ⭐ (default) | Free tier available |
| `HuggingFaceH4/zephyr-7b-beta` | Excellent | Free tier available |
| `meta-llama/Llama-2-7b-chat-hf` | Excellent | Requires approval |
| `tiiuae/falcon-7b-instruct` | Good | Free tier available |

## Benefits of Hugging Face

### Cost
- ✅ **Free tier** for Inference API
- ✅ **No API key required** for embeddings (runs locally)
- ✅ Optional token for higher rate limits

### Privacy
- ✅ Embeddings run **locally** on your machine
- ✅ No data sent to external services for embeddings
- ⚠️ Chat messages sent to HF Inference API (like OpenAI)

### Performance
- ✅ Embeddings are instant (local)
- ✅ No network latency for vector search
- ⚠️ Chat responses may be slower than GPT-4 (free tier has limits)

## Troubleshooting

### "No module named 'sentence_transformers'"
```bash
cd /Users/yash/Documents/practice/bookwith/apps/api
make configure
```

### Slow First Request
The first request downloads the embedding model (~80MB). Subsequent requests are fast.

### Rate Limiting (HF Inference API)
If you hit rate limits on the free tier:
1. Get a free API token: https://huggingface.co/settings/tokens
2. Add to `.env`: `HUGGINGFACE_API_KEY=hf_your_token_here`
3. Restart server

### Model Download Location
Models are cached in: `~/.cache/huggingface/hub/`

To clear cache:
```bash
rm -rf ~/.cache/huggingface/hub/
```

## Architecture

### Request Flow
```
User sends message
    ↓
AIResponseGenerator._create_llm()
    ↓
Check LLM_PROVIDER config
    ↓
├─ "openai" → ChatOpenAI(gpt-4o)
└─ "huggingface" → HuggingFaceChatClient(Mistral-7B)
    ↓
Stream response back to user
```

### Embedding Flow
```
Search query
    ↓
BaseVectorStore.encode_text()
    ↓
Check EMBEDDING_PROVIDER config
    ↓
├─ "openai" → OpenAIEmbeddings (API call)
└─ "huggingface" → HuggingFaceEmbeddings (local)
    ↓
Vector search in Weaviate
    ↓
Return relevant documents
```

## Testing

### Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "test-chat-id",
    "sender_id": "91527c9d-48aa-41d0-bb85-dc96f26556a0",
    "content": "Hello, how are you?"
  }'
```

### Verify Embedding Provider
Check logs on startup:
```
INFO - Using Hugging Face embeddings: sentence-transformers/all-MiniLM-L6-v2
INFO - Initialized Hugging Face chat client with model: mistralai/Mistral-7B-Instruct-v0.2
```

## Migration from OpenAI

### Steps
1. **Update `.env`**:
   ```bash
   EMBEDDING_PROVIDER=huggingface
   LLM_PROVIDER=huggingface
   ```

2. **Install dependencies**:
   ```bash
   make configure
   ```

3. **Restart server**:
   ```bash
   make run
   ```

4. **First request** will download models (one-time)

### Rollback to OpenAI
Simply change providers in `.env` and restart:
```bash
EMBEDDING_PROVIDER=openai
LLM_PROVIDER=openai
```

## Performance Comparison

| Feature | OpenAI | Hugging Face |
|---------|--------|--------------|
| Embedding Speed | ~200ms (API) | ~50ms (local) ⚡ |
| Chat Quality | Excellent (GPT-4) | Excellent (Mistral-7B) |
| Chat Speed | Fast | Medium (free tier) |
| Cost | $$ | Free ✅ |
| Rate Limits | High (paid) | Medium (free) |
| Privacy | API call | Mixed (embeddings local) |

## Support

For issues or questions:
1. Check logs: Look for HuggingFace-related errors
2. Verify models: Ensure correct model IDs in `.env`
3. Check rate limits: Consider getting HF API token
4. Test locally: Try embeddings with small test

## References

- [Hugging Face Hub](https://huggingface.co/)
- [Sentence Transformers](https://www.sbert.net/)
- [LangChain Hugging Face Integration](https://python.langchain.com/docs/integrations/llms/huggingface_hub)
- [Mistral AI Models](https://huggingface.co/mistralai)
