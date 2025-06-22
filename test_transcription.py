"""
Simple test script to verify faster-whisper installation and basic functionality
"""
import numpy as np
from faster_whisper import WhisperModel
import time

def test_whisper_installation():
    """Test if faster-whisper is working correctly"""
    print("🧪 Testing faster-whisper installation...")
    
    try:
        # Load the model
        print("Loading Whisper model (tiny for speed)...")
        model = WhisperModel("tiny")
        print("✅ Model loaded successfully!")
        
        # Create a simple test audio (silence)
        print("Creating test audio...")
        sample_rate = 16000
        duration = 2.0  # 2 seconds
        samples = int(sample_rate * duration)
        
        # Generate some test audio (sine wave)
        t = np.linspace(0, duration, samples, False)
        test_audio = np.sin(2 * np.pi * 440 * t) * 0.1  # 440 Hz sine wave, low volume
        test_audio = test_audio.astype(np.float32)
        
        print("Transcribing test audio...")
        start_time = time.time()
        
        segments, info = model.transcribe(test_audio, language="en")
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"✅ Transcription completed in {processing_time:.2f} seconds")
        print(f"Language detected: {info.language} (confidence: {info.language_probability:.2f})")
        
        # Print segments
        for segment in segments:
            print(f"Segment: {segment.text}")
        
        print("\n🎉 All tests passed! Your installation is working correctly.")
        print("You can now run 'python live_transcription.py' for live microphone transcription.")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("Please check your installation and try again.")

if __name__ == "__main__":
    test_whisper_installation() 