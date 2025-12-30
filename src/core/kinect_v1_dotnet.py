"""
Kinect v1 Camera Interface using .NET SDK via pythonnet
Works with Kinect for Windows SDK v1.8 and Python 3.9+

Requirements:
- Kinect for Windows SDK v1.8 installed
- pythonnet package (pip install pythonnet)
"""

import sys
import os
import numpy as np

try:
    import clr
except ImportError:
    raise ImportError("pythonnet not installed. Run: pip install pythonnet")

# Add Kinect SDK assembly path
KINECT_SDK_PATH = r"C:\Program Files\Microsoft SDKs\Kinect\v1.8\Assemblies"
KINECT_ASSEMBLY = os.path.join(KINECT_SDK_PATH, "Microsoft.Kinect.dll")

if not os.path.exists(KINECT_ASSEMBLY):
    raise FileNotFoundError(f"Kinect SDK assembly not found at: {KINECT_ASSEMBLY}")

# Load Kinect assembly
sys.path.append(KINECT_SDK_PATH)
clr.AddReference("Microsoft.Kinect")

from Microsoft.Kinect import KinectSensor, ColorImageFormat, DepthImageFormat
from System import Array, Byte


class KinectV1Camera:
    """Kinect v1 Camera wrapper using .NET SDK"""
    
    def __init__(self):
        self.sensor = None
        self.is_running = False
        self.frame_width = 640
        self.frame_height = 480
        self.latest_frame = None
        
    def initialize(self):
        """Initialize Kinect sensor"""
        try:
            # Get first available Kinect sensor
            sensors = KinectSensor.KinectSensors
            
            if sensors.Count == 0:
                print("ERROR: No Kinect sensors detected")
                return False
            
            self.sensor = sensors[0]
            print(f"Found Kinect sensor: {self.sensor.UniqueKinectId}")
            
            # Enable color stream
            self.sensor.ColorStream.Enable(ColorImageFormat.RgbResolution640x480Fps30)
            
            # Start sensor
            self.sensor.Start()
            
            # Wait for sensor to be ready
            import time
            time.sleep(1)
            
            if self.sensor.IsRunning:
                self.is_running = True
                print("✓ Kinect v1 initialized successfully!")
                print(f"  Resolution: {self.frame_width}x{self.frame_height}")
                print(f"  Status: {self.sensor.Status}")
                return True
            else:
                print("ERROR: Kinect sensor failed to start")
                return False
                
        except Exception as e:
            print(f"ERROR initializing Kinect: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_frame(self):
        """
        Capture a color frame from Kinect
        
        Returns:
            numpy.ndarray: BGR image in OpenCV format (H, W, 3) or None if failed
        """
        if not self.is_running or self.sensor is None:
            return None
        
        try:
            # Get color frame (don't use context manager - not supported in pythonnet)
            color_frame = self.sensor.ColorStream.OpenNextFrame(100)
            
            if color_frame is None:
                return None
            
            try:
                # Get pixel data
                pixel_data = color_frame.GetRawPixelData()
                
                # Convert to numpy array
                # Kinect SDK returns BGRA format (4 bytes per pixel)
                frame_array = np.frombuffer(
                    Array[Byte](pixel_data),
                    dtype=np.uint8
                ).reshape((self.frame_height, self.frame_width, 4))
                
                # Convert BGRA to BGR (remove alpha channel)
                frame_bgr = frame_array[:, :, :3].copy()
                
                # Store latest frame
                self.latest_frame = frame_bgr
                
                return frame_bgr
            finally:
                # Always dispose the frame
                color_frame.Dispose()
                
        except Exception as e:
            print(f"Error capturing frame: {e}")
            return None
    
    def read(self):
        """
        OpenCV-compatible read method
        
        Returns:
            tuple: (success: bool, frame: numpy.ndarray)
        """
        frame = self.get_frame()
        return (frame is not None, frame)
    
    def isOpened(self):
        """Check if camera is opened (OpenCV compatible)"""
        return self.is_running
    
    def release(self):
        """Stop and release Kinect sensor"""
        if self.sensor is not None:
            try:
                if self.sensor.IsRunning:
                    self.sensor.Stop()
                self.sensor.Dispose()
                print("✓ Kinect sensor released")
            except:
                pass
            self.sensor = None
            self.is_running = False
    
    def __del__(self):
        """Cleanup when object is deleted"""
        self.release()
    
    # OpenCV-compatible properties
    def get(self, prop_id):
        """Get camera property (OpenCV compatible)"""
        # cv2.CAP_PROP_FRAME_WIDTH = 3
        # cv2.CAP_PROP_FRAME_HEIGHT = 4
        # cv2.CAP_PROP_FPS = 5
        if prop_id == 3:  # WIDTH
            return self.frame_width
        elif prop_id == 4:  # HEIGHT
            return self.frame_height
        elif prop_id == 5:  # FPS
            return 30.0
        return 0.0


# Test function
def test_kinect():
    """Test Kinect camera functionality"""
    print("=" * 70)
    print("Kinect v1 .NET SDK Test")
    print("=" * 70)
    print()
    
    try:
        kinect = KinectV1Camera()
        
        print("[1/3] Initializing Kinect...")
        if not kinect.initialize():
            print("FAILED: Could not initialize Kinect")
            return False
        
        print()
        print("[2/3] Capturing test frame...")
        frame = kinect.get_frame()
        
        if frame is not None:
            print(f"✓ Frame captured: {frame.shape}, dtype: {frame.dtype}")
            print(f"  Frame statistics:")
            print(f"    - Mean pixel value: {frame.mean():.2f}")
            print(f"    - Min/Max: {frame.min()}/{frame.max()}")
            
            # Try to save frame
            try:
                import cv2
                test_file = "kinect_test_frame.jpg"
                cv2.imwrite(test_file, frame)
                print(f"✓ Test frame saved: {test_file}")
            except:
                print("  (OpenCV not available for saving)")
        else:
            print("✗ Failed to capture frame")
            kinect.release()
            return False
        
        print()
        print("[3/3] Testing continuous capture...")
        success_count = 0
        for i in range(5):
            ret, frame = kinect.read()
            if ret:
                success_count += 1
                print(f"  Frame {i+1}/5: ✓ {frame.shape}")
            else:
                print(f"  Frame {i+1}/5: ✗ Failed")
        
        kinect.release()
        
        print()
        print("=" * 70)
        if success_count >= 3:
            print("SUCCESS: Kinect is working correctly!")
            print()
            print("Next steps:")
            print("  1. Run the scanner GUI with Python 3.9:")
            print("     C:\\Users\\johnj\\AppData\\Local\\Programs\\Python\\Python39\\python.exe kinect_scanner_gui.py")
            print("  2. Select 'Kinect v1' from the camera dropdown")
            print("  3. Start capturing!")
        else:
            print("PARTIAL SUCCESS: Some frames captured but unstable")
        print("=" * 70)
        
        return success_count >= 3
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_kinect()
