import os
import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")  # grabs it from .env

def generate_with_ollama(prompt: str, model: str = "codellama"):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OLLAMA_API_KEY}"  # use key if Ollama requires it
    }

    response = requests.post(OLLAMA_URL, data=json.dumps(payload), headers=headers)
    response.raise_for_status()
    return response.json().get("response", "")
