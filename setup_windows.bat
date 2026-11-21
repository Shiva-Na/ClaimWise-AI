@echo off
setlocal
cd /d "%~dp0"
echo === ClaimWise AI setup ===
where py >nul 2>nul || (echo Python launcher not found. Install Python 3.11 or 3.12 and retry.& pause & exit /b 1)
where npm >nul 2>nul || (echo npm not found. Install Node.js 20 LTS or later and retry.& pause & exit /b 1)
if not exist backend\.venv (py -3.11 -m venv backend\.venv 2>nul || py -3.12 -m venv backend\.venv)
call backend\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
if errorlevel 1 (echo Backend dependencies failed. Check your internet connection and Python version.& pause & exit /b 1)
cd frontend
npm install
if errorlevel 1 (echo Frontend dependencies failed. Check your internet connection and Node.js version.& pause & exit /b 1)
cd ..
if not exist backend\.env copy backend\.env.example backend\.env
if not exist frontend\.env copy frontend\.env.example frontend\.env
echo.
echo Setup complete. Edit backend\.env with your PostgreSQL password and optional OpenAI key.
pause
