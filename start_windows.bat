@echo off
setlocal
cd /d "%~dp0"
if not exist backend\.venv\Scripts\activate.bat (echo Run setup_windows.bat first.& pause & exit /b 1)
start "ClaimWise API" cmd /k "cd /d ""%~dp0backend"" && call .venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
start "ClaimWise Web" cmd /k "cd /d ""%~dp0frontend"" && npm run dev"
echo Backend: http://localhost:8000/docs
echo Frontend: http://localhost:5173
echo Ensure PostgreSQL is running and backend\.env is configured.
