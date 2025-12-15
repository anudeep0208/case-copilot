import requests
import json


class LocalLLMAdapter:
    def __init__(
        self,
        model: str = "gemma3:1b",
        base_url: str = "http://localhost:11434"
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def complete(self, prompt: str) -> str:
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()

        output = ""

        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if "message" in data:
                    output += data["message"].get("content", "")

        return output.strip()
