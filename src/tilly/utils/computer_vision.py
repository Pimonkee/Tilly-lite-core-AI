"""
Computer Vision Module for Tilly AI
Provides webcam capture and image analysis capabilities
"""

import cv2
import base64
import numpy as np
from typing import Optional, Tuple
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ComputerVision:
    """Handles webcam capture and basic image processing"""
    
    def __init__(self):
        self.camera = None
        self.is_active = False
        
    def start_camera(self, camera_index: int = 0) -> bool:
        """
        Initialize and start the camera
        
        Args:
            camera_index: Camera device index (default: 0 for primary camera)
            
        Returns:
            True if camera started successfully, False otherwise
        """
        try:
            self.camera = cv2.VideoCapture(camera_index)
            if self.camera.isOpened():
                self.is_active = True
                logger.info(f"Camera {camera_index} started successfully")
                return True
            else:
                logger.error(f"Failed to open camera {camera_index}")
                return False
        except Exception as e:
            logger.error(f"Error starting camera: {e}")
            return False
    
    def stop_camera(self):
        """Stop and release the camera"""
        if self.camera:
            self.camera.release()
            self.is_active = False
            logger.info("Camera stopped")
    
    def capture_frame(self) -> Optional[np.ndarray]:
        """
        Capture a single frame from the camera
        
        Returns:
            Captured frame as numpy array, or None if capture failed
        """
        if not self.is_active or not self.camera:
            logger.warning("Camera not active")
            return None
        
        try:
            ret, frame = self.camera.read()
            if ret:
                return frame
            else:
                logger.warning("Failed to read frame from camera")
                return None
        except Exception as e:
            logger.error(f"Error capturing frame: {e}")
            return None
    
    def frame_to_base64(self, frame: np.ndarray, format: str = 'jpg') -> Optional[str]:
        """
        Convert a frame to base64 encoded string
        
        Args:
            frame: Input frame as numpy array
            format: Image format ('jpg' or 'png')
            
        Returns:
            Base64 encoded string, or None if conversion failed
        """
        try:
            # Encode frame to the specified format
            if format.lower() == 'jpg' or format.lower() == 'jpeg':
                _, buffer = cv2.imencode('.jpg', frame)
            else:
                _, buffer = cv2.imencode('.png', frame)
            
            # Convert to base64
            base64_str = base64.b64encode(buffer).decode('utf-8')
            return base64_str
        except Exception as e:
            logger.error(f"Error converting frame to base64: {e}")
            return None
    
    def base64_to_frame(self, base64_str: str) -> Optional[np.ndarray]:
        """
        Convert base64 encoded string back to frame
        
        Args:
            base64_str: Base64 encoded image string
            
        Returns:
            Frame as numpy array, or None if conversion failed
        """
        try:
            # Decode base64 to bytes
            img_bytes = base64.b64decode(base64_str)
            # Convert to numpy array
            nparr = np.frombuffer(img_bytes, np.uint8)
            # Decode image
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return frame
        except Exception as e:
            logger.error(f"Error converting base64 to frame: {e}")
            return None
    
    def save_frame(self, frame: np.ndarray, filepath: Path) -> bool:
        """
        Save a frame to disk
        
        Args:
            frame: Frame to save
            filepath: Path where to save the image
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            cv2.imwrite(str(filepath), frame)
            logger.info(f"Frame saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving frame: {e}")
            return False
    
    def detect_faces(self, frame: np.ndarray) -> list:
        """
        Detect faces in a frame using Haar Cascade
        
        Args:
            frame: Input frame
            
        Returns:
            List of face rectangles [(x, y, w, h), ...]
        """
        try:
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Load the pre-trained Haar Cascade classifier
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            
            # Detect faces
            faces = face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(30, 30)
            )
            
            return faces.tolist() if len(faces) > 0 else []
        except Exception as e:
            logger.error(f"Error detecting faces: {e}")
            return []
    
    def annotate_frame(self, frame: np.ndarray, faces: list) -> np.ndarray:
        """
        Draw rectangles around detected faces
        
        Args:
            frame: Input frame
            faces: List of face rectangles from detect_faces()
            
        Returns:
            Annotated frame
        """
        annotated = frame.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(annotated, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return annotated
    
    def __del__(self):
        """Cleanup on deletion"""
        self.stop_camera()


# Global instance
_cv_instance = None


def get_vision_instance() -> ComputerVision:
    """Get or create the global computer vision instance"""
    global _cv_instance
    if _cv_instance is None:
        _cv_instance = ComputerVision()
    return _cv_instance
