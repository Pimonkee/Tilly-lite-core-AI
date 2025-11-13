"""
Tests for Computer Vision and Audio Handler modules
"""
import pytest
import sys
from pathlib import Path
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tilly.utils.computer_vision import ComputerVision, get_vision_instance
from tilly.utils.audio_handler import AudioHandler, get_audio_instance


class TestComputerVision:
    """Test computer vision functionality"""
    
    def test_vision_instance_creation(self):
        """Test creating a computer vision instance"""
        cv = ComputerVision()
        assert cv is not None
        assert not cv.is_active
        assert cv.camera is None
    
    def test_get_vision_instance(self):
        """Test getting the global vision instance"""
        cv1 = get_vision_instance()
        cv2 = get_vision_instance()
        assert cv1 is cv2  # Should be the same instance
    
    def test_frame_to_base64(self):
        """Test converting a frame to base64"""
        cv = ComputerVision()
        
        # Create a dummy frame (100x100 blue image)
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame[:, :] = [255, 0, 0]  # Blue in BGR
        
        # Convert to base64
        base64_str = cv.frame_to_base64(frame)
        assert base64_str is not None
        assert isinstance(base64_str, str)
        assert len(base64_str) > 0
    
    def test_base64_to_frame(self):
        """Test converting base64 back to frame"""
        cv = ComputerVision()
        
        # Create a dummy frame
        original_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        original_frame[:, :] = [0, 255, 0]  # Green in BGR
        
        # Convert to base64 and back
        base64_str = cv.frame_to_base64(original_frame)
        decoded_frame = cv.base64_to_frame(base64_str)
        
        assert decoded_frame is not None
        assert decoded_frame.shape == original_frame.shape
        # Allow some tolerance due to JPEG compression
        assert np.mean(np.abs(decoded_frame - original_frame)) < 10
    
    def test_detect_faces_no_faces(self):
        """Test face detection on image without faces"""
        cv = ComputerVision()
        
        # Create a blank frame
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        
        faces = cv.detect_faces(frame)
        assert isinstance(faces, list)
        assert len(faces) == 0
    
    def test_annotate_frame(self):
        """Test annotating frame with face rectangles"""
        cv = ComputerVision()
        
        # Create a dummy frame
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Mock some face detections
        faces = [(10, 10, 30, 30), (50, 50, 40, 40)]
        
        annotated = cv.annotate_frame(frame, faces)
        assert annotated is not None
        assert annotated.shape == frame.shape
        # Frame should have been modified (rectangles drawn)
        assert not np.array_equal(annotated, frame)


class TestAudioHandler:
    """Test audio handler functionality"""
    
    def test_audio_instance_creation(self):
        """Test creating an audio handler instance"""
        audio = AudioHandler()
        assert audio is not None
        assert not audio.is_listening
    
    def test_get_audio_instance(self):
        """Test getting the global audio instance"""
        audio1 = get_audio_instance()
        audio2 = get_audio_instance()
        assert audio1 is audio2  # Should be the same instance
    
    def test_configure_tts_engine(self):
        """Test TTS engine configuration"""
        audio = AudioHandler()
        # Just check that the method doesn't crash
        # Actual configuration depends on system availability
        if audio.tts_engine:
            audio._configure_tts_engine()
            assert True
        else:
            pytest.skip("TTS engine not available")
    
    def test_save_speech_to_file_without_gtts(self):
        """Test that save_speech_to_file handles missing gTTS gracefully"""
        audio = AudioHandler()
        from tilly.utils import audio_handler as ah
        
        # Temporarily disable gTTS
        original_gtts = ah.GTTS_AVAILABLE
        ah.GTTS_AVAILABLE = False
        
        result = audio.save_speech_to_file("test", Path("/tmp/test.mp3"))
        
        # Restore original value
        ah.GTTS_AVAILABLE = original_gtts
        
        assert result == False


class TestIntegration:
    """Integration tests for vision and audio"""
    
    def test_vision_and_audio_instances_independent(self):
        """Test that vision and audio instances are independent"""
        cv = get_vision_instance()
        audio = get_audio_instance()
        
        assert cv is not audio
        assert isinstance(cv, ComputerVision)
        assert isinstance(audio, AudioHandler)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
