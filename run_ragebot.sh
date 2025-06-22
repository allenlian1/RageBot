#!/bin/bash

echo "🎤 Starting RageBot..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Check if requirements are installed
echo "🔍 Checking dependencies..."
python3 -c "import PySide6, faster_whisper, pyaudio, requests, dotenv" &> /dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Some dependencies are missing"
    echo "Installing requirements..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install requirements"
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found"
    echo "Running setup..."
    python3 setup_environment.py
    if [ $? -ne 0 ]; then
        echo "❌ Setup failed"
        exit 1
    fi
fi

echo "✅ Starting RageBot application..."
echo
python3 ragebot_pyside.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ RageBot encountered an error"
    read -p "Press Enter to continue..."
fi 