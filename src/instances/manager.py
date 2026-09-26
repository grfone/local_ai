# src/instances/manager.py

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from src.instances.instance import AgentInstance


class InstanceManager:
    """
    Manages the lifecycle and persistence of agent instances.

    The manager is responsible for:
    - Creating instances
    - Loading instances
    - Listing persistent instances
    - Updating instances
    - Deleting instances
    - Persisting instance metadata

    It does not execute the graph or manage conversations directly.
    """

    def __init__(
        self,
        storage_path: str | Path = ".data/instances",
    ) -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    def create(
        self,
        name: str,
        persistent: bool = True,
        configuration: dict | None = None,
    ) -> AgentInstance:
        """
        Create a new agent instance.

        Persistent instances are written to disk.

        Non-persistent instances exist only in memory and are not
        written to disk.
        """

        now = self._now()

        instance = AgentInstance(
            id=str(uuid4()),
            name=name,
            created_at=now,
            updated_at=now,
            thread_id=str(uuid4()),
            persistent=persistent,
            configuration=configuration or {},
        )

        if persistent:
            self._save(instance)

        return instance

    # ------------------------------------------------------------------
    # Get
    # ------------------------------------------------------------------

    def get(
        self,
        instance_id: str,
    ) -> AgentInstance | None:
        """
        Load a persistent instance by ID.

        Returns None when the instance does not exist.
        """

        path = self._instance_path(instance_id)

        if not path.exists():
            return None

        return self._load(path)

    # ------------------------------------------------------------------
    # List
    # ------------------------------------------------------------------

    def list(self) -> list[AgentInstance]:
        """
        Return all persistent instances.

        Instances are ordered by most recently updated first.
        """

        instances: list[AgentInstance] = []

        for path in self.storage_path.glob("*.json"):
            try:
                instance = self._load(path)
                instances.append(instance)

            except (
                OSError,
                json.JSONDecodeError,
                KeyError,
                TypeError,
                ValueError,
            ):
                # Ignore malformed instance files for now.
                # This can later be replaced with proper logging.
                continue

        instances.sort(
            key=lambda instance: instance.updated_at,
            reverse=True,
        )

        return instances

    # ------------------------------------------------------------------
    # Save / Update
    # ------------------------------------------------------------------

    def save(
        self,
        instance: AgentInstance,
    ) -> None:
        """
        Persist an existing instance.

        Non-persistent instances are ignored.
        """

        if not instance.persistent:
            return

        instance.updated_at = self._now()

        self._save(instance)

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def delete(
        self,
        instance_id: str,
    ) -> bool:
        """
        Delete a persistent instance.

        Returns True when the instance existed and was deleted.

        Returns False when no instance with the given ID exists.
        """

        path = self._instance_path(instance_id)

        if not path.exists():
            return False

        path.unlink()

        return True

    # ------------------------------------------------------------------
    # Internal persistence
    # ------------------------------------------------------------------

    def _save(
        self,
        instance: AgentInstance,
    ) -> None:
        path = self._instance_path(instance.id)

        data = {
            "id": instance.id,
            "name": instance.name,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
            "thread_id": instance.thread_id,
            "persistent": instance.persistent,
            "configuration": instance.configuration,
        }

        path.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )

    def _load(
        self,
        path: Path,
    ) -> AgentInstance:
        data = json.loads(
            path.read_text(
                encoding="utf-8",
            )
        )

        return AgentInstance(
            id=data["id"],
            name=data["name"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            thread_id=data["thread_id"],
            persistent=data["persistent"],
            configuration=data.get(
                "configuration",
                {},
            ),
        )

    # ------------------------------------------------------------------
    # Paths
    # ------------------------------------------------------------------

    def _instance_path(
        self,
        instance_id: str,
    ) -> Path:
        return self.storage_path / f"{instance_id}.json"

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()