#!/usr/bin/env python3
"""
Setup script for RageBot environment configuration
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Setup the environment for RageBot"""
    print("🎤 RageBot Environment Setup")
    print("=" * 40)
    
    # Check if .env file already exists
    env_file = Path('.env')
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    print("\n📋 To use RageBot, you need a Gemini API key.")
    print("Follow these steps:")
    print("\n1. Go to Google AI Studio: https://aistudio.google.com/")
    print("2. Sign in with your Google account")
    print("3. Click 'Get API key'")
    print("4. Create a new API key")
    print("5. Copy the API key")
    
    print("\n🔧 Creating .env file...")
    
    # Get API key from user
    api_key = input("\nEnter your Gemini API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return False
    
    # Create .env file
    try:
        with open(env_file, 'w') as f:
            f.write(f"# RageBot Configuration\n")
            f.write(f"# Your Gemini API key from Google AI Studio\n")
            f.write(f"GEMINI_API_KEY={api_key}\n")
            f.write(f"\n# Optional: Audio settings\n")
            f.write(f"# CHUNK_DURATION=2.0\n")
            f.write(f"# MODEL_SIZE=base\n")
            f.write(f"# SAMPLE_RATE=16000\n")
        
        print(f"✅ .env file created successfully!")
        print(f"📁 Location: {env_file.absolute()}")
        print("\n🔒 Security note: The .env file contains your API key.")
        print("   Make sure to keep it secure and never commit it to version control.")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False
    
    print("\n🎉 Setup complete! You can now run RageBot.")
    return True

def verify_setup():
    """Verify that the setup is correct"""
    print("\n🔍 Verifying setup...")
    
    # Check if required packages are installed
    required_packages = ['PySide6', 'faster_whisper', 'pyaudio', 'requests', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    # Check .env file
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found")
        print("Run: python setup_environment.py")
        return False
    
    # Check API key in .env file
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env file")
            return False
        print(f"✅ API key found: {api_key[:10]}...")
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False
    
    print("✅ All required packages are installed")
    print("✅ .env file is configured")
    print("\n🎉 Setup verification complete!")
    return True

def create_env_template():
    """Create a template .env file"""
    template_content = """# RageBot Configuration
# Copy this file to .env and add your actual API key

# Your Gemini API key from Google AI Studio
# Get it from: https://aistudio.google.com/
GEMINI_API_KEY=your_api_key_here

# Optional: Audio settings (these can be overridden in the app)
# CHUNK_DURATION=2.0
# MODEL_SIZE=base
# SAMPLE_RATE=16000
"""
    
    try:
        with open('env_template.txt', 'w') as f:
            f.write(template_content)
        print("✅ Template file created: env_template.txt")
        print("Copy this to .env and add your API key")
    except Exception as e:
        print(f"❌ Error creating template: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'verify':
            verify_setup()
        elif sys.argv[1] == 'template':
            create_env_template()
        else:
            print("Usage: python setup_environment.py [verify|template]")
    else:
        setup_environment() 