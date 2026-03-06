# OmniMind Automator (MVP+ Skeleton)

Desktop prototype for **local-first AI automation** combining macro recording, OCR, adaptive playback and a roadmap for modern timeless capabilities.

## Project structure

- `main.py` – app entrypoint.
- `gui/app.py` – Tkinter desktop UI (agent list, step preview, AI panel).
- `recorder.py` – hybrid recorder skeleton (events + screenshot interval) with sensitive-input redaction.
- `player.py` – adaptive step player with text-based target fallback.
- `ocr_engine.py` – OCR abstraction with pluggable backend (Tesseract default).
- `ai_planner.py` – placeholder planner for natural-language commands + timeless feature suggestions.
- `workflow.py` – workflow domain model (versioning, IF/loop metadata, fingerprinting, JSON persistence).
- `safety.py` – local safety guard for redacting sensitive values before persistence.
- `tests/` – unit tests for player, OCR, safety guard, and workflow repository.

## Run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```


## Windows one-click style installation (with desktop shortcut)

1. Download/clone the repository from GitHub.
2. Open **PowerShell as Administrator** (recommended).
3. Run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\install_windows.ps1
```

After installation:
- files are copied to `%LOCALAPPDATA%\OmniMindAutomator`
- dependencies are installed into a local virtual environment
- a desktop shortcut **OmniMind Automator** is created for quick launch

You can also start manually from install folder via `launch_omnimind.bat`.

## Testing

```bash
pytest -q
```

## Architecture notes

- **MVP v1 focus:** recording click/key events, periodic screenshots, simple editable steps.
- **Adaptive playback:** steps can contain `target_text`; runtime locator resolves element position before clicking.
- **OCR pipeline:** wrapped in `OCREngine` to switch between Tesseract/PaddleOCR without affecting core logic.
- **Workflow durability:** each workflow carries semantic tags, version, and SHA-256 fingerprint for integrity checks.
- **Local privacy:** keypress values pass through `SensitiveDataGuard` so card-like numbers/emails/password patterns are redacted.
- **AI planner path:** currently rule-based; prepared for Ollama-backed local LLM in v2.

## Modern & timeless features proposed (next iterations)

1. Self-healing selectors (UIA + OCR + visual embeddings).
2. Policy engine (allow/deny by app/window/path).
3. Deterministic dry-run with visual diff before execution.
4. Signed workflow packages + rollback.
5. Local semantic memory with vector retrieval.
6. On-device federated personalization without raw-data cloud export.
