from dataclasses import dataclass


@dataclass
class GuardContext:
    environment: str
    allow_automated_actions: bool
    protected_namespaces: set[str]
    allowed_action_types: set[str]


class K8sActionGuard:
    def validate(self, context: GuardContext, action_type: str, namespace: str | None) -> None:
        if action_type not in context.allowed_action_types:
            raise PermissionError(f"action type {action_type} not allowed")
        if not context.allow_automated_actions:
            raise PermissionError("automated actions are disabled for this cluster")
        if context.environment == "prod" and action_type in {"patch", "scale", "restart"}:
            raise PermissionError("prod actions require explicit approval path")
        if namespace and namespace in context.protected_namespaces:
            raise PermissionError(f"namespace {namespace} is protected")
