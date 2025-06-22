#!/usr/bin/env python3
"""
RageBot Launcher - Simple startup script with dependency checking
"""

import sys
import os
import subprocess
import importlib
from pathlib import Path
from dotenv import load_dotenv

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_modules = [
        'PySide6',
        'faster_whisper', 
        'pyaudio',
        'requests',
        'numpy',
        'torch',
        'dotenv'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n❌ Missing modules: {', '.join(missing_modules)}")
        print("Installing missing dependencies...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    
    print("✅ All dependencies are installed!")
    return True

def check_api_key():
    """Check if Gemini API key is configured in .env file"""
    env_file = Path('.env')
    if not env_file.exists():
        print("\n⚠️  .env file not found!")
        print("You need to set up your Gemini API key to use RageBot.")
        
        response = input("Would you like to run the setup now? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            try:
                subprocess.run([sys.executable, "setup_environment.py"])
                return True
            except Exception as e:
                print(f"❌ Setup failed: {e}")
                return False
        else:
            print("You can set up your API key later by running: python setup_environment.py")
            return False
    
    try:
        load_dotenv(env_file)
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("\n⚠️  GEMINI_API_KEY not found in .env file!")
            print("Please edit the .env file and add your API key.")
            return False
        
        print(f"✅ API key found: {api_key[:10]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def main():
    """Main launcher function"""
    print("🎤 RageBot Launcher")
    print("=" * 30)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Cannot start RageBot due to missing dependencies")
        input("Press Enter to exit...")
        return
    
    # Check API key
    if not check_api_key():
        print("\n⚠️  RageBot will start but AI features won't work without an API key")
        response = input("Continue anyway? (y/n): ").lower().strip()
        if response not in ['y', 'yes']:
            return
    
    # Start the application
    print("\n🚀 Starting RageBot...")
    try:
        subprocess.run([sys.executable, "ragebot_pyside.py"])
    except KeyboardInterrupt:
        print("\n👋 RageBot stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start RageBot: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 