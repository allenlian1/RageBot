@echo off
echo 🎤 Starting RageBot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
echo 🔍 Checking dependencies...
python -c "import PySide6, faster_whisper, pyaudio, requests, dotenv" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Some dependencies are missing
    echo Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install requirements
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found
    echo Running setup...
    python setup_environment.py
    if errorlevel 1 (
        echo ❌ Setup failed
        pause
        exit /b 1
    )
)

echo ✅ Starting RageBot application...
echo.
python ragebot_pyside.py

if errorlevel 1 (
    echo.
    echo ❌ RageBot encountered an error
    pause
) 