import os
from openai import OpenAI
from .provider import EmbeddingProvider

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OpenAIEmbeddingProvider(EmbeddingProvider):

    def embed(self, text: str) -> list[float]:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding