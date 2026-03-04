import os
from .openai_provider import OpenAIEmbeddingProvider
from .gemini_provider import GeminiEmbeddingProvider
# from .ollama_provider import OllamaEmbeddingProvider  (add later)

def get_embedding_provider():
    provider = os.getenv("EMBEDDING_PROVIDER", "gemini")

    if provider == "openai":
        return OpenAIEmbeddingProvider()
    elif provider == "gemini":
        
        return GeminiEmbeddingProvider()
    # elif provider == "ollama":
    #     return OllamaEmbeddingProvider()
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")