from src.models.model import Model
from src.providers.chain import ModelChain
from src.providers.minimax import MiniMaxModel
from src.providers.ollama import OllamaModel


class ProviderFactory:
    """
    Creates the model used by the application.

    Models are tried in the order defined below.
    """

    @staticmethod
    def create() -> Model:
        models = [
            MiniMaxModel(),
            OllamaModel(),
        ]

        return ModelChain(models)
