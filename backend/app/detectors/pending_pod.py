from app.detectors.base import Detector, Finding
from app.schemas.snapshot import ClusterSnapshot


class PendingPodDetector(Detector):
    def __init__(self, pending_threshold_seconds: int = 300) -> None:
        self.pending_threshold_seconds = pending_threshold_seconds

    def detect(self, snapshot: ClusterSnapshot) -> list[Finding]:
        return [
            Finding("PendingPodDetector", "warning", "scheduling", f"Pod {p.namespace}/{p.name} stuck Pending", [f"pod/{p.namespace}/{p.name}"], {"pending_seconds": p.pending_seconds}, ["Inspect FailedScheduling events and resource quotas"])
            for p in snapshot.pods
            if p.phase == "Pending" and p.pending_seconds > self.pending_threshold_seconds
        ]
