from __future__ import annotations

from dataclasses import dataclass
from time import sleep
from typing import Protocol


class InputBackend(Protocol):
    def click(self, x: int, y: int, button: str = "left") -> None: ...

    def typewrite(self, text: str) -> None: ...


class ObjectLocator(Protocol):
    def find_by_text(self, text: str) -> tuple[int, int] | None: ...


@dataclass
class PlayStep:
    action: str
    payload: dict


class AdaptivePlayer:
    """Replays steps and can target controls by OCR/UI text labels instead of static coordinates."""

    def __init__(self, input_backend: InputBackend, locator: ObjectLocator) -> None:
        self.input_backend = input_backend
        self.locator = locator

    def play(self, steps: list[PlayStep], speed: float = 1.0) -> None:
        for step in steps:
            delay = float(step.payload.get("delay", 0)) / max(speed, 0.1)
            if delay:
                sleep(delay)

            if step.action == "click":
                self._play_click(step.payload)
            elif step.action == "type":
                self.input_backend.typewrite(step.payload["text"])

    def _play_click(self, payload: dict) -> None:
        target_text = payload.get("target_text")
        if target_text:
            pos = self.locator.find_by_text(target_text)
            if pos:
                self.input_backend.click(pos[0], pos[1], button=payload.get("button", "left"))
                return
        self.input_backend.click(payload["x"], payload["y"], button=payload.get("button", "left"))
