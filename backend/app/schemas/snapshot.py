from dataclasses import dataclass, field


@dataclass
class PodSnapshot:
    namespace: str
    name: str
    phase: str
    restart_count_10m: int = 0
    pending_seconds: int = 0
    oom_killed: bool = False


@dataclass
class NodeSnapshot:
    name: str
    cpu_requested_ratio: float
    memory_requested_ratio: float
    ready: bool = True


@dataclass
class ClusterSnapshot:
    cluster_id: str
    pods: list[PodSnapshot] = field(default_factory=list)
    nodes: list[NodeSnapshot] = field(default_factory=list)
    events: list[dict] = field(default_factory=list)
