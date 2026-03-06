@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo [OmniMind] Virtual environment not found. Run scripts\install_windows.ps1 first.
  pause
  exit /b 1
)

call ".venv\Scripts\activate.bat"
python main.py
