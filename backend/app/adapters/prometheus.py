from __future__ import annotations

from abc import ABC, abstractmethod


class PrometheusAdapter(ABC):
    @abstractmethod
    async def query_range(self, cluster_id: str, promql: str, start: str, end: str, step: str) -> dict: ...

    @abstractmethod
    async def health(self, cluster_id: str) -> bool: ...
