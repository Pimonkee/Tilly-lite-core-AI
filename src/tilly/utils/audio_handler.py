"""
Audio Handler Module for Tilly AI
Provides speech recognition and text-to-speech capabilities
"""

import logging
from typing import Optional, Callable
from pathlib import Path
import threading
import queue

logger = logging.getLogger(__name__)

# Try to import audio libraries with graceful fallback
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    logger.warning("SpeechRecognition not available. Install with: pip install SpeechRecognition")

try:
    from gtts import gTTS
    import tempfile
    import os
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    logger.warning("gTTS not available. Install with: pip install gTTS")

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    logger.warning("pyttsx3 not available. Install with: pip install pyttsx3")


class AudioHandler:
    """Handles speech recognition and text-to-speech"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer() if SPEECH_RECOGNITION_AVAILABLE else None
        self.tts_engine = None
        self.is_listening = False
        self.listen_thread = None
        self.audio_queue = queue.Queue()
        
        # Initialize pyttsx3 if available (offline TTS)
        if PYTTSX3_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self._configure_tts_engine()
            except Exception as e:
                logger.warning(f"Failed to initialize pyttsx3: {e}")
                self.tts_engine = None
    
    def _configure_tts_engine(self):
        """Configure the TTS engine settings"""
        if self.tts_engine:
            try:
                # Set properties
                self.tts_engine.setProperty('rate', 150)  # Speed of speech
                self.tts_engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
                
                # Try to set a female voice if available
                voices = self.tts_engine.getProperty('voices')
                for voice in voices:
                    if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            except Exception as e:
                logger.warning(f"Error configuring TTS engine: {e}")
    
    def listen_once(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for a single speech input and convert to text
        
        Args:
            timeout: Maximum time to wait for speech to start (seconds)
            phrase_time_limit: Maximum time for a phrase (seconds)
            
        Returns:
            Recognized text, or None if recognition failed
        """
        if not SPEECH_RECOGNITION_AVAILABLE or not self.recognizer:
            logger.error("Speech recognition not available")
            return None
        
        try:
            with sr.Microphone() as source:
                logger.info("Listening for speech...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
                
                logger.info("Processing speech...")
                # Use Google Speech Recognition
                text = self.recognizer.recognize_google(audio)
                logger.info(f"Recognized: {text}")
                return text
                
        except sr.WaitTimeoutError:
            logger.warning("Listening timed out")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error during speech recognition: {e}")
            return None
    
    def start_continuous_listening(self, callback: Callable[[str], None]):
        """
        Start listening continuously in a background thread
        
        Args:
            callback: Function to call with recognized text
        """
        if self.is_listening:
            logger.warning("Already listening")
            return
        
        if not SPEECH_RECOGNITION_AVAILABLE or not self.recognizer:
            logger.error("Speech recognition not available")
            return
        
        self.is_listening = True
        self.listen_thread = threading.Thread(
            target=self._listen_loop,
            args=(callback,),
            daemon=True
        )
        self.listen_thread.start()
        logger.info("Started continuous listening")
    
    def stop_continuous_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        logger.info("Stopped continuous listening")
    
    def _listen_loop(self, callback: Callable[[str], None]):
        """Internal loop for continuous listening"""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
            while self.is_listening:
                try:
                    logger.debug("Listening for speech...")
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                    
                    # Process in background to not block listening
                    threading.Thread(
                        target=self._process_audio,
                        args=(audio, callback),
                        daemon=True
                    ).start()
                    
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    logger.error(f"Error in listen loop: {e}")
                    continue
    
    def _process_audio(self, audio, callback: Callable[[str], None]):
        """Process audio in background thread"""
        try:
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            callback(text)
        except sr.UnknownValueError:
            logger.debug("Could not understand audio")
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
    
    def speak(self, text: str, use_online: bool = False) -> bool:
        """
        Convert text to speech and play it
        
        Args:
            text: Text to speak
            use_online: Use online TTS (gTTS) instead of offline (pyttsx3)
            
        Returns:
            True if speech was successful, False otherwise
        """
        if not text:
            return False
        
        try:
            if use_online and GTTS_AVAILABLE:
                return self._speak_gtts(text)
            elif self.tts_engine and PYTTSX3_AVAILABLE:
                return self._speak_pyttsx3(text)
            else:
                logger.error("No TTS engine available")
                return False
        except Exception as e:
            logger.error(f"Error during speech: {e}")
            return False
    
    def _speak_pyttsx3(self, text: str) -> bool:
        """Speak using pyttsx3 (offline)"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return True
        except Exception as e:
            logger.error(f"pyttsx3 error: {e}")
            return False
    
    def _speak_gtts(self, text: str) -> bool:
        """Speak using gTTS (online, requires internet)"""
        try:
            # Create speech
            tts = gTTS(text=text, lang='en', slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name
                tts.save(temp_file)
            
            # Play the audio (platform dependent)
            # This is a simplified version - in production, use a proper audio player
            import subprocess
            import platform
            
            system = platform.system()
            if system == 'Darwin':  # macOS
                subprocess.run(['afplay', temp_file])
            elif system == 'Linux':
                subprocess.run(['mpg123', temp_file])
            elif system == 'Windows':
                subprocess.run(['start', temp_file], shell=True)
            
            # Clean up
            try:
                os.unlink(temp_file)
            except:
                pass
            
            return True
        except Exception as e:
            logger.error(f"gTTS error: {e}")
            return False
    
    def save_speech_to_file(self, text: str, filepath: Path) -> bool:
        """
        Convert text to speech and save to file
        
        Args:
            text: Text to convert
            filepath: Path where to save the audio file
            
        Returns:
            True if saved successfully, False otherwise
        """
        if not GTTS_AVAILABLE:
            logger.error("gTTS not available for saving audio")
            return False
        
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(str(filepath))
            logger.info(f"Speech saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving speech: {e}")
            return False


# Global instance
_audio_instance = None


def get_audio_instance() -> AudioHandler:
    """Get or create the global audio handler instance"""
    global _audio_instance
    if _audio_instance is None:
        _audio_instance = AudioHandler()
    return _audio_instance
