# 🎤 RageBot - Live Conversation Assistant

RageBot is a PySide6-based desktop application that provides real-time speech transcription and AI-powered conversation suggestions using Google's Gemini API. Perfect for generating engaging responses during live conversations!

## ✨ Features

- **🎤 Live Speech Transcription**: Real-time audio recording and transcription using Whisper
- **🤖 AI-Powered Suggestions**: Generate conversation responses using Google's Gemini API
- **🎨 Modern GUI**: Clean, intuitive PySide6 interface with recording animations
- **📝 Conversation History**: Keep track of your conversation flow
- **⚡ Real-time Processing**: Non-blocking UI with threaded audio processing

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API key"
4. Create a new API key
5. Copy the API key

### 3. Setup Environment

#### Option A: Use the Setup Script (Recommended)
```bash
python setup_environment.py
```

#### Option B: Manual Setup

Create a `.env` file in the project directory:
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

Or copy the template:
```bash
cp env_template.txt .env
# Then edit .env and add your actual API key
```

### 4. Run the Application

```bash
python ragebot_pyside.py
```

## 🎯 How to Use

1. **Start Recording**: Click the "🎤 Start Recording" button
2. **Speak**: The app will transcribe your speech in real-time
3. **Get Suggestions**: AI will generate conversation suggestions based on the context
4. **Continue Conversation**: Use the suggestions to keep the conversation engaging
5. **Stop Recording**: Click "⏹️ Stop Recording" when done

## 📋 Requirements

- Python 3.8+
- PySide6 (Qt6 bindings for Python)
- faster-whisper
- pyaudio
- requests
- numpy
- torch
- python-dotenv

## 🔧 Configuration

### API Key Setup
The application uses a `.env` file for configuration:

```bash
# .env file
GEMINI_API_KEY=your_actual_api_key_here
CHUNK_DURATION=2.0
MODEL_SIZE=base
SAMPLE_RATE=16000
```

### Audio Settings
- **Sample Rate**: 16kHz (default)
- **Chunk Duration**: 2 seconds (configurable)
- **Model Size**: "base" (options: tiny, base, small, medium, large)

### AI Settings
- **Model**: Gemini 2.0 Flash
- **Context Window**: Last 5 conversation exchanges
- **Response Style**: Engaging and provocative

## 🛠️ Troubleshooting

### Common Issues

1. **"No module named 'pyaudio'"**
   ```bash
   # Windows
   pip install pipwin
   pipwin install pyaudio
   
   # Linux
   sudo apt-get install portaudio19-dev
   pip install pyaudio
   
   # macOS
   brew install portaudio
   pip install pyaudio
   ```

2. **".env file not found"**
   - Run `python setup_environment.py` to create the .env file
   - Or manually create a .env file with your API key

3. **"GEMINI_API_KEY not found in .env file"**
   - Edit the .env file and add your API key
   - Make sure the format is: `GEMINI_API_KEY=your_key_here`

4. **Audio recording issues**
   - Check microphone permissions
   - Ensure microphone is not being used by other applications
   - Try different audio input devices

5. **GUI issues on Windows**
   - PySide6 is used instead of PyQt6 for better Windows compatibility
   - If you still have issues, try running: `pip install --user PySide6`

### Verification

Run the verification script to check your setup:
```bash
python test_app.py
```

## 📁 Project Structure

```
RageBot/
├── ragebot_pyside.py       # Main PySide6 application
├── live_transcription.py   # Speech transcription engine
├── setup_environment.py    # Environment setup script
├── test_app.py            # Component testing script
├── start_ragebot.py       # Smart launcher
├── env_template.txt       # .env file template
├── requirements.txt       # Python dependencies
├── run_ragebot.bat       # Windows launcher
├── run_ragebot.sh        # Unix launcher
└── README.md             # This file
```

## 🔒 Privacy & Security

- **Local Processing**: Audio transcription happens locally using Whisper
- **API Key Security**: API key is stored in local `.env` file (never commit to version control)
- **Data Privacy**: Conversation data is not stored permanently
- **Network Usage**: Only API calls to Gemini are sent over the network

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Google AI Studio](https://aistudio.google.com/) for Gemini API
- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [PySide6](https://doc.qt.io/qtforpython/) for the GUI framework

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Verify your setup with `python test_app.py`
3. Check the console output for error messages
4. Open an issue on GitHub with detailed error information

---

**Happy RageBotting! 🎤🤖** 