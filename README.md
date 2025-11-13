# 🤖 Tilly AI - Your Empathetic AI Companion

<div align="center">

![Tilly AI](static/images/logo.png)

*An empathetic AI companion focused on mental wellness and genuine human connection*

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

Tilly is an advanced AI companion designed with empathy at its core. Unlike traditional chatbots, Tilly focuses on:

- **Mental Wellness Support**: Providing therapeutic conversations and emotional support
- **Crisis Detection**: Identifying users who may need immediate help
- **Emotional Intelligence**: Understanding and responding to emotional states
- **Multi-Model Architecture**: Seamlessly switching between different AI models for optimal responses

---

## ✨ Features

### Core Capabilities

- 🧠 **Advanced Intent Recognition**: Detects user needs (wellness, crisis, casual chat)
- 💭 **Mood Analysis**: Understands emotional states and adjusts responses accordingly
- 🔄 **Multi-Model Support**: Works with Gemini, DeepSeek, Ollama, and other LLM providers
- 🚨 **Crisis Detection**: Identifies users in distress and provides appropriate resources
- 💬 **Context-Aware Conversations**: Maintains conversation history and context
- 🖼️ **OCR Integration**: Extract and process text from images
- 📊 **Health Monitoring**: Built-in health checks for all components
- 👁️ **Computer Vision**: Real-time webcam integration with face detection
- 🎤 **Live Voice Conversations**: Speech-to-text and text-to-speech for natural interactions

### Technical Features

- ⚡ **FastAPI Backend**: High-performance async API
- 🎨 **Modern Web UI**: ChatGPT-style interface with avatar support
- 🔒 **Security First**: Built-in security best practices
- 📈 **Scalable Architecture**: Modular design for easy extension
- 🐳 **Container Ready**: Easy deployment with Docker
- 📝 **Comprehensive Logging**: Detailed logs for debugging and monitoring
- 📹 **Video Streaming**: Real-time camera feed in web interface
- 🗣️ **Audio Processing**: Speech recognition and synthesis

---

## 🏗️ Architecture

Tilly uses a modular pipeline architecture:

```
User Input → Intent Router → Mood Analyzer → LLM Provider → Response
                ↓               ↓               ↓
            Context ←─────────────────────────────
```

### Key Components

1. **Intent Router**: Analyzes user input to determine intent (wellness, crisis, chat)
2. **Mood Analyzer**: Detects emotional state and vulnerability level
3. **LLM Provider Manager**: Routes requests to appropriate AI models
4. **Context Manager**: Maintains conversation state and history
5. **API Layer**: FastAPI-based REST API for external integrations

---

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Pimonkee/Tilly-lite-core-AI.git
cd Tilly-lite-core-AI
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

Create a `.env` file in the root directory:

```bash
# LLM Provider Configuration
TILLY_PRIMARY_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Fallback Provider
TILLY_FALLBACK_PROVIDER=ollama

# Application Settings
TILLY_ENV=development
TILLY_LOG_LEVEL=INFO
TILLY_DATA_ROOT=./data

# Model Parameters
TILLY_TEMPERATURE=0.7
TILLY_MAX_TOKENS=1024
```

---

## 🚀 Quick Start

### Running Tilly

#### Option 1: Using the Run Script (Recommended)

```bash
python run.py
```

#### Option 2: Direct FastAPI

```bash
uvicorn src.tilly.api.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Option 3: With Custom Configuration

```bash
python run.py --host 127.0.0.1 --port 8080 --reload
```

### Accessing the Application

- **Web UI**: http://localhost:8000/
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Example API Requests

#### Chat with Tilly

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I am feeling anxious today",
    "session_id": "user123"
  }'
```

#### Health Check

```bash
curl http://localhost:8000/health
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TILLY_PRIMARY_PROVIDER` | Primary LLM provider (gemini/deepseek/ollama) | `gemini` |
| `GEMINI_API_KEY` | Google Gemini API key | - |
| `DEEPSEEK_API_KEY` | DeepSeek API key | - |
| `TILLY_FALLBACK_PROVIDER` | Fallback provider if primary fails | - |
| `TILLY_ENV` | Environment (development/production) | `development` |
| `TILLY_LOG_LEVEL` | Logging level | `INFO` |
| `TILLY_DATA_ROOT` | Data directory path | `./data` |
| `TILLY_TEMPERATURE` | Model temperature (0.0-1.0) | `0.7` |
| `TILLY_MAX_TOKENS` | Maximum tokens per response | `1024` |

