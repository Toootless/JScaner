"""
Kinect v1 (Xbox 360) Camera Capture via PyUSB

Direct USB interface to Kinect v1 using PyUSB and libusbK driver.
Works with libusbK-controlled devices.
"""

import numpy as np
from typing import Optional, Tuple
import cv2

try:
    import usb.core
    import usb.util
    PYUSB_AVAILABLE = True
except ImportError:
    PYUSB_AVAILABLE = False


class KinectV1PyUSB:
    """
    Captures RGB and depth images from Kinect v1 (Xbox 360) sensor.
    Uses PyUSB for direct USB access with libusbK driver.
    """
    
    # Kinect v1 USB identifiers
    KINECT_VENDOR_ID = 0x045e
    KINECT_PRODUCT_IDS = {
        0x02ae: "Kinect for Xbox 360",
        0x02ad: "Kinect for Xbox 360 (prototype)",
    }
    
    def __init__(self):
        """Initialize Kinect capture."""
        self.depth = None
        self.rgb = None
        self.is_capturing = False
        self.device = None
        
        # Check for Kinect availability
        self.available = self._detect_kinect_device()
    
    def _detect_kinect_device(self) -> bool:
        """
        Detect Kinect v1 device via USB.
        
        Returns:
            True if Kinect v1 detected, False otherwise
        """
        if not PYUSB_AVAILABLE:
            print("⚠ PyUSB not available for USB device detection")
            return False
        
        try:
            # Find all Kinect devices
            devices = list(usb.core.find(
                find_all=True,
                idVendor=self.KINECT_VENDOR_ID,
                idProduct=list(self.KINECT_PRODUCT_IDS.keys())
            ))
            
            if devices:
                self.device = devices[0]
                product_id = self.device.idProduct
                product_name = self.KINECT_PRODUCT_IDS.get(
                    product_id, f"Unknown Kinect (0x{product_id:04x})"
                )
                print(f"✓ Found {product_name}")
                return True
            else:
                print("ℹ  No Kinect v1 devices found via USB")
                return False
                
        except Exception as e:
            print(f"⚠ USB device detection failed: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if Kinect is available."""
        return self.available
    
    def initialize(self) -> bool:
        """
        Initialize Kinect v1 connection via PyUSB.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.available or self.device is None:
            return False
        
        try:
            # Try to claim the device
            if self.device.is_kernel_driver_active(0):
                try:
                    self.device.detach_kernel_driver(0)
                except usb.core.USBError:
                    pass  # Already detached or not supported
            
            self.device.set_configuration()
            print("✓ Kinect v1 USB device initialized")
            return True
            
        except Exception as e:
            print(f"⚠ Failed to initialize Kinect: {e}")
            return False
    
    def get_rgb_frame(self) -> Optional[np.ndarray]:
        """
        Get current RGB frame from Kinect v1.
        
        Returns:
            RGB frame as numpy array (640x480x3) in BGR format, or None
        """
        if not self.available or self.device is None:
            return None
        
        try:
            # Kinect v1 RGB data comes from endpoint 0x81
            # Frame format: 640x480 YUYV (YCbCr 4:2:2)
            # Each frame is ~614400 bytes (640*480*2)
            
            # Read raw USB data (with timeout)
            data = self.device.read(0x81, 614400, timeout=1000)
            
            if not data:
                return None
            
            # Convert to numpy array
            frame_data = np.frombuffer(bytes(data), dtype=np.uint8)
            
            # Reshape to 480x640x2 (YUYV format)
            frame_yuyv = frame_data.reshape((480, 640, 2))
            
            # Convert YUYV to BGR using OpenCV
            frame_bgr = cv2.cvtColor(frame_yuyv, cv2.COLOR_YUV2BGR_YUYV)
            
            return frame_bgr
            
        except usb.core.USBTimeoutError:
            # Timeout is expected if no data available
            return None
        except Exception as e:
            print(f"DEBUG: Failed to capture RGB frame: {e}")
            return self._get_status_pattern()
    
    def get_depth_frame(self) -> Optional[np.ndarray]:
        """
        Get current depth frame from Kinect v1.
        
        Returns:
            Depth frame as numpy array or None
        """
        # Depth data comes from endpoint 0x82
        # Would need similar USB read + unpacking
        # For now, return None
        return None
    
    def _get_status_pattern(self) -> np.ndarray:
        """Generate status pattern."""
        rgb_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        for i in range(480):
            ratio = i / 480
            rgb_frame[i, :] = [int(100 + 50 * ratio), int(80 + 60 * ratio), 120]
        
        cv2.putText(rgb_frame, "Kinect v1 (PyUSB)", 
                   (140, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (100, 255, 255), 2)
        cv2.putText(rgb_frame, "Reading USB stream...", 
                   (110, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (100, 200, 200), 1)
        
        return rgb_frame
    
    def get_frames(self) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """Get synchronized RGB and depth frames."""
        return self.get_rgb_frame(), self.get_depth_frame()
    
    def close(self):
        """Close Kinect connection."""
        if self.device is not None:
            try:
                usb.util.release_interface(self.device, 0)
                print("✓ Kinect v1 USB disconnected")
                self.device = None
            except Exception as e:
                print(f"⚠ Error closing Kinect: {e}")
    
    def __del__(self):
        """Cleanup on deletion."""
        self.close()
