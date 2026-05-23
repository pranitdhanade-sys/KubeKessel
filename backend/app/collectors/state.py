from app.schemas.snapshot import ClusterSnapshot, NodeSnapshot, PodSnapshot


class ClusterSnapshotBuilder:
    def build(self, cluster_id: str, pod_rows: list[dict], node_rows: list[dict], events: list[dict]) -> ClusterSnapshot:
        pods = [
            PodSnapshot(
                namespace=row["namespace"],
                name=row["name"],
                phase=row.get("phase", "Unknown"),
                restart_count_10m=row.get("restart_count_10m", 0),
                pending_seconds=row.get("pending_seconds", 0),
                oom_killed=row.get("oom_killed", False),
            )
            for row in pod_rows
        ]
        nodes = [
            NodeSnapshot(
                name=row["name"],
                cpu_requested_ratio=row.get("cpu_requested_ratio", 0.0),
                memory_requested_ratio=row.get("memory_requested_ratio", 0.0),
                ready=row.get("ready", True),
            )
            for row in node_rows
        ]
        return ClusterSnapshot(cluster_id=cluster_id, pods=pods, nodes=nodes, events=events)
