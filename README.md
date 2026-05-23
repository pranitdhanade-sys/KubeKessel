# KubeKessel

Production-grade scaffold for a Smart Kubernetes Monitoring Assistant.

## Implemented in this scaffold
- Backend project skeleton (FastAPI-oriented) with SQLAlchemy + Alembic layout.
- Core relational models (`Cluster`, `Finding`, `AnalysisReport`, `RecommendedAction`, `AuditLog`).
- Initial migration with TimescaleDB hypertable bootstrap stubs.
- Ports/adapters base interfaces for Kubernetes and Prometheus.
- `K8sActionGuard` safety contract and unit tests.
- `ClusterSnapshot` schema and snapshot builder.
- Initial detectors: CrashLoop, OOMKill, PendingPod, ResourcePressure with fixture-based unit tests.
- Redis Streams event watcher publisher/consumer primitives.
- Agent core placeholder for iterative analysis orchestration.

## Next milestones
- Wire concrete `kubernetes-asyncio` and PromQL adapters.
- Add FastAPI endpoints and Celery tasks.
- Expand migrations for remaining tables and Timescale continuous aggregates.
- Add integration tests with `pytest-kind`.
