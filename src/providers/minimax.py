import os

import requests
from dotenv import load_dotenv
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
)

from src.models.model import Model


class MiniMaxModel(Model):

    API_URL = "https://api.minimax.io/v1/text/chatcompletion_v2"

    def __init__(
        self,
        model: str = "M3",
    ):
        load_dotenv()

        self.model = f"MiniMax-{model}"
        self.api_key = os.getenv("MINIMAX_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "MINIMAX_API_KEY is missing. "
                "Add it to your .env file."
            )

    def generate(
        self,
        messages: list[BaseMessage],
    ) -> str:
        payload = {
            "model": self.model,
            "messages": [
                self._to_minimax_message(message)
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

        base_resp = data.get(
            "base_resp",
            {},
        )

        if base_resp.get("status_code", 0) != 0:
            raise RuntimeError(
                "MiniMax API error: "
                f"{base_resp.get('status_msg', 'Unknown error')}"
            )

        choices = data.get("choices")

        if not choices:
            raise RuntimeError(
                "MiniMax returned no choices."
            )

        return str(
            choices[0]["message"]["content"]
        )

    @staticmethod
    def _to_minimax_message(
        message: BaseMessage,
    ) -> dict[str, str]:
        if isinstance(message, HumanMessage):
            role = "user"

        elif isinstance(message, AIMessage):
            role = "assistant"

        elif isinstance(message, SystemMessage):
            role = "system"

        else:
            raise TypeError(
                "Unsupported message type for MiniMax: "
                f"{type(message).__name__}"
            )

        return {
            "role": role,
            "content": str(message.content),
        }
