# FALCON-AI PowerShell Launcher
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectDir
Write-Host "===================================================" -ForegroundColor Green
Write-Host "Starting FALCON-AI Server on http://localhost:8000" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Green
& "$ProjectDir\.venv\Scripts\python.exe" -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
