import requests
import json

url = "http://localhost:11434/api/chat"

payload = {
    "model": "gemma3:1b",
    "messages": [
        {"role": "user", "content": "Hello!"}
    ]
}

response = requests.post(url, json=payload, stream=True)
response.raise_for_status()

final_output = ""

for line in response.iter_lines():
    if line:
        data = json.loads(line)
        if "message" in data:
            final_output += data["message"].get("content", "")

print(final_output)
