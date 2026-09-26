from abc import ABC, abstractmethod

from langchain_core.messages import BaseMessage


class Model(ABC):
    """
    Application-level interface for language models.

    The rest of the application does not know which provider
    implements this interface.
    """

    @abstractmethod
    def generate(
        self,
        messages: list[BaseMessage],
    ) -> str:
        """
        Generate a model response from the supplied messages.
        """
        raise NotImplementedError