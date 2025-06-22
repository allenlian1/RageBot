#!/usr/bin/env python3
"""
Test script for RageBot components
"""

import sys
import os
import importlib
from pathlib import Path
from dotenv import load_dotenv

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    required_modules = [
        'PySide6',
        'faster_whisper', 
        'pyaudio',
        'requests',
        'numpy',
        'torch',
        'dotenv'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All imports successful!")
    return True

def test_api_key():
    """Test if Gemini API key is configured in .env file"""
    print("\n🔑 Testing API key configuration...")
    
    # Load .env file
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found")
        print("Run: python setup_environment.py")
        return False
    
    try:
        load_dotenv(env_file)
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env file")
            print("Run: python setup_environment.py")
            return False
        
        print(f"✅ API key found: {api_key[:10]}...")
        return True
        
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def test_transcription():
    """Test transcription module"""
    print("\n🎤 Testing transcription module...")
    
    try:
        from live_transcription import LiveTranscription
        print("✅ LiveTranscription class imported successfully")
        
        # Test initialization (without starting audio)
        transcriber = LiveTranscription(model_size="tiny")
        print("✅ Transcriber initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Transcription test failed: {e}")
        return False

def test_gui():
    """Test PySide6 GUI components"""
    print("\n🖥️ Testing GUI components...")
    
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import QTimer
        
        # Create minimal app for testing
        app = QApplication([])
        print("✅ QApplication created successfully")
        
        # Test timer
        timer = QTimer()
        print("✅ QTimer created successfully")
        
        app.quit()
        return True
        
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

def test_gemini_api():
    """Test Gemini API connection"""
    print("\n🤖 Testing Gemini API...")
    
    try:
        from ragebot_pyside import GeminiAPI
        
        # Load .env file
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("❌ No API key available for testing")
            return False
        
        api = GeminiAPI(api_key)
        print("✅ GeminiAPI class created successfully")
        
        # Test with a simple prompt
        test_prompt = "Say hello"
        response = api.generate_response(test_prompt)
        
        if response and not response.startswith("Error"):
            print(f"✅ API test successful: {response[:50]}...")
            return True
        else:
            print(f"❌ API test failed: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 RageBot Component Tests")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_api_key,
        test_transcription,
        test_gui,
        test_gemini_api
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! RageBot is ready to use.")
        print("Run: python ragebot_pyside.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 