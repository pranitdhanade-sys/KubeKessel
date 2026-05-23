from app.detectors.base import Detector, Finding
from app.schemas.snapshot import ClusterSnapshot


class CrashLoopDetector(Detector):
    def __init__(self, restart_threshold: int = 5) -> None:
        self.restart_threshold = restart_threshold

    def detect(self, snapshot: ClusterSnapshot) -> list[Finding]:
        findings = []
        for pod in snapshot.pods:
            if pod.restart_count_10m > self.restart_threshold:
                findings.append(Finding("CrashLoopDetector", "high", "resource", f"Pod {pod.namespace}/{pod.name} restart spike", [f"pod/{pod.namespace}/{pod.name}"], {"restart_count_10m": pod.restart_count_10m}, ["Inspect container logs", "Check recent rollout or config changes"]))
        return findings
