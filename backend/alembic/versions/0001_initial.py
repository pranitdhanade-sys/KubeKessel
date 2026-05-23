from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    op.create_table("clusters", sa.Column("id", sa.UUID(), primary_key=True), sa.Column("name", sa.String(128), unique=True, nullable=False), sa.Column("environment", sa.String(32), nullable=False), sa.Column("kubeconfig_ref", sa.String(512), nullable=False), sa.Column("prometheus_endpoint", sa.String(512), nullable=False), sa.Column("allow_automated_actions", sa.Boolean(), nullable=False, server_default=sa.false()), sa.Column("action_approval_required", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("alert_namespaces", sa.ARRAY(sa.String(128))), sa.Column("ignore_namespaces", sa.ARRAY(sa.String(128))), sa.Column("health_score", sa.Float(), nullable=False, server_default="100"), sa.Column("health_checked_at", sa.DateTime(timezone=True)))
    op.execute("""
    CREATE TABLE pod_metrics(time TIMESTAMPTZ NOT NULL, cluster_id UUID NOT NULL, namespace TEXT NOT NULL, pod_name TEXT NOT NULL, container_name TEXT NOT NULL, cpu_usage DOUBLE PRECISION, memory_usage DOUBLE PRECISION, restart_count INTEGER, anomaly_score DOUBLE PRECISION);
    CREATE TABLE node_metrics(time TIMESTAMPTZ NOT NULL, cluster_id UUID NOT NULL, node_name TEXT NOT NULL, cpu_usage DOUBLE PRECISION, memory_usage DOUBLE PRECISION, disk_usage DOUBLE PRECISION, condition_flags JSONB);
    CREATE TABLE namespace_quota(time TIMESTAMPTZ NOT NULL, cluster_id UUID NOT NULL, namespace TEXT NOT NULL, resource TEXT NOT NULL, used DOUBLE PRECISION, limit_value DOUBLE PRECISION);
    CREATE EXTENSION IF NOT EXISTS timescaledb;
    SELECT create_hypertable('pod_metrics', 'time', if_not_exists => TRUE);
    SELECT create_hypertable('node_metrics', 'time', if_not_exists => TRUE);
    SELECT create_hypertable('namespace_quota', 'time', if_not_exists => TRUE);
    """)

def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS namespace_quota;")
    op.execute("DROP TABLE IF EXISTS node_metrics;")
    op.execute("DROP TABLE IF EXISTS pod_metrics;")
    op.drop_table("clusters")
