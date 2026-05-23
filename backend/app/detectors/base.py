from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.schemas.snapshot import ClusterSnapshot


@dataclass
class Finding:
    detector_name: str
    severity: str
    category: str
    title: str
    affected_resources: list[str]
    evidence: dict
    suggested_actions: list[str]


class Detector(ABC):
    @abstractmethod
    def detect(self, snapshot: ClusterSnapshot) -> list[Finding]: ...
