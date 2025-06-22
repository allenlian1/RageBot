# Live Transcription with Whisper

A real-time speech-to-text transcription tool using OpenAI's Whisper model via `faster-whisper` and microphone input.

## Features

- 🎤 Real-time microphone input
- 🚀 Fast transcription using `faster-whisper`
- 🌍 Multilingual support (configurable)
- 📝 Transcription history
- ⚙️ Configurable model sizes and chunk durations
- 🎯 High accuracy with beam search

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install PyAudio (if needed)

On Windows:
```bash
pip install pyaudio
```

On macOS:
```bash
brew install portaudio
pip install pyaudio
```

On Ubuntu/Debian:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

## Usage

### Basic Usage

Run the live transcription script:

```bash
python live_transcription.py
```

The script will:
1. Load the Whisper model (base model by default)
2. Start recording from your microphone
3. Transcribe speech in real-time
4. Display transcriptions as they're processed
5. Show transcription history when stopped

### Configuration

You can modify the configuration in the `main()` function:

```python
# Model size options: "tiny", "base", "small", "medium", "large"
model_size = "base"

# Duration of audio chunks in seconds
chunk_duration = 3.0
```

### Model Sizes

- **tiny**: Fastest, least accurate (~39MB)
- **base**: Good balance of speed and accuracy (~74MB)
- **small**: Better accuracy, slower (~244MB)
- **medium**: High accuracy, slower (~769MB)
- **large**: Best accuracy, slowest (~1550MB)

## How It Works

1. **Audio Recording**: Uses PyAudio to capture audio from the microphone in real-time
2. **Chunking**: Audio is processed in configurable time chunks (default: 3 seconds)
3. **Transcription**: Each chunk is sent to the Whisper model for transcription
4. **Output**: Transcriptions are displayed in real-time and stored in history

## Controls

- **Start**: Run the script to begin transcription
- **Stop**: Press `Ctrl+C` to stop transcription
- **History**: View all transcriptions when the session ends

## Troubleshooting

### PyAudio Installation Issues

If you encounter PyAudio installation problems:

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
export LDFLAGS="-L/opt/homebrew/lib"
export CFLAGS="-I/opt/homebrew/include"
pip install pyaudio
```

### Microphone Not Working

1. Check if your microphone is properly connected
2. Ensure microphone permissions are granted
3. Test with a simple audio recording script first

### Model Download Issues

The first run will download the Whisper model. Ensure you have:
- Stable internet connection
- Sufficient disk space (up to 1.5GB for large model)
- Proper permissions to write to the cache directory

## Performance Tips

- Use "tiny" or "base" models for faster real-time performance
- Reduce `chunk_duration` for more responsive transcription
- Use "large" model for maximum accuracy (slower)
- Ensure good microphone quality for better results

## Example Output

```
🎤 Live Transcription with Whisper
========================================
Loading Whisper model: base
Model loaded successfully!
🎤 Recording started. Press Ctrl+C to stop.
🎯 Hello, this is a test of the live transcription system.
🎯 The transcription is working in real time.
🎯 You can speak continuously and see the results.

🛑 Stopping transcription...
✅ Transcription stopped.

📝 Transcription History:
--------------------
1. Hello, this is a test of the live transcription system.
2. The transcription is working in real time.
3. You can speak continuously and see the results.
```

## License

This project uses OpenAI's Whisper model. Please refer to OpenAI's licensing terms for commercial use. 