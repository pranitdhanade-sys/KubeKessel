from app.detectors.base import Detector, Finding
from app.schemas.snapshot import ClusterSnapshot


class OOMKillDetector(Detector):
    def detect(self, snapshot: ClusterSnapshot) -> list[Finding]:
        return [
            Finding("OOMKillDetector", "high", "resource", f"Pod {p.namespace}/{p.name} had OOM kill", [f"pod/{p.namespace}/{p.name}"], {"oom_killed": True}, ["Raise memory limit or reduce memory footprint"])
            for p in snapshot.pods
            if p.oom_killed
        ]
