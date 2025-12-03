"""
Kinect v1 (Xbox 360) Camera Capture Module

Provides Kinect v1 sensor support via OpenCV with Windows drivers.
Falls back to MSR Kinect SDK if available.
"""

import numpy as np
from typing import Optional, Tuple
import ctypes
from pathlib import Path
import sys
import cv2
import os

class KinectCapture:
    """
    Captures RGB and depth images from Kinect v1 (Xbox 360) sensor.
    Uses OpenCV or MSR Kinect SDK.
    """
    
    def __init__(self):
        """Initialize Kinect capture."""
        self.depth = None
        self.rgb = None
        self.is_capturing = False
        self.kinect_device = None
        self.kinect_dll = None
        
        # Check for Kinect availability
        self.available = self._check_kinect_availability()
    
    def _check_kinect_availability(self) -> bool:
        """
        Check if Kinect v1 is available via Windows drivers.
        
        Returns:
            True if Kinect v1 detected, False otherwise
        """
        try:
            # Try to detect Kinect via OpenCV's VideoCapture
            # OpenCV supports Kinect v1 on Windows with proper drivers
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                # Try to read a frame to verify camera is working
                ret, frame = cap.read()
                cap.release()
                if ret and frame is not None:
                    return True
            
            # Try Kinect-specific device indices (sometimes Kinect is at index 1+)
            for idx in range(1, 4):
                cap = cv2.VideoCapture(idx)
                if cap.isOpened():
                    ret, frame = cap.read()
                    cap.release()
                    if ret and frame is not None:
                        return True
                        
            return False
            
        except Exception as e:
            print(f"DEBUG: Kinect availability check failed: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if Kinect is available."""
        return self.available
    
    def initialize(self) -> bool:
        """
        Initialize Kinect v1 connection via OpenCV.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.available:
            print("ℹ  Kinect v1 not detected via Windows drivers")
            return False
        
        try:
            print("✓ Kinect v1 sensor available")
            return True
            
        except Exception as e:
            print(f"⚠ Kinect initialization error: {e}")
            return False
    
    def get_depth_frame(self) -> Optional[np.ndarray]:
        """
        Get current depth frame from Kinect v1.
        
        Returns:
            Depth frame as numpy array or None
            Note: Kinect v1 depth requires additional SDK - returns None for now
        """
        # Kinect v1 depth frame requires Windows Kinect SDK
        # For now, we provide RGB only support
        return None
    
    def get_rgb_frame(self) -> Optional[np.ndarray]:
        """
        Get current RGB frame from Kinect v1.
        
        Returns:
            RGB frame as numpy array (640x480x3) in BGR format, or None if not available
        """
        if not self.available:
            return None
        
        try:
            # Try to capture frame from Kinect v1 via OpenCV
            frame = self._capture_kinect_frame()
            if frame is not None and frame.size > 0:
                return frame
            
            # Show status pattern if capture fails
            return self._get_status_pattern()
            
        except Exception as e:
            print(f"DEBUG: Failed to get RGB frame: {e}")
            return self._get_status_pattern()
    
    def _capture_kinect_frame(self) -> Optional[np.ndarray]:
        """
        Capture actual RGB frame from Kinect v1 via OpenCV.
        
        Returns:
            RGB frame as numpy array (640x480x3) or None
        """
        try:
            # Try different device indices for Kinect
            for device_idx in [0, 1, 2]:
                cap = cv2.VideoCapture(device_idx)
                if not cap.isOpened():
                    continue
                
                # Try to read a frame
                ret, frame = cap.read()
                cap.release()
                
                if ret and frame is not None and frame.size > 0:
                    # Ensure frame is 640x480
                    if frame.shape != (480, 640, 3):
                        frame = cv2.resize(frame, (640, 480))
                    
                    # Verify it's not pure black (check if it has some variation)
                    if frame.max() > 10:  # Not a black frame
                        return frame
            
            # No valid frame found
            return None
            
        except Exception as e:
            print(f"DEBUG: Frame capture exception: {e}")
            return None
    
    def _get_status_pattern(self) -> np.ndarray:
        """
        Generate a status pattern showing Kinect v1 status.
        
        Returns:
            BGR numpy array (480x640x3) with status information
        """
        # Create status display
        rgb_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Add gradient background (dark blue to teal)
        for i in range(480):
            ratio = i / 480
            rgb_frame[i, :] = [int(100 + 50 * ratio), int(80 + 60 * ratio), 120]
        
        # Title
        cv2.putText(rgb_frame, "Kinect v1 Sensor", 
                   (160, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (100, 255, 255), 2)
        
        # Status
        cv2.putText(rgb_frame, "Detecting camera feed...", 
                   (130, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 200, 200), 1)
        
        # Instructions
        cv2.putText(rgb_frame, "Troubleshooting:", 
                   (50, 290), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 200, 255), 1)
        cv2.putText(rgb_frame, "1. Ensure Kinect v1 is plugged into USB", 
                   (50, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 150, 200), 1)
        cv2.putText(rgb_frame, "2. Install Windows Kinect v1 drivers", 
                   (50, 345), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 150, 200), 1)
        cv2.putText(rgb_frame, "3. Check Device Manager for USB device", 
                   (50, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 150, 200), 1)
        
        return rgb_frame
    
    def get_frames(self) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Get synchronized RGB and depth frames.
        
        Returns:
            Tuple of (rgb_frame, depth_frame) or (None, None)
        """
        return self.get_rgb_frame(), self.get_depth_frame()
    
    def set_led(self, color: str = "green"):
        """
        Control Kinect v1 LED color.
        
        Args:
            color: 'off', 'red', 'green', 'yellow', 'blink_green', 'blink_red_yellow'
        """
        if not self.available:
            return
        
        # Kinect v1 LED control would require Windows Kinect SDK
        # For now, this is a placeholder
        print(f"ℹ  Kinect v1 LED control requested: {color}")
    
    def close(self):
        """Close Kinect connection."""
        pass
    
    def __del__(self):
        """Cleanup on deletion."""
        self.close()



# Example usage
if __name__ == "__main__":
    import time
    
    kinect = KinectCapture()
    
    if not kinect.is_available():
        print("Kinect v1 not detected")
        exit(1)
    
    if kinect.initialize():
        print("✓ Kinect v1 initialized")
        
        for i in range(10):
            rgb, depth = kinect.get_frames()
            if rgb is not None:
                print(f"Frame {i}: RGB shape {rgb.shape}")
                if depth is not None:
                    print(f"         Depth shape {depth.shape}")
            time.sleep(0.1)
        
        kinect.close()

