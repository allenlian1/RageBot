import sys
import os
import json
import requests
import threading
import time
from dotenv import load_dotenv
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QWidget, QProgressBar)
from PySide6.QtCore import QThread, Signal, QTimer, Qt
from PySide6.QtGui import QMovie, QPixmap
from live_transcription import LiveTranscription

class GeminiAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
    def generate_response(self, conversation_history):
        """Generate a response using Gemini API"""
        url = f"{self.base_url}?key={self.api_key}"
        
        # Create a prompt for ragebaiting
        prompt = f"""You are an AI assistant that helps generate responses to continue conversations. 
        Based on the following conversation, suggest the next thing to say that would be engaging, 
        provocative, or interesting to keep the conversation going. Be creative and natural.

        Conversation history:
        {conversation_history}

        Generate a single, natural response that would be the next thing to say:"""
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                return "I couldn't generate a response at the moment."
                
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return f"Error: {str(e)}"

class TranscriptionThread(QThread):
    transcription_received = Signal(str)
    error_occurred = Signal(str)
    
    def __init__(self, transcriber):
        super().__init__()
        self.transcriber = transcriber
        self.is_running = False
        
    def run(self):
        self.is_running = True
        try:
            # Start transcription
            self.transcriber.start_transcription()
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.is_running = False
            
    def stop(self):
        self.is_running = False
        self.transcriber.stop_transcription()

class AudioProcessingThread(QThread):
    transcription_ready = Signal(str)
    
    def __init__(self, transcriber):
        super().__init__()
        self.transcriber = transcriber
        self.is_running = False
        
    def run(self):
        self.is_running = True
        while self.is_running:
            try:
                # Check for new transcriptions
                if not self.transcriber.transcription_queue.empty():
                    transcription = self.transcriber.transcription_queue.get()
                    if transcription.strip():
                        self.transcription_ready.emit(transcription)
                time.sleep(0.1)
            except Exception as e:
                print(f"Error in audio processing thread: {e}")
                break
                
    def stop(self):
        self.is_running = False

class RageBotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RageBot - Live Conversation Assistant")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize components
        self.transcriber = None
        self.transcription_thread = None
        self.audio_processing_thread = None
        self.gemini_api = None
        self.conversation_history = []
        self.is_recording = False
        
        # Load API key
        self.load_api_key()
        
        # Setup UI
        self.setup_ui()
        
        # Setup timer for animation
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_frame = 0
        
    def load_api_key(self):
        """Load Gemini API key from .env file"""
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'your_api_key_here':
            print("Warning: GEMINI_API_KEY not found or not configured!")
            print("Please:")
            print("1. Copy env_template.txt to .env")
            print("2. Edit .env and add your Gemini API key")
            print("3. Get your API key from: https://aistudio.google.com/")
            return
            
        self.gemini_api = GeminiAPI(api_key)
        print("Gemini API key loaded successfully!")
        
    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("🎤 RageBot - Live Conversation Assistant")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Recording status and animation
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("Ready to record")
        self.status_label.setStyleSheet("font-size: 16px; padding: 10px;")
        status_layout.addWidget(self.status_label)
        
        # Animation label (will show recording animation)
        self.animation_label = QLabel()
        self.animation_label.setFixedSize(50, 50)
        self.animation_label.setStyleSheet("border: 2px solid #ccc; border-radius: 25px;")
        status_layout.addWidget(self.animation_label)
        
        layout.addLayout(status_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.record_button = QPushButton("🎤 Start Recording")
        self.record_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.record_button.clicked.connect(self.toggle_recording)
        button_layout.addWidget(self.record_button)
        
        self.clear_button = QPushButton("🗑️ Clear History")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.clear_button.clicked.connect(self.clear_history)
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(button_layout)
        
        # Progress bar for processing
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Conversation display
        conversation_label = QLabel("Conversation History:")
        conversation_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(conversation_label)
        
        self.conversation_display = QTextEdit()
        self.conversation_display.setReadOnly(True)
        self.conversation_display.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
            }
        """)
        layout.addWidget(self.conversation_display)
        
        # AI suggestion display
        suggestion_label = QLabel("🤖 AI Suggestion:")
        suggestion_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(suggestion_label)
        
        self.suggestion_display = QTextEdit()
        self.suggestion_display.setReadOnly(True)
        self.suggestion_display.setMaximumHeight(100)
        self.suggestion_display.setStyleSheet("""
            QTextEdit {
                background-color: #e3f2fd;
                border: 1px solid #2196F3;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Arial', sans-serif;
            }
        """)
        layout.addWidget(self.suggestion_display)
        
    def toggle_recording(self):
        """Toggle recording on/off"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        """Start recording and transcription"""
        if not self.gemini_api:
            self.suggestion_display.setText("Error: Gemini API key not configured!")
            return
            
        try:
            # Initialize transcriber
            self.transcriber = LiveTranscription(model_size="base", chunk_duration=2.0)
            
            # Start transcription thread
            self.transcription_thread = TranscriptionThread(self.transcriber)
            self.transcription_thread.transcription_received.connect(self.on_transcription_received)
            self.transcription_thread.error_occurred.connect(self.on_error)
            self.transcription_thread.start()
            
            # Start audio processing thread
            self.audio_processing_thread = AudioProcessingThread(self.transcriber)
            self.audio_processing_thread.transcription_ready.connect(self.on_transcription_received)
            self.audio_processing_thread.start()
            
            # Update UI
            self.is_recording = True
            self.record_button.setText("⏹️ Stop Recording")
            self.record_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    font-size: 16px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)
            self.status_label.setText("🎤 Recording...")
            
            # Start animation
            self.animation_timer.start(100)  # Update every 100ms
            
        except Exception as e:
            self.suggestion_display.setText(f"Error starting recording: {str(e)}")
            
    def stop_recording(self):
        """Stop recording and transcription"""
        try:
            # Stop threads
            if self.transcription_thread:
                self.transcription_thread.stop()
                self.transcription_thread.wait()
                
            if self.audio_processing_thread:
                self.audio_processing_thread.stop()
                self.audio_processing_thread.wait()
                
            if self.transcriber:
                self.transcriber.stop_transcription()
                
            # Update UI
            self.is_recording = False
            self.record_button.setText("🎤 Start Recording")
            self.record_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 15px 30px;
                    font-size: 16px;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            self.status_label.setText("Ready to record")
            
            # Stop animation
            self.animation_timer.stop()
            self.animation_label.setStyleSheet("border: 2px solid #ccc; border-radius: 25px; background-color: transparent;")
            
        except Exception as e:
            self.suggestion_display.setText(f"Error stopping recording: {str(e)}")
            
    def on_transcription_received(self, transcription):
        """Handle new transcription"""
        if transcription.strip():
            # Add to conversation history
            self.conversation_history.append(f"User: {transcription}")
            
            # Update conversation display
            self.update_conversation_display()
            
            # Generate AI suggestion
            self.generate_ai_suggestion()
            
    def update_conversation_display(self):
        """Update the conversation display"""
        display_text = "\n".join(self.conversation_history)
        self.conversation_display.setText(display_text)
        
        # Auto-scroll to bottom
        scrollbar = self.conversation_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def generate_ai_suggestion(self):
        """Generate AI suggestion using Gemini"""
        if not self.gemini_api or not self.conversation_history:
            return
            
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.suggestion_display.setText("🤔 Generating suggestion...")
        
        # Run in separate thread to avoid blocking UI
        def generate_suggestion():
            try:
                conversation_text = "\n".join(self.conversation_history[-5:])  # Last 5 exchanges
                suggestion = self.gemini_api.generate_response(conversation_text)
                
                # Update UI from main thread
                self.suggestion_received.emit(suggestion)
                
            except Exception as e:
                self.suggestion_received.emit(f"Error generating suggestion: {str(e)}")
                
        # Create signal for suggestion received
        self.suggestion_received = Signal(str)
        self.suggestion_received.connect(self.on_suggestion_received)
        
        # Start suggestion thread
        suggestion_thread = threading.Thread(target=generate_suggestion)
        suggestion_thread.daemon = True
        suggestion_thread.start()
        
    def on_suggestion_received(self, suggestion):
        """Handle AI suggestion received"""
        self.progress_bar.setVisible(False)
        self.suggestion_display.setText(suggestion)
        
        # Add suggestion to conversation history
        self.conversation_history.append(f"AI: {suggestion}")
        self.update_conversation_display()
        
    def on_error(self, error_message):
        """Handle errors"""
        self.suggestion_display.setText(f"Error: {error_message}")
        self.stop_recording()
        
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        self.conversation_display.clear()
        self.suggestion_display.clear()
        
    def update_animation(self):
        """Update recording animation"""
        self.animation_frame = (self.animation_frame + 1) % 8
        
        # Create pulsing animation
        if self.animation_frame < 4:
            color = f"#{255 - self.animation_frame * 50:02x}0000"  # Red pulsing
        else:
            color = f"#{255 - (self.animation_frame - 4) * 50:02x}0000"
            
        self.animation_label.setStyleSheet(f"""
            border: 2px solid {color};
            border-radius: 25px;
            background-color: {color};
        """)
        
    def closeEvent(self, event):
        """Handle application close"""
        if self.is_recording:
            self.stop_recording()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the main window
    window = RageBotApp()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 