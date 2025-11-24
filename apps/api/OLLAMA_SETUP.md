# Ollama Local Setup Guide

Complete guide for running BookWith API with Ollama for local AI inference.

## Why Ollama?

- ✅ **100% Free** - No API costs, no rate limits
- ✅ **Fully Local** - Complete privacy, no data sent to external servers
- ✅ **Fast** - Runs on your machine with GPU acceleration
- ✅ **Easy Setup** - Simple installation and model management
- ✅ **Multiple Models** - Choose from Llama, Mistral, Phi, Gemma, and more

## Prerequisites

- macOS, Linux, or Windows
- At least 8GB RAM (16GB recommended for larger models)
- Optional: GPU for faster inference

## Installation

### 1. Install Ollama

**macOS:**
```bash
brew install ollama
```

Or download from: https://ollama.com/download/mac

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download installer from: https://ollama.com/download/windows

### 2. Start Ollama Service

**macOS/Linux:**
```bash
# Ollama runs as a background service automatically
# Check if it's running:
ollama --version
```

**Windows:**
Ollama starts automatically after installation.

### 3. Pull Required Models

**Chat Model (Choose one):**
```bash
# Llama 3.2 (3B) - Recommended for development (2GB download)
ollama pull llama3.2

# OR Mistral (7B) - Better quality, slower (4.1GB download)
ollama pull mistral

# OR Phi-3 (3.8B) - Fast, good quality (2.3GB download)
ollama pull phi3

# OR Llama 3.1 (8B) - Best quality (4.7GB download)
ollama pull llama3.1:8b
```

**Embedding Model:**
```bash
# Nomic Embed Text - Recommended (274MB download)
ollama pull nomic-embed-text

# OR Mxbai Embed Large - Higher quality (669MB download)
ollama pull mxbai-embed-large
```

### 4. Verify Installation

```bash
# List installed models
ollama list

# Test chat model
ollama run llama3.2

# Type a message and press Enter
# Type /bye to exit
```

## Configuration

Your `.env` file is already configured for Ollama:

```bash
####################################################
# AI Provider Configuration
####################################################
EMBEDDING_PROVIDER=ollama
LLM_PROVIDER=ollama

####################################################
# Ollama Configuration
####################################################
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

### Changing Models

Edit `.env` and change the model name:

```bash
# For better quality (but slower):
OLLAMA_MODEL=mistral

# For faster inference:
OLLAMA_MODEL=phi3

# For multilingual support:
OLLAMA_MODEL=qwen2.5
```

Then restart the API server.

## Install Python Dependencies

```bash
cd /Users/yash/Documents/practice/bookwith/apps/api
make configure
```

This installs `langchain-ollama` for Ollama integration.

## Start the API

```bash
cd /Users/yash/Documents/practice/bookwith/apps/api
make run
```

You should see:
```
INFO - Using Ollama embeddings: nomic-embed-text at http://localhost:11434
INFO - Application startup complete.
```

## Testing

### Test Chat Endpoint

```bash
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "test-chat-id",
    "sender_id": "91527c9d-48aa-41d0-bb85-dc96f26556a0",
    "content": "Hello! Tell me about yourself."
  }'
```

### Test Embeddings

The first embedding request will take a few seconds as the model loads into memory. Subsequent requests are fast.

## Model Recommendations

### For Development (Fast, Lower RAM)
```bash
OLLAMA_MODEL=llama3.2              # 3B params, 2GB RAM
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

### For Production (Best Quality)
```bash
OLLAMA_MODEL=llama3.1:8b           # 8B params, 8GB RAM
OLLAMA_EMBEDDING_MODEL=mxbai-embed-large
```

### For Limited Hardware
```bash
OLLAMA_MODEL=phi3                  # 3.8B params, 2.3GB RAM
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

## Available Models

### Chat Models

| Model | Size | RAM | Quality | Speed | Best For |
|-------|------|-----|---------|-------|----------|
| llama3.2 | 3B | 2GB | Good | Fast ⚡ | Development |
| phi3 | 3.8B | 2.3GB | Good | Fast ⚡ | Quick testing |
| mistral | 7B | 4GB | Excellent | Medium | Balanced |
| llama3.1:8b | 8B | 5GB | Excellent | Medium | Production |
| gemma2:9b | 9B | 6GB | Excellent | Medium | Google model |
| qwen2.5 | 7B | 4GB | Excellent | Medium | Multilingual |

### Embedding Models

| Model | Size | RAM | Quality | Best For |
|-------|------|-----|---------|----------|
| nomic-embed-text | 137M | 274MB | Good | General use |
| mxbai-embed-large | 335M | 669MB | Better | High accuracy |
| all-minilm | 22M | 45MB | Basic | Quick testing |

## Performance Tips

### 1. GPU Acceleration (Optional but Recommended)

**macOS with Apple Silicon:**
Ollama automatically uses Metal for GPU acceleration. No configuration needed!

**Linux/Windows with NVIDIA GPU:**
Install CUDA toolkit. Ollama will automatically detect and use GPU.

### 2. Memory Management

If you're running out of memory:
```bash
# Use smaller models
OLLAMA_MODEL=phi3

# Or quantized versions
ollama pull llama3.2:q4_0  # 4-bit quantization
```

### 3. Model Preloading

Keep models loaded in memory for faster responses:
```bash
# Preload chat model
ollama run llama3.2 ""

# Preload embedding model
ollama run nomic-embed-text ""
```

## Troubleshooting

### "Connection refused" Error

**Problem:** Ollama service not running

**Solution:**
```bash
# macOS/Linux
brew services restart ollama

# Or start manually
ollama serve
```

### "Model not found" Error

**Problem:** Model not downloaded

**Solution:**
```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### Slow First Request

**Problem:** Model loading into memory

**Solution:** This is normal. First request takes 5-30 seconds depending on model size. Subsequent requests are fast.

### Out of Memory

**Problem:** Model too large for available RAM

**Solution:** Use a smaller model:
```bash
OLLAMA_MODEL=phi3  # Only 2.3GB RAM needed
```

## Switching Between Providers

You can easily switch between Ollama, OpenAI, and HuggingFace by editing `.env`:

### Use Ollama (Local, Free)
```bash
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
```

### Use OpenAI (Cloud, Paid)
```bash
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai
```

### Mix Providers (Recommended)
```bash
LLM_PROVIDER=ollama              # Local chat
EMBEDDING_PROVIDER=ollama        # Local embeddings
```

Just restart the API server after changing providers.

## Uninstalling

### Remove Ollama
```bash
# macOS
brew uninstall ollama

# Linux
sudo rm -rf /usr/local/bin/ollama
```

### Remove Models (Free up disk space)
```bash
# Remove specific model
ollama rm llama3.2

# Remove all models
rm -rf ~/.ollama/models
```

## Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Available Models](https://ollama.com/library)
- [LangChain Ollama Integration](https://python.langchain.com/docs/integrations/llms/ollama)

## Comparison: Ollama vs OpenAI vs HuggingFace

| Feature | Ollama | OpenAI | HuggingFace |
|---------|--------|--------|-------------|
| Cost | Free ✅ | Paid 💰 | Free (limited) |
| Privacy | Local ✅ | Cloud ⚠️ | Cloud ⚠️ |
| Speed | Fast (GPU) | Fast | Slow (free tier) |
| Quality | Excellent | Excellent | Varies |
| Setup | Easy | Easiest | Easy |
| Rate Limits | None ✅ | Yes (paid) | Yes (free) |
| Offline | Yes ✅ | No | No |

**Recommendation:** Use Ollama for development and testing. It's free, fast, and completely private!
