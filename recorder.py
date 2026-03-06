from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from threading import Event, Thread
from time import sleep
from typing import Any

from safety import SensitiveDataGuard


@dataclass
class RecordedStep:
    action: str
    payload: dict[str, Any]
    timestamp: float


@dataclass
class RecordingSession:
    name: str
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    steps: list[RecordedStep] = field(default_factory=list)
    screenshots: list[str] = field(default_factory=list)


class HybridRecorder:
    """MVP skeleton for hybrid recording (events + periodic screenshots)."""

    def __init__(
        self,
        screenshot_dir: str = "data/screenshots",
        interval_ms: int = 500,
        guard: SensitiveDataGuard | None = None,
    ) -> None:
        self.screenshot_dir = Path(screenshot_dir)
        self.interval_ms = interval_ms
        self._running = Event()
        self._thread: Thread | None = None
        self.session: RecordingSession | None = None
        self.guard = guard or SensitiveDataGuard()

    def start(self, session_name: str) -> RecordingSession:
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.session = RecordingSession(name=session_name)
        self._running.set()
        self._thread = Thread(target=self._capture_loop, daemon=True)
        self._thread.start()
        return self.session

    def stop(self) -> RecordingSession:
        if not self.session:
            raise RuntimeError("Recording has not been started")
        self._running.clear()
        if self._thread:
            self._thread.join(timeout=2)
        return self.session

    def record_click(self, x: int, y: int, button: str = "left") -> None:
        self._append_step("click", {"x": x, "y": y, "button": button})

    def record_keypress(self, key: str) -> None:
        safe_key = self.guard.redact(key)
        self._append_step("keypress", {"key": safe_key})

    def _append_step(self, action: str, payload: dict[str, Any]) -> None:
        if not self.session:
            raise RuntimeError("Recording session is not active")
        self.session.steps.append(
            RecordedStep(action=action, payload=payload, timestamp=datetime.utcnow().timestamp())
        )

    def _capture_loop(self) -> None:
        while self._running.is_set():
            if self.session:
                filename = self.screenshot_dir / f"{self.session.name}_{len(self.session.screenshots):04d}.png"
                filename.touch(exist_ok=True)
                self.session.screenshots.append(str(filename))
            sleep(self.interval_ms / 1000)
