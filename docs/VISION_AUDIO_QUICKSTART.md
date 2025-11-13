# Quick Start Guide: Computer Vision & Voice Features

## 🎥 Using Computer Vision

### Prerequisites
- Webcam connected to your computer
- Browser with camera permissions (Chrome, Firefox, Safari recommended)

### Steps

1. **Start Tilly:**
   ```bash
   python run.py
   ```

2. **Open Web UI:**
   Navigate to http://localhost:8000/

3. **Enable Camera:**
   - Click the 📹 **Camera** button in the toolbar
   - Allow camera access when prompted by your browser
   - You'll see a live video feed appear

4. **Chat with Vision:**
   Type messages in the chat. Tilly will be aware of what she sees through the camera!
   
   Example conversation:
   ```
   You: Can you see me?
   Tilly: Yes! I can see 1 face in the camera 😊
   
   You: What's in front of me?
   Tilly: [Vision Context: I can see 1 face(s) in the camera]
   ```

5. **Turn Off Camera:**
   Click the Camera button again to stop the video feed.

### Face Detection
The system automatically detects faces using Haar Cascades and draws green rectangles around them.

---

## 🎤 Using Voice Conversations

### Prerequisites
- Microphone connected to your computer
- Internet connection (for speech recognition)
- Speakers/headphones for audio output

### Steps

1. **Start Tilly:**
   ```bash
   python run.py
   ```

2. **Open Web UI:**
   Navigate to http://localhost:8000/

3. **Start Voice Conversation:**
   - Click the 🎤 **Voice** button
   - Allow microphone access when prompted
   - Wait for "Listening..." message
   - **Speak clearly** into your microphone

4. **Tilly Responds:**
   - Your speech is transcribed and displayed
   - Tilly processes your message
   - You'll hear Tilly's response through your speakers
   - Response also appears as text

### Tips for Best Results
- Speak clearly and at a normal pace
- Minimize background noise
- Wait for the "Listening..." indicator before speaking
- Each click starts a new conversation turn

---

## 🔌 Using the API Directly

### Computer Vision API

```python
import requests

# Start camera
response = requests.post('http://localhost:8000/vision/start')
print(response.json())  # {'status': 'success', 'message': 'Camera started'}

# Capture a frame
response = requests.get('http://localhost:8000/vision/capture')
data = response.json()
print(f"Faces detected: {data['faces_detected']}")

# Chat with vision context
response = requests.post('http://localhost:8000/vision/chat', json={
    'message': 'What do you see?'
})
print(response.json()['response'])

# Stop camera
requests.post('http://localhost:8000/vision/stop')
```

### Voice Conversation API

```python
import requests

# Full voice conversation
response = requests.post('http://localhost:8000/audio/conversation')
data = response.json()

if data['status'] == 'success':
    print(f"You said: {data['user_text']}")
    print(f"Tilly said: {data['response']}")
else:
    print("No speech detected")
```

### Text-to-Speech Only

```python
import requests

response = requests.post('http://localhost:8000/audio/speak', params={
    'text': 'Hello! I am Tilly, your AI companion.'
})
# Tilly will speak the text through your speakers
```

### Speech-to-Text Only

```python
import requests

response = requests.post('http://localhost:8000/audio/listen')
data = response.json()

if data['status'] == 'success':
    print(f"You said: {data['text']}")
else:
    print("No speech detected")
```

---

## 🛠️ Troubleshooting

### Camera Issues

**Problem:** Camera button doesn't activate
- **Solution:** Check that your webcam is connected and not being used by another application
- **Solution:** Grant camera permissions in your browser settings

**Problem:** No video feed appears
- **Solution:** Check browser console for errors (F12)
- **Solution:** Try a different browser (Chrome recommended)

### Voice Issues

**Problem:** "No speech detected"
- **Solution:** Check microphone is connected and working
- **Solution:** Speak louder or move closer to microphone
- **Solution:** Check browser microphone permissions

**Problem:** No audio output
- **Solution:** Check speakers/headphones are connected
- **Solution:** Increase system volume
- **Solution:** Check browser audio permissions

**Problem:** Text-to-speech not working
- **Solution:** Install required packages: `pip install pyttsx3 gTTS`
- **Solution:** Check internet connection (required for gTTS)

### General Issues

**Problem:** Module import errors
- **Solution:** Install all dependencies: `pip install -r requirements.txt`

**Problem:** API endpoints return 500 errors
- **Solution:** Check server logs for detailed error messages
- **Solution:** Ensure all required services are running

---

## 📝 Configuration

### Audio Settings

Edit `src/tilly/utils/audio_handler.py` to customize:

```python
# Speech recognition timeout (seconds)
timeout=5

# Maximum phrase duration (seconds)
phrase_time_limit=10

# TTS speech rate (words per minute)
rate=150

# TTS volume (0.0 to 1.0)
volume=0.9
```

### Camera Settings

Edit `src/tilly/utils/computer_vision.py` to customize:

```python
# Camera device index (0 = default camera, 1 = external camera)
camera_index=0

# Frame capture interval (milliseconds)
# In app.js, change: setInterval(() => this.captureFrame(), 100)
interval=100  # 10 FPS
```

---

## 🎯 Use Cases

### Mental Wellness Check-ins
Use voice conversations for daily emotional check-ins:
```
User: "How are you feeling today?" (spoken)
Tilly: "I'm doing well, thank you for asking! How are you feeling?" (spoken)
```

### Vision-Based Support
Enable camera for more empathetic interactions:
```
User: "I'm feeling anxious"
Tilly: [sees your facial expression] "I can see you're here with me. Let's take some deep breaths together..."
```

### Hands-Free Interaction
Use voice mode while doing other activities:
- Cooking and chatting
- Exercising while getting motivation
- Relaxing with eyes closed during meditation

---

## 🔐 Privacy & Security

- **Camera:** Video is processed locally and not stored
- **Audio:** Speech is processed through Google's API (requires internet)
- **Data:** No recordings are saved unless explicitly configured
- **Permissions:** Always requested before accessing camera/microphone

---

## 💡 Pro Tips

1. **Combine Features:** Use camera and voice together for the most natural experience
2. **Good Lighting:** Better lighting = better face detection
3. **Quiet Environment:** Less background noise = better speech recognition
4. **Browser Choice:** Chrome has the best WebRTC support for camera/audio
5. **Microphone Quality:** Better microphone = better recognition accuracy

---

## 📞 Need Help?

- Check the main [README.md](../README.md) for setup instructions
- Visit `/docs` when the server is running for API documentation
- Open an issue on GitHub if you encounter problems
- See server logs in `data/logs/tilly.log` for debugging

---

**Happy chatting with Tilly! 🤖💜**
