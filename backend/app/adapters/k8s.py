from __future__ import annotations

from abc import ABC, abstractmethod

from app.schemas.snapshot import ClusterSnapshot


class K8sAdapter(ABC):
    @abstractmethod
    async def get_cluster_snapshot(self, cluster_id: str) -> ClusterSnapshot: ...

    @abstractmethod
    async def list_events(self, cluster_id: str, minutes_back: int = 10) -> list[dict]: ...

    @abstractmethod
    async def dry_run_patch(self, cluster_id: str, namespace: str, kind: str, name: str, patch: dict) -> dict: ...
