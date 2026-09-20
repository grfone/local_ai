import os

import requests
from dotenv import load_dotenv

from src.models.messages import Message
from src.providers.base import BaseProvider


class MiniMaxProvider(BaseProvider):

    API_URL = "https://api.minimax.io/v1/text/chatcompletion_v2"

    def __init__(self, model: str = "M3"):
        # Load API key from .env
        load_dotenv()

        self.model = f"MiniMax-{model}"
        self.api_key = os.getenv("MINIMAX_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "MINIMAX_API_KEY is missing. "
                "Add it to your .env file."
            )

    def predict(self, messages: list[Message]) -> str:
        # Convert our messages to MiniMax format
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in messages
            ],
        }

        response = requests.post(
            self.API_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()
        base_resp = data.get("base_resp", {})

        if base_resp.get("status_code", 0) != 0:
            raise RuntimeError(
                f"MiniMax API error: "
                f"{base_resp.get('status_msg', 'Unknown error')}"
            )

        choices = data.get("choices")

        if not choices:
            raise RuntimeError("MiniMax returned no choices.")

        return choices[0]["message"]["content"]