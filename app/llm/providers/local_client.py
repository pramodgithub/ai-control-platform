import os
import requests


class LocalLLMClient:

    def __init__(self):
        self.base_url = os.getenv("LOCAL_LLM_URL")

    def generate(self, model: str, prompt: str, temperature: float = 0.0):
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        response = requests.post(
            self.base_url,
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            raise Exception(f"Local LLM error: {response.text}")

        data = response.json()
        return data["response"]