### LLM Provider Setup

#### Google Gemini

1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set `GEMINI_API_KEY` in `.env`
3. Set `TILLY_PRIMARY_PROVIDER=gemini`

#### DeepSeek

1. Get API key from [DeepSeek Platform](https://platform.deepseek.com/)
2. Set `DEEPSEEK_API_KEY` in `.env`
3. Set `TILLY_PRIMARY_PROVIDER=deepseek`

#### Ollama (Local)

1. Install [Ollama](https://ollama.ai/)
2. Pull a model: `ollama pull llama2`
3. Set `TILLY_PRIMARY_PROVIDER=ollama`

---

## 📚 API Documentation

### Endpoints

#### `POST /chat`

Chat with Tilly

**Request:**
```json
{
  "message": "Hello, how are you?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "Hello! I'm here to listen and support you...",
  "session_id": "generated-or-provided-id",
  "intent": "chat",
  "mood": "neutral",
  "model_used": "gemini-pro"
}
```

#### `GET /health`

Check system health

**Response:**
```json
{
  "status": "healthy",
  "components": {
    "pipeline": "healthy",
    "router": "healthy",
    "mood_detector": "healthy",
    "brain": {
      "gemini": true
    }
  }
}
```

#### `POST /ocr/upload/`

Upload image for OCR processing

**Request:** Multipart form with file

**Response:**
```json
{
  "filename": "image.png",
  "extracted_text": "Text from image...",
  "summary": "Brief summary of content"
}
```

#### `POST /vision/start`

Start the computer vision camera

**Response:**
```json
{
  "status": "success",
  "message": "Camera started"
}
```

#### `POST /vision/stop`

Stop the computer vision camera

**Response:**
```json
{
  "status": "success",
  "message": "Camera stopped"
}
```

#### `GET /vision/capture`

Capture a single frame from the camera with face detection

**Response:**
```json
{
  "status": "success",
  "image": "base64_encoded_image_data",
  "faces_detected": 2,
  "faces": [[x, y, w, h], ...]
}
```

#### `POST /vision/chat`

Chat with Tilly using computer vision context

**Request:**
```json
{
  "message": "What do you see?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "I can see 2 faces in the camera...",
  "session_id": "session-id",
  "intent": "chat",
  "mood": "neutral",
  "model_used": "gemini-pro"
}
```

#### `POST /audio/listen`

Listen for speech and convert to text

**Response:**
```json
{
  "status": "success",
  "text": "Hello Tilly"
}
```

#### `POST /audio/speak`

Convert text to speech and play it

**Parameters:** `text` (string)

**Response:**
```json
{
  "status": "success",
  "message": "Speech completed"
}
```

#### `POST /audio/conversation`

Live conversation: Listen, process with Tilly, and respond with speech

**Response:**
```json
{
  "status": "success",
  "user_text": "Hello Tilly",
  "response": "Hello! How are you?",
  "session_id": "session-id",
  "intent": "chat",
  "mood": "positive"
}
```

For complete API documentation, visit `/docs` when running the application.

---

## 🎥 Using Computer Vision and Voice Features

### Computer Vision

Tilly now supports real-time computer vision through your webcam:

1. **Start the Application**: Run `python run.py`
2. **Open the Web UI**: Navigate to `http://localhost:8000/`
3. **Click the Camera Button**: In the web interface, click the 📹 Camera button
4. **Grant Permissions**: Allow camera access when prompted by your browser
5. **View the Feed**: You'll see a live video feed with face detection
6. **Chat with Vision**: Messages sent while camera is active include vision context

**Features:**
- Real-time face detection using Haar Cascades
- Vision-enhanced conversations (Tilly knows what she sees)
- Easy on/off toggle
- Works entirely in the browser

### Live Voice Conversations

Have natural voice conversations with Tilly:

1. **Click the Voice Button**: Click the 🎤 Voice button in the web interface
2. **Grant Microphone Permissions**: Allow microphone access when prompted
3. **Speak Your Message**: Tilly will listen for 5-10 seconds
4. **Get Audio Response**: Tilly will respond both as text and speech

**Requirements:**
- Microphone access
- Internet connection for Google Speech Recognition
- Audio output (speakers/headphones)

**Offline Option:**
The system uses `pyttsx3` for offline text-to-speech. No internet required for responses!

### API Usage Examples

#### Vision Chat with cURL

```bash
# Start the camera
curl -X POST http://localhost:8000/vision/start

# Capture a frame
curl http://localhost:8000/vision/capture

# Chat with vision context
curl -X POST http://localhost:8000/vision/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What do you see?"}'

# Stop the camera
curl -X POST http://localhost:8000/vision/stop
```

#### Voice Conversation with Python

```python
import requests

# Start a voice conversation
response = requests.post('http://localhost:8000/audio/conversation')
data = response.json()

print(f"You said: {data['user_text']}")
print(f"Tilly responded: {data['response']}")
```

---

## 📁 Project Structure

```
Tilly-lite-core-AI/
├── src/
│   └── tilly/
│       ├── __init__.py
│       ├── core/              # Core AI components
│       │   ├── __init__.py
│       │   ├── tilly_conversation_context.py
│       │   ├── tilly_intelligence_pipeline.py
│       │   ├── tilly_intent_router.py
│       │   ├── tilly_mood_analyzer.py
│       │   └── tilly_l_l_m_provider_manager.py
│       ├── api/               # FastAPI application
│       │   ├── __init__.py
│       │   └── main.py
│       ├── config/            # Configuration management
│       │   ├── __init__.py
│       │   ├── configuration_manager.py
│       │   ├── manager.py
│       │   └── path_management.py
│       └── utils/             # Utility modules
│           ├── __init__.py
│           ├── ocr.py
│           ├── ollama_client.py
│           └── data_directory_management.py
├── static/                    # Static web assets
│   ├── css/
│   ├── js/
│   └── images/
├── templates/                 # HTML templates
├── docs/                      # Documentation
├── tests/                     # Test suite
├── data/                      # Runtime data (gitignored)
│   ├── logs/
│   ├── screenshots/
│   ├── memory/
│   └── sessions/
├── run.py                     # Main entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .env.example              # Example environment config
└── .gitignore                # Git ignore rules
```

---

## 🛠️ Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest

# Format code
black src/
isort src/

# Lint
flake8 src/
mypy src/
```

### Running in Development Mode

```bash
python run.py --reload
```

This enables auto-reload when code changes are detected.

### Adding New Features

1. Create your feature in the appropriate module under `src/tilly/`
2. Add tests in `tests/`
3. Update documentation
4. Submit a pull request

---

## 🎨 UI/UX Features

Tilly includes a modern, ChatGPT-style web interface:

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Chat**: Instant message delivery
- **Avatar Integration**: AI girlfriend avatar with animations
- **Typing Indicators**: Shows when Tilly is thinking
- **Message History**: Persistent conversation history
- **Dark/Light Themes**: User preference support
- **Accessibility**: WCAG 2.1 compliant

### Customizing the Avatar

The avatar can be customized by replacing the image in `static/images/avatar.png` or configuring in the UI settings.

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Write/update tests**
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Code Standards

- Follow PEP 8 style guide
- Write docstrings for all functions/classes
- Add type hints where applicable
- Include tests for new features
- Update documentation

---

## 🔒 Security

Tilly takes security seriously:

- No user data is stored without explicit consent
- API keys are stored securely in environment variables
- All communications use HTTPS in production
- Regular security audits and updates

### Reporting Security Issues

Please report security vulnerabilities to [security@tilly-ai.example](mailto:security@tilly-ai.example)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastAPI** - For the amazing web framework
- **Google Gemini** - For powerful LLM capabilities
- **DeepSeek** - For open-source AI models
- **Ollama** - For local AI model deployment
- **Open Source Community** - For continuous inspiration and support

---

## 📞 Support

- **Documentation**: [Full docs here](docs/)
- **Issues**: [GitHub Issues](https://github.com/Pimonkee/Tilly-lite-core-AI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Pimonkee/Tilly-lite-core-AI/discussions)
- **Email**: support@tilly-ai.example

---

## 🗺️ Roadmap

- [ ] Voice input/output integration
- [ ] Mobile applications (iOS/Android)
- [ ] Multi-language support
- [ ] Advanced emotion recognition
- [ ] Integration with mental health resources
- [ ] Plugin system for extensibility
- [ ] Kubernetes deployment templates

---

<div align="center">

**Made with ❤️ by the Tilly AI Team**

*Empowering better mental health through AI*

</div>
