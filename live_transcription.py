import pyaudio
import wave
import threading
import time
import numpy as np
from faster_whisper import WhisperModel
import queue
import sys

class LiveTranscription:
    def __init__(self, model_size="base", chunk_duration=3.0, sample_rate=16000):
        """
        Initialize live transcription with faster-whisper
        
        Args:
            model_size (str): Whisper model size ("tiny", "base", "small", "medium", "large")
            chunk_duration (float): Duration of audio chunks in seconds
            sample_rate (int): Audio sample rate
        """
        self.model_size = model_size
        self.chunk_duration = chunk_duration
        self.sample_rate = sample_rate
        self.chunk_size = int(sample_rate * chunk_duration)
        
        # Initialize Whisper model
        print(f"Loading Whisper model: {model_size}")
        self.model = WhisperModel(model_size)
        print("Model loaded successfully!")
        
        # Audio settings
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        
        # Threading and queues
        self.audio_queue = queue.Queue()
        self.transcription_queue = queue.Queue()
        self.is_recording = False
        
        # Initialize PyAudio
        self.pyaudio_instance = pyaudio.PyAudio()
        
    def audio_callback(self, in_data, frame_count, time_info, status):
        """Callback function for audio stream"""
        if self.is_recording:
            self.audio_queue.put(in_data)
        return (in_data, pyaudio.paContinue)
    
    def record_audio(self):
        """Record audio from microphone"""
        try:
            stream = self.pyaudio_instance.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self.audio_callback
            )
            
            print("🎤 Recording started. Press Ctrl+C to stop.")
            stream.start_stream()
            
            while self.is_recording:
                time.sleep(0.1)
                
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            print(f"Error in audio recording: {e}")
    
    def process_audio_chunks(self):
        """Process audio chunks and transcribe them"""
        audio_buffer = b""
        
        while self.is_recording:
            try:
                # Get audio data from queue
                audio_data = self.audio_queue.get(timeout=1)
                audio_buffer += audio_data
                
                # Process when we have enough data
                if len(audio_buffer) >= self.chunk_size * 2:  # 2 bytes per sample
                    # Convert to numpy array
                    audio_array = np.frombuffer(audio_buffer, dtype=np.int16)
                    audio_array = audio_array.astype(np.float32) / 32768.0
                    
                    # Transcribe the chunk
                    segments, _ = self.model.transcribe(
                        audio_array, 
                        language="en",  # Change language as needed
                        beam_size=5,
                        best_of=5,
                        temperature=0.0
                    )
                    
                    # Get transcription text
                    transcription_text = " ".join([segment.text for segment in segments])
                    
                    if transcription_text.strip():
                        print(f"🎯 {transcription_text}")
                        self.transcription_queue.put(transcription_text)
                    
                    # Clear buffer
                    audio_buffer = b""
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in audio processing: {e}")
    
    def start_transcription(self):
        """Start live transcription"""
        self.is_recording = True
        
        # Start recording thread
        record_thread = threading.Thread(target=self.record_audio)
        record_thread.daemon = True
        record_thread.start()
        
        # Start processing thread
        process_thread = threading.Thread(target=self.process_audio_chunks)
        process_thread.daemon = True
        process_thread.start()
        
        try:
            while self.is_recording:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping transcription...")
            self.stop_transcription()
    
    def stop_transcription(self):
        """Stop live transcription"""
        self.is_recording = False
        self.pyaudio_instance.terminate()
        print("✅ Transcription stopped.")
    
    def get_transcription_history(self):
        """Get all transcriptions from the queue"""
        transcriptions = []
        while not self.transcription_queue.empty():
            transcriptions.append(self.transcription_queue.get())
        return transcriptions

def main():
    """Main function to run live transcription"""
    print("🎤 Live Transcription with Whisper")
    print("=" * 40)
    
    # Configuration
    model_size = "base"  # Options: "tiny", "base", "small", "medium", "large"
    chunk_duration = 2.0  # Duration of audio chunks in seconds
    
    # Create transcription instance
    transcriber = LiveTranscription(
        model_size=model_size,
        chunk_duration=chunk_duration
    )
    
    try:
        # Start transcription
        transcriber.start_transcription()
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    finally:
        transcriber.stop_transcription()
        
        # Show transcription history
        print("\n📝 Transcription History:")
        print("-" * 20)
        history = transcriber.get_transcription_history()
        for i, text in enumerate(history, 1):
            print(f"{i}. {text}")

if __name__ == "__main__":
    main() 