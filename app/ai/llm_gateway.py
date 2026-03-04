import json
import os
from google import genai


class LLMGateway:
    def __init__(self, model=None, temperature=0.0):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = model or os.getenv("LLM_MODEL", "gemini-3-flash-preview")
        self.temperature = temperature

    def generate(self, prompt: str) -> str:
        """
        Generate plain text response from LLM.
        Used for clause filtering or non-JSON tasks.
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "temperature": self.temperature
            }
        )

        if not response.text:
            raise ValueError("LLM returned empty response")

        return response.text.strip()
        
    def generate_json(self, prompt: str) -> dict:
        """
        Generate structured JSON response from LLM.
        """
       
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "temperature": self.temperature,
                "response_mime_type": "application/json"
            }
        )

        if not response.text:
            raise ValueError("LLM returned empty response")

        return json.loads(response.text)