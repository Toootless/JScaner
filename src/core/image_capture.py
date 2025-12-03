"""
Image Capture Module

Handles camera interface and image acquisition for 3D scanning with improved error handling.
Supports both standard webcams and Kinect v1 (Xbox 360) sensors.
"""

import cv2
import numpy as np
import time
from typing import List, Optional, Tuple
import os
from pathlib import Path

# Try to import Kinect support
try:
    from .kinect_capture import KinectCapture
    KINECT_AVAILABLE = True
except ImportError:
    KINECT_AVAILABLE = False

class ImageCapture:
    """Manages camera interface and image capture for 3D scanning."""
    
    def __init__(self, camera_id: int = 0, use_kinect: bool = True):
        """
        Initialize camera capture.
        
        Args:
            camera_id: Camera device ID (usually 0 for default camera)
            use_kinect: Try to use Kinect if available (True) or force webcam (False)
        """
        self.camera_id = camera_id
        self.cap = None
        self.is_recording = False
        self.use_kinect = use_kinect
        self.kinect = None
        self.kinect_active = False
        self.current_camera_type = None  # Track which camera is active
        
        # Try to initialize Kinect if enabled
        if KINECT_AVAILABLE and use_kinect:
            self.kinect = KinectCapture()
            if self.kinect.is_available() and self.kinect.initialize():
                self.kinect_active = True
                self.current_camera_type = "kinect"
                print("✓ Kinect sensor initialized and ready")
            else:
                print("⚠ Kinect not available, will use webcam")
                self.kinect = None
                self.kinect_active = False
    
    def switch_camera(self, use_kinect: bool) -> bool:
        """
        Switch between Kinect and webcam at runtime.
        
        Args:
            use_kinect: True to use Kinect, False to use webcam
            
        Returns:
            True if switch was successful, False otherwise
        """
        print(f"\n📷 Switching camera... {'Kinect' if use_kinect else 'Webcam'}")
        
        # Stop current camera
        if self.is_recording or self.cap is not None or self.kinect_active:
            self.release()
        
        self.use_kinect = use_kinect
        
        if use_kinect:
            # Try to switch to Kinect
            if KINECT_AVAILABLE and self.kinect is None:
                self.kinect = KinectCapture()
            
            if self.kinect and self.kinect.is_available():
                if self.kinect.initialize():
                    self.kinect_active = True
                    self.current_camera_type = "kinect"
                    print("✓ Switched to Kinect v1")
                    return True
                else:
                    print("⚠ Failed to initialize Kinect")
                    self.kinect_active = False
                    return False
            else:
                print("⚠ Kinect not available")
                return False
        else:
            # Switch to webcam
            self.kinect_active = False
            if self.initialize_camera():
                self.current_camera_type = "webcam"
                print("✓ Switched to Webcam")
                return True
            else:
                print("⚠ Failed to initialize Webcam")
                return False
        
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
        Initialize camera connection with proper LED activation.
        
        Returns:
            True if camera initialized successfully, False otherwise
        """
        try:
            print("Attempting to initialize camera...")
            
            # If Kinect is active, just return True - will use frame display
            if self.kinect_active and self.kinect is not None:
                print("Using Kinect v1 for preview (test pattern)")
                return True
            
            # Release any existing capture first
            if self.cap is not None:
                self.cap.release()
                self.cap = None
                time.sleep(0.5)  # Give time for release
            
            # Try different camera backends and indices
            backends_to_try = [
                (cv2.CAP_DSHOW, "DirectShow"),    # Windows native - best for webcams
                (cv2.CAP_MSMF, "Media Foundation"), # Windows modern
                (cv2.CAP_ANY, "Auto")             # OpenCV auto-select
            ]
            
            # For Kinect, try camera indices 0, 1, 2 (Kinect often shows up as camera 1)
            for camera_id in [0, 1, 2]:
                for backend, backend_name in backends_to_try:
                    try:
                        print(f"Trying camera {camera_id} with {backend_name} backend...")
                        
                        # Create capture with specific backend
                        if backend == cv2.CAP_ANY:
                            self.cap = cv2.VideoCapture(camera_id)
                        else:
                            self.cap = cv2.VideoCapture(camera_id, backend)
                        
                        if self.cap.isOpened():
                            print(f"Camera {camera_id} opened with {backend_name}")
                            
                            # Set buffer size immediately to activate camera
                            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                            
                            # Try to read a frame to fully activate camera (this should turn on LED)
                            print("Activating camera (LED should turn on now)...")
                            for attempt in range(5):  # Try multiple reads
                                ret, test_frame = self.cap.read()
                                if ret and test_frame is not None:
                                    print(f"SUCCESS: Camera active! LED should be on. Frame size: {test_frame.shape}")
                                    self.camera_id = camera_id
                                    
                                    # Get final resolution
                                    width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                    height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                                    print(f"Camera resolution: {width}x{height}")
                                    
                                    return True
                                time.sleep(0.1)  # Brief pause between attempts
                            
                            print(f"Camera {camera_id} opened but cannot read frames with {backend_name}")
                        else:
                            print(f"Camera {camera_id} failed to open with {backend_name}")
                        
                        # Clean up failed attempt
                        if self.cap:
                            self.cap.release()
                        self.cap = None
                        
                    except Exception as e:
                        print(f"Error with camera {camera_id} and {backend_name}: {e}")
                        if self.cap:
                            self.cap.release()
                        self.cap = None
                        continue
            
            print("ERROR: No working camera found with any backend")
            return False
            
        except Exception as e:
            print(f"Fatal error initializing camera: {e}")
            if self.cap:
                self.cap.release()
                self.cap = None
            return False
    
    def is_camera_truly_active(self) -> bool:
        """
        Check if camera is truly active (LED should be on).
        
        Returns:
            True if camera is active and capturing
        """
        if self.cap is None or not self.cap.isOpened():
            return False
        
        try:
            # Try to read a frame
            ret, frame = self.cap.read()
            return ret and frame is not None
        except Exception:
            return False
    
    def get_frame(self) -> Optional[np.ndarray]:
        """
        Capture a single frame from the camera.
        
        Returns:
            Frame as numpy array, or None if capture failed
        """
        # Try Kinect first if active
        if self.kinect_active and self.kinect is not None:
            rgb_frame = self.kinect.get_rgb_frame()
            if rgb_frame is not None:
                return rgb_frame
        
        # Fallback to webcam
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
        Apply optimal settings for 3D scanning (call after successful initialization).
        """
        if self.cap is None:
            print("No camera to optimize")
            return
            
        try:
            print("Optimizing camera settings for 3D scanning...")
            
            # Try to improve resolution gradually
            current_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            current_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            print(f"Current resolution: {current_width}x{current_height}")
            
            # Try higher resolutions step by step
            resolutions_to_try = [
                (1920, 1080),  # Full HD
                (1280, 720),   # HD
                (800, 600),    # SVGA
            ]
            
            for width, height in resolutions_to_try:
                if width > current_width or height > current_height:
                    try:
                        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                        
                        # Check if it worked
                        new_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        new_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        
                        if new_width == width and new_height == height:
                            print(f"Successfully set resolution to {width}x{height}")
                            break
                        else:
                            print(f"Resolution {width}x{height} not supported")
                    except Exception as e:
                        print(f"Failed to set {width}x{height}: {e}")
            
            # Try other optimizations carefully
            try:
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer for real-time
                print("Reduced buffer size for real-time capture")
            except Exception:
                pass
                
            print("Camera optimization complete")
            
        except Exception as e:
            print(f"Warning: Could not optimize camera settings: {e}")
    
    def get_depth_frame(self) -> Optional[np.ndarray]:
        """
        Get depth frame from Kinect sensor.
        
        Returns:
            Depth frame as numpy array (512x424 float32) or None if not available
            Values in millimeters
        """
        if self.kinect_active and self.kinect is not None:
            return self.kinect.get_depth_frame()
        return None
    
    def has_depth_sensor(self) -> bool:
        """
        Check if a depth sensor (Kinect) is available.
        
        Returns:
            True if Kinect is active, False otherwise
        """
        return self.kinect_active and self.kinect is not None
    
    def get_camera_type(self) -> str:
        """
        Get the type of camera being used.
        
        Returns:
            "Kinect v1" if using Kinect, "Webcam" if using webcam
        """
        if self.kinect_active:
            return "Kinect v1"
        return "Webcam"
    
    def release(self):
        """Release camera resources."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
    
    def __del__(self):
        """Destructor to ensure camera is released."""
        self.release()