from __future__ import annotations

import re


class SensitiveDataGuard:
    """Redacts common sensitive inputs before they are persisted in recordings."""

    PATTERNS = [
        re.compile(r"\b\d{12,19}\b"),  # card-like
        re.compile(r"[\w.-]+@[\w.-]+\.[A-Za-z]{2,}"),
        re.compile(r"(?i)(password|heslo)\s*[:=]\s*\S+"),
    ]

    def redact(self, value: str) -> str:
        result = value
        for pattern in self.PATTERNS:
            result = pattern.sub("[REDACTED]", result)
        return result
