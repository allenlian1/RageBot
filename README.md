# 🎤 RageBot - Live Conversation Assistant

A modern PySide6 desktop application that provides real-time audio transcription and AI-powered conversation suggestions using advanced ragebaiting tactics and logical fallacies.

## Features

### 🎤 Live Audio Recording & Transcription
- Real-time audio capture from microphone
- Instant transcription using OpenAI Whisper
- Continuous conversation tracking

### 🤖 AI-Powered Ragebaiting
- Advanced psychological manipulation techniques
- Logical fallacies integration (straw man, ad hominem, appeal to authority, etc.)
- Emotional engagement optimization
- Controversial response generation

### 🔊 Text-to-Speech (TTS)
- Automatic speech synthesis for AI responses
- Adjustable speech rate (100-300 WPM)
- Male voice preference for authoritative tone
- Manual "Speak Response" button
- TTS enable/disable toggle

### 🎨 Modern UI Design
- Gradient backgrounds and modern styling
- Card-based layout with rounded corners
- Responsive design with proper spacing
- Professional color scheme
- Animated recording indicator
- Progress bars and status indicators

## Installation

### Prerequisites
- Python 3.8 or higher
- Microphone access
- Internet connection for API calls

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd RageBot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file:**
   ```bash
   cp env_template.txt .env
   ```

4. **Add your Gemini API key:**
   Edit `.env` and add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

### Quick Start
1. Run the application:
   ```bash
   python ragebot_pyside.py
   ```

2. Configure TTS settings (optional):
   - Toggle TTS on/off with the checkbox
   - Adjust speech rate using the slider
   - Use "Speak Response" button for manual playback

3. Start recording:
   - Click "🎤 Start Recording" to begin
   - Speak into your microphone
   - View real-time transcriptions
   - Receive AI-generated responses

4. Manage conversation:
   - View full conversation history
   - Clear history with "🗑️ Clear History"
   - Stop recording anytime

### TTS Controls
- **Enable/Disable**: Checkbox to turn TTS on/off
- **Speech Rate**: Slider to adjust words per minute (100-300 WPM)
- **Manual Playback**: "🔊 Speak Response" button to replay current suggestion

## Technical Details

### Architecture
- **PySide6**: Modern Qt-based UI framework
- **OpenAI Whisper**: Real-time speech-to-text
- **Google Gemini API**: AI response generation
- **pyttsx3**: Cross-platform text-to-speech
- **Threading**: Non-blocking audio processing

### Ragebaiting Techniques
The AI uses advanced psychological manipulation including:
- **Logical Fallacies**: Straw man, ad hominem, appeal to authority, false dilemma
- **Psychological Triggers**: Condescending language, tribal instincts, false urgency
- **Emotional Manipulation**: Inflammatory language, loaded terms, crisis creation

### Voice Settings
- **Default Rate**: 180 WPM (adjustable 100-300)
- **Volume**: 90% (fixed)
- **Voice Preference**: Male voice for authoritative tone
- **Cross-platform**: Works on Windows, macOS, and Linux

## File Structure
```
RageBot/
├── ragebot_pyside.py      # Main application
├── live_transcription.py  # Audio transcription module
├── requirements.txt       # Python dependencies
├── .env                  # API key configuration
├── env_template.txt      # Environment template
├── run_ragebot.bat       # Windows launcher
├── run_ragebot.sh        # Linux/macOS launcher
└── README.md            # This file
```

## Troubleshooting

### Common Issues

**TTS not working:**
- Ensure pyttsx3 is installed: `pip install pyttsx3`
- Check system audio settings
- Try different speech rates

**Audio recording issues:**
- Verify microphone permissions
- Check PyAudio installation
- Ensure microphone is not in use by other applications

**API errors:**
- Verify Gemini API key in `.env` file
- Check internet connection
- Ensure API key has proper permissions

### Platform-Specific Notes

**Windows:**
- TTS uses Windows SAPI voices
- PyAudio may require Visual C++ redistributables

**macOS:**
- TTS uses macOS system voices
- May need to grant microphone permissions

**Linux:**
- TTS uses espeak or festival
- May need to install additional audio packages

## Development

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Test thoroughly
5. Submit pull request

### Customization
- Modify `ragebaiting_prompt` in `GeminiAPI.generate_response()` for different AI behavior
- Adjust TTS settings in `TextToSpeech.setup_voice()`
- Customize UI styling in `setup_ui()` method

## License

This project is for educational and research purposes. Use responsibly and ethically.

## Disclaimer

This application is designed for educational purposes to demonstrate AI conversation techniques. The ragebaiting features are intended for research and understanding of online communication patterns. Use responsibly and consider the ethical implications of AI-generated content.