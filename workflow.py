from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path
from typing import Any


@dataclass
class Condition:
    """Simple IF condition for MVP+ editor support."""

    if_text_visible: str
    then_action: str


@dataclass
class Loop:
    repeat: int = 1


@dataclass
class WorkflowStep:
    action: str
    payload: dict[str, Any]
    condition: Condition | None = None
    loop: Loop | None = None


@dataclass
class AgentWorkflow:
    name: str
    app_hint: str = ""
    tags: list[str] = field(default_factory=list)
    version: int = 1
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    steps: list[WorkflowStep] = field(default_factory=list)

    def add_step(self, step: WorkflowStep) -> None:
        self.steps.append(step)
        self.bump_version()

    def bump_version(self) -> None:
        self.version += 1
        self.updated_at = datetime.now(UTC).isoformat()

    def fingerprint(self) -> str:
        canonical = json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AgentWorkflow":
        steps = []
        for item in payload.get("steps", []):
            condition = item.get("condition")
            loop = item.get("loop")
            steps.append(
                WorkflowStep(
                    action=item["action"],
                    payload=item.get("payload", {}),
                    condition=Condition(**condition) if condition else None,
                    loop=Loop(**loop) if loop else None,
                )
            )
        return cls(
            name=payload["name"],
            app_hint=payload.get("app_hint", ""),
            tags=payload.get("tags", []),
            version=payload.get("version", 1),
            created_at=payload.get("created_at", datetime.now(UTC).isoformat()),
            updated_at=payload.get("updated_at", datetime.now(UTC).isoformat()),
            steps=steps,
        )


class WorkflowRepository:
    """Local JSON workflow store with deterministic naming."""

    def __init__(self, root: str = "data/workflows") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, workflow: AgentWorkflow) -> Path:
        name = self._safe_name(workflow.name)
        path = self.root / f"{name}.json"
        path.write_text(json.dumps(workflow.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def load(self, name: str) -> AgentWorkflow:
        path = self.root / f"{self._safe_name(name)}.json"
        return AgentWorkflow.from_dict(json.loads(path.read_text(encoding="utf-8")))

    @staticmethod
    def _safe_name(name: str) -> str:
        return "".join(ch.lower() if ch.isalnum() else "_" for ch in name).strip("_") or "agent"
