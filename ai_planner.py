from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlannedAction:
    action: str
    arguments: dict


class AIPlanner:
    """Rule-based placeholder for local LLM planner integration."""

    def plan(self, instruction: str) -> list[PlannedAction]:
        normalized = instruction.lower().strip()
        actions: list[PlannedAction] = []

        if "open" in normalized or "otev" in normalized:
            actions.append(PlannedAction(action="open_app", arguments={"name": "browser"}))
        if "klik" in normalized:
            actions.append(PlannedAction(action="click_text", arguments={"target_text": "OK"}))
        if "write" in normalized or "napi" in normalized:
            actions.append(PlannedAction(action="type", arguments={"text": instruction}))
        if "if" in normalized or "pokud" in normalized:
            actions.append(PlannedAction(action="condition_check", arguments={"mode": "text_presence"}))
        if "loop" in normalized or "opak" in normalized:
            actions.append(PlannedAction(action="repeat", arguments={"times": 3}))

        if not actions:
            actions.append(PlannedAction(action="analyze_screen", arguments={}))
        return actions

    def suggest_timeless_features(self) -> list[str]:
        """Modern, long-horizon capabilities for roadmap discussions."""
        return [
            "Self-healing selectors combining UIA + OCR + visual embeddings",
            "Local semantic memory of repeated workflows with vector search",
            "Policy engine: allow/deny actions per app, window title, and file path",
            "Deterministic replay mode with dry-run diff before execution",
            "Signed workflow packages with integrity checks and rollback",
            "On-device federated learning of user preferences without cloud raw-data upload",
        ]
