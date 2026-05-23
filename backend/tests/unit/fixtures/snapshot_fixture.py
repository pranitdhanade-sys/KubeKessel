from app.schemas.snapshot import ClusterSnapshot, NodeSnapshot, PodSnapshot


def sample_snapshot() -> ClusterSnapshot:
    return ClusterSnapshot(
        cluster_id="cluster-1",
        pods=[
            PodSnapshot(namespace="payments", name="api-1", phase="Running", restart_count_10m=8),
            PodSnapshot(namespace="orders", name="worker-1", phase="Pending", pending_seconds=600),
            PodSnapshot(namespace="payments", name="api-2", phase="Running", oom_killed=True),
        ],
        nodes=[NodeSnapshot(name="node-a", cpu_requested_ratio=0.92, memory_requested_ratio=0.75)],
        events=[{"reason": "FailedScheduling"}],
    )
