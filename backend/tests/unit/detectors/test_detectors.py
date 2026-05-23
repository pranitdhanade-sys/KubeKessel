from app.detectors.crash_loop import CrashLoopDetector
from app.detectors.oom_kill import OOMKillDetector
from app.detectors.pending_pod import PendingPodDetector
from app.detectors.resource_pressure import ResourcePressureDetector
from tests.unit.fixtures.snapshot_fixture import sample_snapshot


def test_crash_loop_detector() -> None:
    findings = CrashLoopDetector(restart_threshold=5).detect(sample_snapshot())
    assert len(findings) == 1
    assert findings[0].detector_name == "CrashLoopDetector"


def test_oom_detector() -> None:
    findings = OOMKillDetector().detect(sample_snapshot())
    assert len(findings) == 1
    assert findings[0].detector_name == "OOMKillDetector"


def test_pending_detector() -> None:
    findings = PendingPodDetector(pending_threshold_seconds=300).detect(sample_snapshot())
    assert len(findings) == 1
    assert findings[0].detector_name == "PendingPodDetector"


def test_resource_pressure_detector() -> None:
    findings = ResourcePressureDetector(cpu_threshold=0.85, memory_threshold=0.9).detect(sample_snapshot())
    assert len(findings) == 1
    assert findings[0].detector_name == "ResourcePressureDetector"
