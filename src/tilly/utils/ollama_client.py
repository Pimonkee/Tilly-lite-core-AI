import os
import logging

logger = logging.getLogger(__name__)

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("requests library not available. Ollama integration will be disabled.")

OLLAMA_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434") + "/api/generate"
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")  # grabs it from .env

def generate_with_ollama(prompt: str, model: str = "codellama"):
    """Generate text using Ollama local LLM"""
    if not REQUESTS_AVAILABLE:
        logger.error("Cannot use Ollama: requests library not available")
        return "Ollama integration not available"
    
    try:
        import json
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        # Only add auth header if API key is configured
        if OLLAMA_API_KEY:
            headers["Authorization"] = f"Bearer {OLLAMA_API_KEY}"

        response = requests.post(OLLAMA_URL, data=json.dumps(payload), headers=headers, timeout=30)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        logger.error(f"Ollama generation failed: {e}")
        return f"Error generating with Ollama: {str(e)}"

