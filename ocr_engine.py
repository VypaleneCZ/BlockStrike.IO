from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass
class OCRResult:
    text: str
    confidence: float


class OCREngine:
    """Thin wrapper around OCR backend (Paddle/Tesseract ready)."""

    def __init__(self, backend: Callable[[str], list[tuple[str, float]]] | None = None) -> None:
        self.backend = backend or self._default_backend

    def extract_text(self, image_path: str, min_confidence: float = 0.5) -> list[OCRResult]:
        raw = self.backend(image_path)
        return [
            OCRResult(text=text.strip(), confidence=conf)
            for text, conf in raw
            if text.strip() and conf >= min_confidence
        ]

    @staticmethod
    def _default_backend(image_path: str) -> list[tuple[str, float]]:
        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            return []

        content = pytesseract.image_to_data(Image.open(image_path), output_type=pytesseract.Output.DICT)
        records: list[tuple[str, float]] = []
        for text, conf in zip(content.get("text", []), content.get("conf", [])):
            try:
                confidence = float(conf) / 100.0
            except (TypeError, ValueError):
                confidence = 0.0
            records.append((text, confidence))
        return records
