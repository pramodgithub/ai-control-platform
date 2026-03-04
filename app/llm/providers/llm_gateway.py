import json
import re
from app.llm.providers.openrouter_client import OpenRouterClient
from app.llm.providers.local_client import LocalLLMClient
from app.llm.providers.grok_client import GrokClient


class LLMGateway:

    def __init__(self):
       # self.openrouter = OpenRouterClient()
       # self.local = LocalLLMClient()
        self.groq = GrokClient()

        # Priority order
        self.providers = [
            ("groq", "groq/compound"),
            
        ]
            #("openrouter", "meta-llama/llama-3.3-70b-instruct"),
            #("openrouter", "qwen/qwen-2.5-72b-instruct"),
            #("local", "qwen2.5:14b") 
        self._active_model = None

    @property
    def model(self):
        return self._active_model

    def generate(self, prompt: str, temperature: float = 0.0):

        last_exception = None

        for provider_name, model_name in self.providers:

            try:
                print(f"Using {provider_name.upper()} → {model_name}")

                self._active_model = model_name

                if provider_name == "openrouter":
                    return self.openrouter.generate(model_name, prompt, temperature)

                elif provider_name == "groq":
                    return self.groq.generate(model_name, prompt, temperature)

                elif provider_name == "local":
                    return self.local.generate(model_name, prompt, temperature)

            except Exception as e:
                print(f"{provider_name} failed:", e)
                last_exception = e
                continue

        raise Exception(f"All providers failed: {last_exception}")

    def generate_json(self, prompt: str, temperature: float = 0.0):
        response_text = self.generate(prompt, temperature)

        try:
            return json.loads(response_text)
            
        except json.JSONDecodeError:
            # Try to extract JSON block
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)

            if json_match:
                try:
                    return json.loads(json_match.group())
                except Exception:
                    pass

            print("⚠ JSON parsing failed. Raw output:")
            print(response_text)
            raise