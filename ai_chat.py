import requests
import json
from config import OPENAI_API_KEY, OPENAI_API_BASE, MODEL_NAME

def chat_with_ai(chat_history):
    """Send chat history to OpenAI API and get response."""
    url = f"{OPENAI_API_BASE}"  # Adjust if using a different API

    headers = {
        "api-key": OPENAI_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": chat_history
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raises an error for 4XX/5XX responses
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
