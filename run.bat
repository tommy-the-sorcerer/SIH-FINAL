@echo off
title FALCON-AI Server
cd /d "%~dp0"
echo ===================================================
echo Starting FALCON-AI Server on http://localhost:8000
echo ===================================================
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment .venv not found.
    pause
    exit /b 1
)
call .venv\Scripts\activate.bat
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
