@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" "main.py"
) else (
    echo [INFO] Virtual environment not found. Running with system python...
    python "main.py"
)

pause
