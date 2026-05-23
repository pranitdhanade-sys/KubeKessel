from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Cluster(Base):
    __tablename__ = "clusters"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    environment: Mapped[str] = mapped_column(String(32), nullable=False)
    kubeconfig_ref: Mapped[str] = mapped_column(String(512), nullable=False)
    prometheus_endpoint: Mapped[str] = mapped_column(String(512), nullable=False)
    allow_automated_actions: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    action_approval_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    alert_namespaces: Mapped[list[str]] = mapped_column(ARRAY(String(128)), default=list)
    ignore_namespaces: Mapped[list[str]] = mapped_column(ARRAY(String(128)), default=list)
    health_score: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    health_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    cluster_id: Mapped[str] = mapped_column(ForeignKey("clusters.id"), nullable=False)
    detector_name: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    category: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    affected_resources: Mapped[dict] = mapped_column(JSON, nullable=False)
    evidence: Mapped[dict] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(16), default="open", nullable=False)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    occurrence_count: Mapped[int] = mapped_column(default=1, nullable=False)
    analysis_id: Mapped[str | None] = mapped_column(ForeignKey("analysis_reports.id"), nullable=True)
    embedding: Mapped[str | None] = mapped_column(Text, nullable=True)


class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    finding_id: Mapped[str] = mapped_column(ForeignKey("findings.id"), nullable=False)
    cluster_id: Mapped[str] = mapped_column(ForeignKey("clusters.id"), nullable=False)
    hypotheses: Mapped[list[dict]] = mapped_column(JSON, nullable=False)
    blast_radius: Mapped[dict] = mapped_column(JSON, nullable=False)
    recommended_actions: Mapped[list[dict]] = mapped_column(JSON, nullable=False)
    confidence_overall: Mapped[float] = mapped_column(Float, nullable=False)
    agent_iterations: Mapped[int] = mapped_column(nullable=False)
    signals_used: Mapped[list[str]] = mapped_column(ARRAY(String(128)), default=list)
    claude_thread_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class RecommendedAction(Base):
    __tablename__ = "recommended_actions"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    analysis_id: Mapped[str] = mapped_column(ForeignKey("analysis_reports.id"), nullable=False)
    cluster_id: Mapped[str] = mapped_column(ForeignKey("clusters.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    action_type: Mapped[str] = mapped_column(String(64), nullable=False)
    kubectl_commands: Mapped[list[str]] = mapped_column(ARRAY(Text), default=list)
    manifest_patch: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    risk_level: Mapped[str] = mapped_column(String(16), nullable=False)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(String(16), default="pending")
    approved_by: Mapped[str | None] = mapped_column(String(128), nullable=True)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    executed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    outcome: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    cluster_id: Mapped[str] = mapped_column(ForeignKey("clusters.id"), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(128), nullable=False)
    resource_name: Mapped[str] = mapped_column(String(255), nullable=False)
    namespace: Mapped[str | None] = mapped_column(String(128), nullable=True)
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    api_call: Mapped[str] = mapped_column(Text, nullable=False)
    before_state: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    after_state: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
