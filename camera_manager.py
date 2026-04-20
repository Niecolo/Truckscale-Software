"""
Camera Manager for Truck Scale Weighing System.
Handles camera operations including device detection, feed capture, and display.
"""

import cv2
import threading
import time
import logging
from typing import Optional, Callable, List
import tkinter as tk
from PIL import Image, ImageTk


class CameraManager:
    """Manages camera operations for the weighing scale system."""
    
    def __init__(self, msg_box=None):
        """Initialize the camera manager.
        
        Args:
            msg_box: Message box instance for displaying messages
        """
        self.msg_box = msg_box
        self.logger = logging.getLogger(__name__)
        
        # Camera variables
        self.current_camera_index = 0
        self.camera = None
        self.is_running = False
        self.capture_thread = None
        self.mirror_mode = False  # New mirror mode flag
        
        # Callback for frame updates
        self.frame_callback: Optional[Callable] = None
        
        # Available cameras
        self.available_cameras = []
        self._detect_available_cameras()
        
    def _detect_available_cameras(self) -> List[int]:
        """Detect available camera devices.
        
        Returns:
            List of available camera indices
        """
        self.available_cameras = []
        
        # Test camera indices 0-9
        for i in range(10):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                self.available_cameras.append(i)
                cap.release()
                
        self.logger.info(f"Found {len(self.available_cameras)} cameras: {self.available_cameras}")
        return self.available_cameras
    
    def get_available_cameras(self) -> List[str]:
        """Get list of available camera names.
        
        Returns:
            List of camera display names
        """
        camera_names = []
        for i in self.available_cameras:
            camera_names.append(f"Camera {i}")
        return camera_names
    
    def set_frame_callback(self, callback: Callable):
        """Set callback function for frame updates.
        
        Args:
            callback: Function to call with new frames
        """
        self.frame_callback = callback
    
    def connect_camera(self, camera_index: int) -> bool:
        """Connect to a camera.
        
        Args:
            camera_index: Index of camera to connect to
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Disconnect current camera if any
            self.disconnect_camera()
            
            # Connect to new camera
            self.current_camera_index = camera_index
            self.camera = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
            
            if not self.camera.isOpened():
                self.logger.error(f"Failed to open camera {camera_index}")
                if self.msg_box:
                    self.msg_box.showerror("Camera Error", f"Failed to connect to Camera {camera_index}")
                return False
            
            # Set camera properties for better performance
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            self.logger.info(f"Successfully connected to camera {camera_index}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error connecting to camera {camera_index}: {e}")
            if self.msg_box:
                self.msg_box.showerror("Camera Error", f"Error connecting to camera: {e}")
            return False
    
    def disconnect_camera(self):
        """Disconnect current camera."""
        self.stop_capture()
        
        if self.camera:
            self.camera.release()
            self.camera = None
            self.logger.info("Camera disconnected")
    
    def start_capture(self) -> bool:
        """Start capturing frames from camera.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.camera or not self.camera.isOpened():
            self.logger.error("No camera connected")
            return False
        
        if self.is_running:
            self.logger.warning("Camera capture already running")
            return True
        
        self.is_running = True
        self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.capture_thread.start()
        
        self.logger.info("Camera capture started")
        return True
    
    def stop_capture(self):
        """Stop capturing frames."""
        self.is_running = False
        
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=1.0)
        
        self.logger.info("Camera capture stopped")
    
    def set_mirror_mode(self, enabled: bool):
        """Enable or disable mirror mode.
        
        Args:
            enabled: True to enable mirror mode, False to disable
        """
        self.mirror_mode = enabled
    
    def _capture_loop(self):
        """Main capture loop running in separate thread."""
        while self.is_running and self.camera and self.camera.isOpened():
            try:
                ret, frame = self.camera.read()
                if not ret:
                    self.logger.warning("Failed to read frame from camera")
                    break
                
                # Compress frame by resizing
                frame = self._compress_frame(frame)
                
                # Apply mirror mode if enabled
                if self.mirror_mode:
                    frame = cv2.flip(frame, 1)  # Flip horizontally
                
                # Convert to RGB and create PIL Image
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb)
                
                # Convert to PhotoImage for tkinter
                photo = ImageTk.PhotoImage(image=image)
                
                # Call callback with new frame (pass both PIL image and PhotoImage)
                if self.frame_callback:
                    self.frame_callback(photo, image)
                
                # Control frame rate (30 FPS)
                time.sleep(1/30)
                
            except Exception as e:
                self.logger.error(f"Error in capture loop: {e}")
                break
        
        self.is_running = False
    
    def _compress_frame(self, frame, max_width: int = 320, max_height: int = 240):
        """Compress frame by resizing.
        
        Args:
            frame: Input frame
            max_width: Maximum width
            max_height: Maximum height
            
        Returns:
            Compressed frame
        """
        height, width = frame.shape[:2]
        
        # Calculate scaling factor
        scale = min(max_width / width, max_height / height, 1.0)
        
        if scale < 1.0:
            new_width = int(width * scale)
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        return frame
    
    def capture_snapshot(self) -> Optional[Image.Image]:
        """Capture a single snapshot from current camera.
        
        Returns:
            PIL Image if successful, None otherwise
        """
        if not self.camera or not self.camera.isOpened():
            return None
        
        try:
            ret, frame = self.camera.read()
            if not ret:
                return None
            
            # Convert to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return Image.fromarray(frame_rgb)
            
        except Exception as e:
            self.logger.error(f"Error capturing snapshot: {e}")
            return None
    
    def is_camera_connected(self) -> bool:
        """Check if camera is connected and running.
        
        Returns:
            True if camera is connected, False otherwise
        """
        return self.camera is not None and self.camera.isOpened()
    
    def get_camera_info(self) -> dict:
        """Get information about current camera.
        
        Returns:
            Dictionary with camera information
        """
        if not self.camera or not self.camera.isOpened():
            return {"connected": False}
        
        return {
            "connected": True,
            "index": self.current_camera_index,
            "width": int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": int(self.camera.get(cv2.CAP_PROP_FPS)),
            "capturing": self.is_running
        }
    
    def cleanup(self):
        """Clean up resources."""
        self.disconnect_camera()
        self.logger.info("Camera manager cleaned up")
