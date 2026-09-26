from dataclasses import dataclass

from src.models.model import Model


@dataclass
class AgentContext:
    """
    Runtime dependencies for one graph execution.

    This is not persisted conversation state.
    """

    model: Model