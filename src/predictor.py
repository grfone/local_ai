from langchain_core.messages import BaseMessage

from src.models.messages import Message
from src.providers.base import BaseProvider
from src.providers.ollama import OllamaProvider
from src.providers.minimax import MiniMaxProvider


class Predictor:

    def __init__(
        self,
        provider: str = "Ollama",
        model: str = "qwen3.5:4b",
    ):
        self.provider = self._create_provider(provider, model)

    def predict(self, messages: list[BaseMessage]) -> str:
        provider_messages = self._to_provider_messages(messages)

        return self.provider.predict(provider_messages)

    @staticmethod
    def _create_provider(
        provider: str,
        model: str,
    ) -> BaseProvider:
        if provider == "Ollama":
            return OllamaProvider(model=model)

        if provider == "MiniMax":
            return MiniMaxProvider(model=model)

        raise ValueError(
            f"Unknown provider: {provider}"
        )

    @staticmethod
    def _to_provider_messages(
        messages: list[BaseMessage],
    ) -> list[Message]:

        role_map = {
            "human": "user",
            "ai": "assistant",
            "system": "system",
        }

        return [
            Message(
                role=role_map[message.type],
                content=message.content,
            )
            for message in messages
        ]