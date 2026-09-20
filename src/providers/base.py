from abc import ABC, abstractmethod

from src.models.messages import Message


class BaseProvider(ABC):

    @abstractmethod
    def predict(
        self,
        messages: list[Message],
    ) -> str:
        """Send messages to the provider and return the model response."""
        raise NotImplementedError