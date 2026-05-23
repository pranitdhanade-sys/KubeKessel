import pytest

from app.actions.guard import GuardContext, K8sActionGuard


def test_blocks_unsupported_action_type() -> None:
    guard = K8sActionGuard()
    context = GuardContext("staging", True, {"kube-system"}, {"patch", "scale"})
    with pytest.raises(PermissionError):
        guard.validate(context, "delete", "payments")


def test_blocks_when_automation_disabled() -> None:
    guard = K8sActionGuard()
    context = GuardContext("staging", False, set(), {"patch"})
    with pytest.raises(PermissionError):
        guard.validate(context, "patch", "payments")


def test_blocks_protected_namespace() -> None:
    guard = K8sActionGuard()
    context = GuardContext("staging", True, {"kube-system"}, {"patch"})
    with pytest.raises(PermissionError):
        guard.validate(context, "patch", "kube-system")
