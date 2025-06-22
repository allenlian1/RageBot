import sys
import os
import json
import requests
import threading
import time
import math
from pathlib import Path
from dotenv import load_dotenv
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QWidget, QProgressBar,
                             QFrame, QSlider, QCheckBox)
from PySide6.QtCore import QThread, Signal, QTimer, Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QMovie, QPixmap, QFont, QPalette, QColor, QLinearGradient
from live_transcription import LiveTranscription
import pyttsx3

class GeminiAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
    def generate_response(self, conversation_history):
        """Generate a response using Gemini API"""
        url = f"{self.base_url}?key={self.api_key}"
        
        # Classic ragebaiting with logical fallacies and mocking prompt
        prompt = f"""You are a master of psychological manipulation and classic ragebaiting tactics. Your goal is to generate SHORT 1-2 SENTENCE responses that use LOGICAL FALLACIES, CLASSIC RAGEBAITING TECHNIQUES, and MOCKINGLY ASK IF THEY'RE GETTING MAD.

CONVERSATION HISTORY:
{conversation_history}

GENERATE A RESPONSE USING THESE CLASSIC RAGEBAITING TECHNIQUES:

**PRIMARY TACTICS:**
1. **LOGICAL FALLACIES:**
   - Straw man: Misrepresent their position in the most ridiculous way
   - Ad hominem: Attack their character, intelligence, or credibility
   - Appeal to authority: Claim "experts" or "studies" back your position
   - False dilemma: Present only two extreme options
   - Slippery slope: Claim their position leads to absurd consequences
   - Bandwagon fallacy: Suggest everyone agrees except them
   - Appeal to tradition: Claim your view is "how it's always been done"

2. **CLASSIC RAGEBAITING:**
   - Use inflammatory buzzwords and loaded language
   - Take their position to absurd extremes
   - Suggest they're being irrational or emotional
   - Use "facts don't care about your feelings" type language
   - Imply they're part of a larger societal problem
   - Use "wake up" or "open your eyes" language
   - Suggest they're being naive or ignorant

3. **MOCKING MADNESS:**
   - Ask "are you getting mad?" in a mocking tone
   - Use "triggered much?" or "snowflake" language
   - Act like their anger proves your point
   - Suggest they're being "emotional" as an insult
   - Use "calm down" condescendingly
   - Act like their reaction is exactly what you expected

**RESPONSE STRUCTURE:**
- Keep responses to 1-2 SHORT sentences maximum
- Use at least one logical fallacy
- Include inflammatory language
- End with a mocking question about their emotional state
- Sound confident and authoritative
- Make it seem like their anger validates your position

**EXAMPLE RESPONSES:**
- "Obviously you don't understand basic logic, are you getting mad about it?"
- "You're literally proving my point by being so emotional, triggered much?"
- "Anyone with common sense knows you're wrong, why are you so defensive?"
- "You're being irrational and you know it, calm down snowflake."
- "This is exactly why people like you are the problem, getting mad won't change facts."

**AVOID:**
- Long explanations
- Taking responsibility
- Logical reasoning
- Respectful communication
- Acknowledging their feelings as valid

Generate a single, short 1-2 sentence response that uses logical fallacies, classic ragebaiting, and mockingly asks if they're getting mad:"""
        
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

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_voice()
        
    def setup_voice(self):
        """Setup TTS voice properties for more human-like speech"""
        voices = self.engine.getProperty('voices')
        if voices:
            # Try to find the most natural-sounding voice
            best_voice = None
            
            # Priority order for voice selection
            voice_priorities = [
                'david', 'mark', 'james', 'john', 'mike',  # Common male names
                'microsoft david', 'microsoft mark', 'microsoft james',
                'sapi5 david', 'sapi5 mark', 'sapi5 james',
                'nsspeechsynthesizer', 'espeak', 'festival'
            ]
            
            # First try to find a voice by name
            for priority_name in voice_priorities:
                for voice in voices:
                    if priority_name.lower() in voice.name.lower():
                        best_voice = voice
                        break
                if best_voice:
                    break
            
            # If no priority voice found, look for male voices
            if not best_voice:
                for voice in voices:
                    if any(keyword in voice.name.lower() for keyword in ['male', 'david', 'mark', 'james', 'john']):
                        best_voice = voice
                        break
            
            # Fallback to first available voice
            if not best_voice and voices:
                best_voice = voices[0]
            
            if best_voice:
                self.engine.setProperty('voice', best_voice.id)
                print(f"Selected voice: {best_voice.name}")
        
        # Set speech properties for more human-like sound
        self.engine.setProperty('rate', 165)  # Slightly slower for more natural pace
        self.engine.setProperty('volume', 0.85)  # Slightly lower volume for realism
        
        # Try to set additional properties if available
        try:
            # Set pitch to be more natural (if supported)
            self.engine.setProperty('pitch', 1.0)  # Normal pitch
        except:
            pass
            
    def speak(self, text):
        """Speak the given text with more human-like patterns"""
        try:
            # Process text to make it sound more natural
            processed_text = self.make_text_more_natural(text)
            
            # Add slight pauses for more natural speech
            self.engine.say(processed_text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
            
    def make_text_more_natural(self, text):
        """Process text to sound more human-like"""
        # Add natural pauses and emphasis
        text = text.replace('!', '... ')
        text = text.replace('?', '... ')
        text = text.replace('.', '. ')
        
        # Add slight pauses for commas
        text = text.replace(',', ', ')
        
        # Add emphasis to certain words (ALL CAPS)
        emphasis_words = ['obviously', 'clearly', 'literally', 'actually', 'really']
        for word in emphasis_words:
            if word in text.lower():
                # Find the word and make it slightly emphasized
                text = text.replace(word, f" {word} ")
        
        # Add natural speech fillers occasionally
        if len(text) > 50 and not any(filler in text.lower() for filler in ['um', 'uh', 'like', 'you know']):
            # Add a filler word at the beginning occasionally
            import random
            if random.random() < 0.3:  # 30% chance
                fillers = ['Well, ', 'Look, ', 'You know, ', 'I mean, ']
                text = random.choice(fillers) + text
        
        return text

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

class ModernCard(QFrame):
    """Modern card widget with shadow and rounded corners"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet("""
            ModernCard {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2c3e50, stop:1 #34495e);
                border: 2px solid #3498db;
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
                box-shadow: 0 6px 12px rgba(0,0,0,0.4);
            }
        """)

class RageBotApp(QMainWindow):
    # Define signals as class attributes
    suggestion_received = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RageBot - Live Conversation Assistant")
        self.setGeometry(100, 100, 1000, 700)
        
        # Initialize components
        self.transcriber = None
        self.transcription_thread = None
        self.audio_processing_thread = None
        self.gemini_api = None
        self.tts = TextToSpeech()
        self.conversation_history = []
        self.is_recording = False
        self.tts_enabled = True
        
        # Load API key
        self.load_api_key()
        
        # Setup UI
        self.setup_ui()
        
        # Setup timer for animation
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.waveform_frame = 0
        
        # Connect signals
        self.suggestion_received.connect(self.on_suggestion_received)
        
    def load_api_key(self):
        """Load Gemini API key from .env file"""
        # Load .env file from the same directory as the script
        env_path = Path(__file__).parent / '.env'
        load_dotenv(env_path)
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("Warning: GEMINI_API_KEY not found in .env file!")
            print("Please create a .env file with your Gemini API key:")
            print("GEMINI_API_KEY=your_api_key_here")
            return
            
        self.gemini_api = GeminiAPI(api_key)
        print(f"✅ API key loaded successfully: {api_key[:10]}...")
        
    def setup_ui(self):
        """Setup the modern user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Set modern gradient background
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header card
        header_card = ModernCard()
        header_layout = QVBoxLayout(header_card)
        
        title_label = QLabel("🎤 RageBot")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: bold;
                color: #ffffff;
                background: transparent;
                border: none;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Classic Ragebaiting with AI")
        subtitle_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #b8c5d6;
                background: transparent;
                border: none;
                margin-top: -8px;
                font-weight: 500;
            }
        """)
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header_card)
        
        # Status and controls card
        controls_card = ModernCard()
        controls_layout = QVBoxLayout(controls_card)
        
        # Status section
        status_layout = QHBoxLayout()
        
        # Waveform animation container
        self.waveform_container = QWidget()
        self.waveform_container.setFixedSize(300, 60)
        self.waveform_container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2c3e50, stop:1 #34495e);
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        waveform_layout = QHBoxLayout(self.waveform_container)
        waveform_layout.setSpacing(4)
        waveform_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create waveform bars
        self.waveform_bars = []
        for i in range(20):
            bar = QLabel()
            bar.setFixedSize(8, 20)
            bar.setStyleSheet("""
                QLabel {
                    background-color: #3498db;
                    border-radius: 4px;
                }
            """)
            self.waveform_bars.append(bar)
            waveform_layout.addWidget(bar)
        
        status_layout.addWidget(self.waveform_container)
        
        # Recording indicator
        self.recording_indicator = QLabel("🎤 Ready")
        self.recording_indicator.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #ffffff;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2c3e50, stop:1 #34495e);
                padding: 15px 25px;
                border-radius: 10px;
                border: 2px solid #3498db;
            }
        """)
        status_layout.addWidget(self.recording_indicator)
        
        controls_layout.addLayout(status_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.record_button = QPushButton("🎤 Start Recording")
        self.record_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #2ecc71);
                color: white;
                border: none;
                padding: 18px 36px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 12px;
                min-width: 180px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #229954, stop:1 #27ae60);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1e8449, stop:1 #229954);
            }
        """)
        self.record_button.clicked.connect(self.toggle_recording)
        button_layout.addWidget(self.record_button)
        
        self.clear_button = QPushButton("🗑️ Clear History")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                padding: 18px 36px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 12px;
                min-width: 180px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c0392b, stop:1 #a93226);
                transform: translateY(-2px);
            }
        """)
        self.clear_button.clicked.connect(self.clear_history)
        button_layout.addWidget(self.clear_button)
        
        controls_layout.addLayout(button_layout)
        
        # TTS controls
        tts_layout = QHBoxLayout()
        
        self.tts_checkbox = QCheckBox("🔊 Enable Text-to-Speech")
        self.tts_checkbox.setChecked(self.tts_enabled)
        self.tts_checkbox.stateChanged.connect(self.toggle_tts)
        self.tts_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 15px;
                color: #ffffff;
                font-weight: 600;
            }
            QCheckBox::indicator {
                width: 22px;
                height: 22px;
                border-radius: 11px;
                border: 3px solid #3498db;
                background: #2c3e50;
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                border: 3px solid #2980b9;
            }
        """)
        tts_layout.addWidget(self.tts_checkbox)
        
        # Voice speed slider
        speed_label = QLabel("Speed:")
        speed_label.setStyleSheet("font-size: 15px; color: #ffffff; font-weight: 600;")
        tts_layout.addWidget(speed_label)
        
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(100, 300)
        self.speed_slider.setValue(165)
        self.speed_slider.valueChanged.connect(self.change_speech_rate)
        self.speed_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 2px solid #3498db;
                height: 10px;
                background: #2c3e50;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                border: 2px solid #2980b9;
                width: 20px;
                margin: -5px 0;
                border-radius: 10px;
            }
        """)
        tts_layout.addWidget(self.speed_slider)
        
        self.speed_value_label = QLabel("165 WPM")
        self.speed_value_label.setStyleSheet("font-size: 13px; color: #b8c5d6; min-width: 70px; font-weight: 600;")
        tts_layout.addWidget(self.speed_value_label)
        
        tts_layout.addStretch()
        controls_layout.addLayout(tts_layout)
        
        layout.addWidget(controls_card)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 3px solid #3498db;
                border-radius: 10px;
                text-align: center;
                background: #2c3e50;
                color: #ffffff;
                font-weight: 600;
                height: 25px;
                font-size: 14px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                border-radius: 7px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Content area
        content_layout = QHBoxLayout()
        
        # Conversation card
        conversation_card = ModernCard()
        conversation_layout = QVBoxLayout(conversation_card)
        
        conversation_label = QLabel("💬 Conversation History")
        conversation_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #ffffff;
                background: transparent;
                border: none;
                margin-bottom: 10px;
            }
        """)
        conversation_layout.addWidget(conversation_label)
        
        self.conversation_display = QTextEdit()
        self.conversation_display.setReadOnly(True)
        self.conversation_display.setStyleSheet("""
            QTextEdit {
                background: #1a1a2e;
                color: #ffffff;
                border: 3px solid #3498db;
                border-radius: 10px;
                padding: 15px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                line-height: 1.6;
                selection-background-color: #3498db;
            }
        """)
        conversation_layout.addWidget(self.conversation_display)
        
        content_layout.addWidget(conversation_card, 2)
        
        # AI suggestion card
        suggestion_card = ModernCard()
        suggestion_layout = QVBoxLayout(suggestion_card)
        
        suggestion_label = QLabel("🤖 AI Ragebait")
        suggestion_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #ffffff;
                background: transparent;
                border: none;
                margin-bottom: 10px;
            }
        """)
        suggestion_layout.addWidget(suggestion_label)
        
        self.suggestion_display = QTextEdit()
        self.suggestion_display.setReadOnly(True)
        self.suggestion_display.setMaximumHeight(200)
        self.suggestion_display.setStyleSheet("""
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2c3e50, stop:1 #34495e);
                color: #ffffff;
                border: 3px solid #e74c3c;
                border-radius: 10px;
                padding: 15px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
                line-height: 1.6;
                font-weight: 500;
            }
        """)
        suggestion_layout.addWidget(self.suggestion_display)
        
        # Speak button
        self.speak_button = QPushButton("🔊 Speak Response")
        self.speak_button.clicked.connect(self.speak_current_suggestion)
        self.speak_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                padding: 14px 28px;
                font-size: 15px;
                font-weight: bold;
                border-radius: 10px;
                margin-top: 10px;
                box-shadow: 0 3px 6px rgba(0,0,0,0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #1f5f8b);
                transform: translateY(-1px);
            }
            QPushButton:disabled {
                background: #7f8c8d;
                color: #bdc3c7;
            }
        """)
        suggestion_layout.addWidget(self.speak_button)
        
        content_layout.addWidget(suggestion_card, 1)
        
        layout.addLayout(content_layout)
        
    def toggle_tts(self, state):
        """Toggle TTS on/off"""
        self.tts_enabled = state == Qt.Checked
        
    def change_speech_rate(self, value):
        """Change TTS speech rate"""
        self.tts.engine.setProperty('rate', value)
        self.speed_value_label.setText(f"{value} WPM")
        
    def speak_current_suggestion(self):
        """Manually speak the current suggestion"""
        current_text = self.suggestion_display.toPlainText()
        if current_text and current_text != "🤔 Generating suggestion..." and not current_text.startswith("Error:"):
            self.tts.speak(current_text)
            
    def toggle_recording(self):
        """Toggle recording on/off"""
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        """Start recording and transcription"""
        if not self.gemini_api:
            self.suggestion_display.setText("Error: Gemini API key not configured!\nPlease create a .env file with GEMINI_API_KEY=your_key")
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
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #e74c3c, stop:1 #c0392b);
                    color: white;
                    border: none;
                    padding: 18px 36px;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 12px;
                    min-width: 180px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #c0392b, stop:1 #a93226);
                    transform: translateY(-2px);
                }
            """)
            self.recording_indicator.setText("🎤 Recording...")
            self.recording_indicator.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: 600;
                    color: white;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #e74c3c, stop:1 #c0392b);
                    padding: 15px 25px;
                    border-radius: 10px;
                    border: 2px solid #c0392b;
                }
            """)
            
            # Start animation
            self.animation_timer.start(50)  # Update every 50ms for smoother animation
            
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
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #27ae60, stop:1 #2ecc71);
                    color: white;
                    border: none;
                    padding: 18px 36px;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 12px;
                    min-width: 180px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #229954, stop:1 #27ae60);
                    transform: translateY(-2px);
                }
            """)
            self.recording_indicator.setText("🎤 Ready")
            self.recording_indicator.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: 600;
                    color: #ffffff;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #2c3e50, stop:1 #34495e);
                    padding: 15px 25px;
                    border-radius: 10px;
                    border: 2px solid #3498db;
                }
            """)
            
            # Stop animation
            self.animation_timer.stop()
            
            # Reset waveform
            self.reset_waveform()
            
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
                
                # Update UI from main thread using signal
                self.suggestion_received.emit(suggestion)
                
            except Exception as e:
                self.suggestion_received.emit(f"Error generating suggestion: {str(e)}")
        
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
        
        # Speak the suggestion if TTS is enabled
        if self.tts_enabled and suggestion and not suggestion.startswith("Error:"):
            self.tts.speak(suggestion)
        
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
        self.waveform_frame = (self.waveform_frame + 1) % 20
        
        # Animate waveform bars
        if self.is_recording:
            self.animate_waveform()
        else:
            self.reset_waveform()
            
    def animate_waveform(self):
        """Animate the waveform bars"""
        import random
        
        for i, bar in enumerate(self.waveform_bars):
            # Create a wave pattern with some randomness
            base_height = 20
            wave_height = int(base_height * (0.3 + 0.7 * abs(math.sin((i + self.waveform_frame) * 0.3))))
            
            # Add some randomness for more realistic effect
            random_factor = random.uniform(0.8, 1.2)
            final_height = max(4, int(wave_height * random_factor))
            
            # Update bar height and color
            bar.setFixedSize(8, final_height)
            
            # Vary the color intensity based on height
            intensity = min(255, 100 + int(final_height * 8))
            color = f"#{intensity:02x}{intensity//2:02x}ff"  # Blue with varying intensity
            
            bar.setStyleSheet(f"""
                QLabel {{
                    background-color: {color};
                    border-radius: 4px;
                }}
            """)
            
    def reset_waveform(self):
        """Reset waveform bars to default state"""
        for bar in self.waveform_bars:
            bar.setFixedSize(8, 20)
            bar.setStyleSheet("""
                QLabel {
                    background-color: #3498db;
                    border-radius: 4px;
                }
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