from langchain_core.messages import BaseMessage

from src.models.model import Model


class ModelChain(Model):
    """
    Tries models in order and returns the first successful response.

    If a model fails, the next model is tried.
    """

    def __init__(self, models: list[Model]) -> None:
        if not models:
            raise ValueError("At least one model must be provided.")

        self.models = models

    def generate(self, messages: list[BaseMessage]) -> str:
        errors: list[tuple[str, Exception]] = []

        for model in self.models:
            model_name = type(model).__name__

            try:
                return model.generate(messages)

            except Exception as error:
                errors.append((model_name, error))

                print(
                    f"\n{model_name} failed: {error}"
                    f"\nTrying next model..."
                )

        details = "\n".join(
            f"- {name}: {error}"
            for name, error in errors
        )

        raise RuntimeError(
            "All configured model providers failed:\n"
            f"{details}"
        )