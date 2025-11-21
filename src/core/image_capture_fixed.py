"""
Image Capture Module

Handles camera interface and image acquisition for 3D scanning with improved error handling.
"""

import cv2
import numpy as np
import time
from typing import List, Optional, Tuple
import os

class ImageCapture:
    """Manages camera interface and image capture for 3D scanning."""
    
    def __init__(self, camera_id: int = 0):
        """
        Initialize camera capture.
        
        Args:
            camera_id: Camera device ID (usually 0 for default camera)
        """
        self.camera_id = camera_id
        self.cap = None
        self.is_recording = False
        
    def diagnose_camera_issues(self):
        """
        Run camera diagnostics to help troubleshoot issues.
        """
        print("\n=== Camera Diagnostics ===")
        
        # Check OpenCV version
        print(f"OpenCV version: {cv2.__version__}")
        
        # Test camera indices
        available_cameras = []
        for i in range(5):  # Check first 5 camera indices
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                available_cameras.append(f"Camera {i}: {width}x{height}")
                cap.release()
        
        if available_cameras:
            print("Available cameras:")
            for cam in available_cameras:
                print(f"  - {cam}")
        else:
            print("No cameras detected")
            print("\nTroubleshooting steps:")
            print("1. Check if camera is physically connected")
            print("2. Close other apps using the camera (Skype, Teams, etc.)")
            print("3. Try unplugging and reconnecting the camera")
            print("4. Check Windows Camera app works")
        
        print("========================\n")
        
    def initialize_camera(self) -> bool:
        """
        Initialize camera connection with improved error handling.
        
        Returns:
            True if camera initialized successfully, False otherwise
        """
        try:
            print("Attempting to initialize camera...")
            
            # Try different camera indices
            for camera_id in [0, 1, 2]:
                print(f"Trying camera index {camera_id}...")
                self.cap = cv2.VideoCapture(camera_id)
                
                if self.cap.isOpened():
                    print(f"Camera {camera_id} opened successfully")
                    self.camera_id = camera_id
                    break
                else:
                    if self.cap:
                        self.cap.release()
                    self.cap = None
            
            if self.cap is None or not self.cap.isOpened():
                print("No camera found on any index")
                return False
            
            print("Configuring camera settings...")
            
            # Get current resolution first
            current_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            current_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(f"Current resolution: {current_width}x{current_height}")
            
            # Try to set higher resolution (conservative approach)
            try:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
                
                # Verify settings
                width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = self.cap.get(cv2.CAP_PROP_FPS)
                print(f"Set resolution: {width}x{height} @ {fps}fps")
                
            except Exception as e:
                print(f"Warning: Could not set resolution: {e}")
            
            # Test frame capture
            ret, test_frame = self.cap.read()
            if not ret or test_frame is None:
                print("Camera opened but cannot read frames")
                return False
            
            print(f"Camera ready! Frame size: {test_frame.shape}")
            return True
            
        except Exception as e:
            print(f"Error initializing camera: {e}")
            if self.cap:
                self.cap.release()
                self.cap = None
            return False
    
    def get_frame(self) -> Optional[np.ndarray]:
        """
        Capture a single frame from the camera.
        
        Returns:
            Frame as numpy array, or None if capture failed
        """
        if self.cap is None or not self.cap.isOpened():
            return None
            
        ret, frame = self.cap.read()
        if ret:
            return frame
        return None
    
    def capture_image(self, save_path: Optional[str] = None) -> Optional[np.ndarray]:
        """
        Capture and optionally save a single image.
        
        Args:
            save_path: Path to save the image (optional)
            
        Returns:
            Captured image as numpy array
        """
        frame = self.get_frame()
        if frame is not None and save_path:
            cv2.imwrite(save_path, frame)
        return frame
    
    def capture_sequence(self, num_images: int, delay_seconds: float = 2.0, 
                        save_directory: Optional[str] = None) -> List[np.ndarray]:
        """
        Capture a sequence of images with delays.
        
        Args:
            num_images: Number of images to capture
            delay_seconds: Delay between captures
            save_directory: Directory to save images (optional)
            
        Returns:
            List of captured images
        """
        images = []
        
        if save_directory and not os.path.exists(save_directory):
            os.makedirs(save_directory)
        
        for i in range(num_images):
            print(f"Capturing image {i+1}/{num_images}...")
            
            # Wait for user to position object
            if i > 0:
                time.sleep(delay_seconds)
            
            frame = self.get_frame()
            if frame is not None:
                images.append(frame.copy())
                
                if save_directory:
                    filename = f"capture_{i+1:03d}.jpg"
                    save_path = os.path.join(save_directory, filename)
                    cv2.imwrite(save_path, frame)
                    print(f"Saved: {save_path}")
            else:
                print(f"Failed to capture image {i+1}")
        
        return images
    
    def preview_camera(self, window_name: str = "Camera Preview") -> List[np.ndarray]:
        """
        Show live camera preview. Press 'q' to quit, 'c' to capture.
        
        Args:
            window_name: Name of the preview window
            
        Returns:
            List of captured images
        """
        if not self.initialize_camera():
            print("Failed to initialize camera")
            return []
        
        captured_images = []
        
        print("Camera preview started. Press 'c' to capture, 'q' to quit.")
        
        while True:
            frame = self.get_frame()
            if frame is None:
                break
            
            # Add instructions overlay
            cv2.putText(frame, "Press 'c' to capture, 'q' to quit", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Captured: {len(captured_images)}", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow(window_name, frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                captured_images.append(frame.copy())
                print(f"Image {len(captured_images)} captured!")
        
        cv2.destroyAllWindows()
        return captured_images
    
    def get_camera_info(self) -> dict:
        """
        Get camera properties and capabilities.
        
        Returns:
            Dictionary with camera information
        """
        if self.cap is None:
            return {}
        
        try:
            info = {
                'width': int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                'height': int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'fps': self.cap.get(cv2.CAP_PROP_FPS),
                'brightness': self.cap.get(cv2.CAP_PROP_BRIGHTNESS),
                'contrast': self.cap.get(cv2.CAP_PROP_CONTRAST),
                'saturation': self.cap.get(cv2.CAP_PROP_SATURATION),
                'hue': self.cap.get(cv2.CAP_PROP_HUE),
                'is_c920_compatible': self.detect_c920()
            }
            return info
        except Exception as e:
            print(f"Error getting camera info: {e}")
            return {}
    
    def detect_c920(self) -> bool:
        """
        Detect if connected camera supports high resolution (C920-like).
        
        Returns:
            True if high-res camera detected, False otherwise
        """
        if self.cap is None:
            return False
            
        try:
            # Check if we can set high resolution
            current_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            current_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            
            # Try setting HD resolution
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            
            new_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            new_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            
            # Restore original settings
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, current_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, current_height)
            
            # If it accepted 1920x1080, likely HD camera
            return new_width >= 1920 and new_height >= 1080
            
        except Exception:
            return False
    
    def optimize_for_3d_scanning(self):
        """
        Apply optimal settings for 3D scanning.
        """
        if self.cap is None:
            return
            
        try:
            # Try high resolution first
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            
            # If that fails, use conservative settings
            if self.cap.get(cv2.CAP_PROP_FRAME_WIDTH) < 1920:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
            # Try to optimize other settings
            try:
                self.cap.set(cv2.CAP_PROP_CONTRAST, 0.6)
            except:
                pass
                
            print("Camera optimized for 3D scanning")
            
        except Exception as e:
            print(f"Warning: Could not optimize camera settings: {e}")
    
    def release(self):
        """Release camera resources."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    def __del__(self):
        """Destructor to ensure camera is released."""
        self.release()