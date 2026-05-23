from app.detectors.base import Detector, Finding
from app.schemas.snapshot import ClusterSnapshot


class ResourcePressureDetector(Detector):
    def __init__(self, cpu_threshold: float = 0.85, memory_threshold: float = 0.90) -> None:
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold

    def detect(self, snapshot: ClusterSnapshot) -> list[Finding]:
        findings = []
        for node in snapshot.nodes:
            if node.cpu_requested_ratio > self.cpu_threshold or node.memory_requested_ratio > self.memory_threshold:
                findings.append(Finding("ResourcePressureDetector", "high", "resource", f"Node {node.name} under resource pressure", [f"node/{node.name}"], {"cpu_requested_ratio": node.cpu_requested_ratio, "memory_requested_ratio": node.memory_requested_ratio}, ["Scale node pool", "Right-size requests/limits"]))
        return findings
