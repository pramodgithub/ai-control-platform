import os
from google import genai
from dotenv import load_dotenv
from .provider import EmbeddingProvider
load_dotenv()

class GeminiEmbeddingProvider(EmbeddingProvider):

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")

        self.client = genai.Client(api_key=api_key)

    def embed(self, text: str) -> list[float]:
        response = self.client.models.embed_content(
            model="models/gemini-embedding-001",
            contents=text
        )

        return response.embeddings[0].values