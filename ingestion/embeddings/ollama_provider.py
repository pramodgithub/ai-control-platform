"""Ollama-based embedding provider (simple stub)."""

from .provider import EmbeddingProvider


class OllamaProvider(EmbeddingProvider):
    def __init__(self, endpoint: str = None):
        self.endpoint = endpoint

    def embed(self, texts):
        # TODO: implement real Ollama calls
        return [[0.0] * 768 for _ in texts]
