# src/instances/instance.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentInstance:
    """
    Represents one agent instance.

    An instance contains the identity and configuration that make it
    distinct from other instances running on the same graph/workflow.

    Persistence and graph execution are handled by other components.
    """

    id: str
    name: str

    created_at: str
    updated_at: str

    thread_id: str

    persistent: bool

    configuration: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------

    def set_config(
        self,
        key: str,
        value: Any,
    ) -> None:
        """Set an instance configuration value."""
        self.configuration[key] = value

    def get_config(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """Get an instance configuration value."""
        return self.configuration.get(key, default)

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
            f"AgentInstance("
            f"id={self.id!r}, "
            f"name={self.name!r}, "
            f"thread_id={self.thread_id!r}, "
            f"persistent={self.persistent!r}"
            f")"
        )