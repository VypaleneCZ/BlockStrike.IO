from ocr_engine import OCREngine


def test_ocr_engine_filters_by_confidence() -> None:
    backend = lambda _: [("Odeslat", 0.95), ("", 0.99), ("Low", 0.1)]
    engine = OCREngine(backend=backend)

    results = engine.extract_text("dummy.png", min_confidence=0.5)

    assert len(results) == 1
    assert results[0].text == "Odeslat"
