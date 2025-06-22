"""
Setup script for Live Transcription with Whisper
Handles dependency installation and common issues
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install all required dependencies"""
    print("🚀 Setting up Live Transcription with Whisper")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Upgrade pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    
    # Install core dependencies
    dependencies = [
        "numpy>=1.21.0",
        "torch>=1.9.0", 
        "torchaudio>=0.9.0"
    ]
    
    for dep in dependencies:
        if not run_command(f"{sys.executable} -m pip install {dep} --user", f"Installing {dep}"):
            return False
    
    # Install faster-whisper
    if not run_command(f"{sys.executable} -m pip install faster-whisper --user", "Installing faster-whisper"):
        return False
    
    # Install PyAudio (with platform-specific handling)
    if os.name == 'nt':  # Windows
        print("🔄 Installing PyAudio on Windows...")
        # Try pipwin first
        if not run_command(f"{sys.executable} -m pip install pipwin --user", "Installing pipwin"):
            print("⚠️  pipwin installation failed, trying direct PyAudio installation...")
        
        if not run_command(f"{sys.executable} -m pip install pyaudio --user", "Installing PyAudio"):
            print("❌ PyAudio installation failed. Please install manually:")
            print("   pip install pipwin")
            print("   pipwin install pyaudio")
            return False
    else:  # Unix-like systems
        if not run_command(f"{sys.executable} -m pip install pyaudio --user", "Installing PyAudio"):
            print("❌ PyAudio installation failed. Please install system dependencies first:")
            print("   Ubuntu/Debian: sudo apt-get install portaudio19-dev python3-pyaudio")
            print("   macOS: brew install portaudio")
            return False
    
    print("\n🎉 All dependencies installed successfully!")
    return True

def test_installation():
    """Test if the installation works"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        import faster_whisper
        import pyaudio
        import numpy
        print("✅ All modules imported successfully")
        
        # Test Whisper model loading
        print("🔄 Testing Whisper model loading...")
        model = faster_whisper.WhisperModel("tiny")
        print("✅ Whisper model loaded successfully")
        
        print("\n🎉 Installation test passed! You can now run:")
        print("   python live_transcription.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def main():
    """Main setup function"""
    if install_dependencies():
        test_installation()
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 