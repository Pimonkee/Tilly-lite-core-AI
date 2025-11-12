# Tilly AI - Quick Start Guide

## What is Tilly?

Tilly is an empathetic AI companion designed to provide mental wellness support through genuine human connection. Built with FastAPI and modern web technologies, Tilly features:

- 🧠 **Advanced AI**: Multi-model LLM support (Gemini, DeepSeek, Ollama)
- 💜 **Emotional Intelligence**: Intent detection, mood analysis, and crisis recognition
- 🎨 **Beautiful UI**: ChatGPT-style interface with friendly avatar
- 🔒 **Privacy-Focused**: Local data storage, secure by design
- 📱 **Responsive**: Works on desktop, tablet, and mobile

## 🚀 Quick Start (3 Minutes)

### 1. Clone and Setup

```bash
git clone https://github.com/Pimonkee/Tilly-lite-core-AI.git
cd Tilly-lite-core-AI
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env and add your API key:
# GEMINI_API_KEY=your_key_here
```

### 3. Run

```bash
python run.py
```

Visit http://localhost:8000 and start chatting! 🎉

## 📖 Documentation

- **[README.md](README.md)** - Complete documentation
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[docs/AVATAR_INTEGRATION.md](docs/AVATAR_INTEGRATION.md)** - Avatar customization guide

## 🐳 Docker Quick Start

```bash
docker-compose up
```

Visit http://localhost:8000

## 🧪 Testing

```bash
pytest tests/
```

## 🛠️ Project Structure

```
Tilly-lite-core-AI/
├── src/tilly/          # Core application code
│   ├── api/            # FastAPI endpoints
│   ├── core/           # AI intelligence pipeline
│   ├── config/         # Configuration management
│   └── utils/          # Utilities (OCR, etc.)
├── static/             # Web UI assets
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript
│   └── images/         # Avatar and images
├── templates/          # HTML templates
├── docs/               # Documentation
├── tests/              # Test suite
├── run.py              # Main entry point
└── requirements.txt    # Dependencies
```

## 🎯 Key Features

### Mental Wellness Focus
- Crisis detection with resource links
- Therapeutic conversation support
- Mood tracking and analysis
- Empathetic response generation

### Technical Excellence
- Async/await architecture
- Multi-model LLM support with fallback
- Modular pipeline design
- Comprehensive error handling

### Modern UI/UX
- ChatGPT-inspired interface
- Friendly AI companion avatar
- Real-time typing indicators
- Responsive design
- Suggestion cards for quick interactions

## 🔑 API Endpoints

- `GET /` - Web UI
- `POST /chat` - Chat with Tilly
- `GET /health` - System health check
- `GET /docs` - Interactive API documentation

## 💡 Tips

- **First Time Setup**: Get a free Gemini API key at https://makersuite.google.com/app/apikey
- **Local Model**: Use Ollama for offline operation
- **Development**: Use `python run.py --reload` for auto-reload
- **Logs**: Check `data/logs/tilly.log` for debugging

## 🤝 Community

- **Issues**: Report bugs on GitHub
- **Discussions**: Share ideas and ask questions
- **PRs**: Contributions welcome!

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

Made with ❤️ for better mental health through AI

**Need help?** Open an issue or check the full README.md
