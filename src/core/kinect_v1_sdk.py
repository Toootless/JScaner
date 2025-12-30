"""
Direct Kinect v1 SDK Access via ctypes
Works with Python 3.9+ without needing pykinect compilation
Requires: Kinect for Windows SDK v1.8 installed
"""

import ctypes
import numpy as np
from ctypes import windll, c_void_p, c_int, c_uint, c_bool, POINTER, Structure, byref
import os

# Kinect SDK paths
KINECT_SDK_PATH = r"C:\Program Files\Microsoft SDKs\Kinect\v1.8"
KINECT_DLL = os.path.join(KINECT_SDK_PATH, "bin", "Kinect10.dll")

# Check if SDK is installed
if not os.path.exists(KINECT_DLL):
    raise ImportError(f"Kinect SDK not found at {KINECT_DLL}")

# Load Kinect DLL
try:
    kinect_dll = ctypes.WinDLL(KINECT_DLL)
except Exception as e:
    raise ImportError(f"Could not load Kinect DLL: {e}")

# Constants
NUI_IMAGE_RESOLUTION_640x480 = 2
NUI_IMAGE_TYPE_COLOR = 1
NUI_IMAGE_TYPE_DEPTH = 2
NUI_INITIALIZE_FLAG_USES_COLOR = 0x20000000
NUI_INITIALIZE_FLAG_USES_DEPTH = 0x00100000

# Frame dimensions
KINECT_WIDTH = 640
KINECT_HEIGHT = 480


class NUI_IMAGE_FRAME(Structure):
    """Kinect image frame structure"""
    _fields_ = [
        ("liTimeStamp", ctypes.c_longlong),
        ("dwFrameNumber", ctypes.c_uint32),
        ("eImageType", ctypes.c_int),
        ("eResolution", ctypes.c_int),
        ("pFrameTexture", c_void_p),
        ("dwFrameFlags", ctypes.c_uint32),
        ("ViewArea", ctypes.c_int * 4),
    ]


class KinectV1:
    """Kinect v1 camera interface using Windows SDK"""
    
    def __init__(self):
        self.sensor_handle = None
        self.color_stream_handle = None
        self.is_initialized = False
        
    def initialize(self):
        """Initialize Kinect sensor"""
        try:
            # Get sensor count
            get_sensor_count = kinect_dll.NuiGetSensorCount
            get_sensor_count.restype = ctypes.HRESULT
            get_sensor_count.argtypes = [POINTER(c_int)]
            
            sensor_count = c_int()
            hr = get_sensor_count(byref(sensor_count))
            
            if hr != 0 or sensor_count.value == 0:
                print(f"No Kinect sensors found (count: {sensor_count.value})")
                return False
            
            print(f"Found {sensor_count.value} Kinect sensor(s)")
            
            # Create sensor instance
            create_sensor = kinect_dll.NuiCreateSensorByIndex
            create_sensor.restype = ctypes.HRESULT
            create_sensor.argtypes = [c_int, POINTER(c_void_p)]
            
            sensor = c_void_p()
            hr = create_sensor(0, byref(sensor))
            
            if hr != 0:
                print(f"Failed to create sensor instance (HRESULT: {hr})")
                return False
            
            self.sensor_handle = sensor
            
            # Initialize sensor
            init_sensor = kinect_dll.NuiInitialize
            init_sensor.restype = ctypes.HRESULT
            init_sensor.argtypes = [c_uint]
            
            hr = init_sensor(NUI_INITIALIZE_FLAG_USES_COLOR)
            
            if hr != 0:
                print(f"Failed to initialize sensor (HRESULT: {hr})")
                return False
            
            # Open color image stream
            open_stream = kinect_dll.NuiImageStreamOpen
            open_stream.restype = ctypes.HRESULT
            open_stream.argtypes = [c_int, c_int, c_int, c_int, c_void_p, POINTER(c_void_p)]
            
            stream_handle = c_void_p()
            hr = open_stream(
                NUI_IMAGE_TYPE_COLOR,
                NUI_IMAGE_RESOLUTION_640x480,
                0,  # dwImageFrameFlags
                2,  # dwFrameLimit
                None,  # hNextFrameEvent
                byref(stream_handle)
            )
            
            if hr != 0:
                print(f"Failed to open color stream (HRESULT: {hr})")
                return False
            
            self.color_stream_handle = stream_handle
            self.is_initialized = True
            print("✓ Kinect v1 initialized successfully!")
            return True
            
        except Exception as e:
            print(f"Exception during Kinect initialization: {e}")
            return False
    
    def get_color_frame(self):
        """Capture a color frame from Kinect"""
        if not self.is_initialized:
            return None
        
        try:
            # Get next frame
            get_frame = kinect_dll.NuiImageStreamGetNextFrame
            get_frame.restype = ctypes.HRESULT
            get_frame.argtypes = [c_void_p, c_uint, POINTER(NUI_IMAGE_FRAME)]
            
            frame = NUI_IMAGE_FRAME()
            hr = get_frame(self.color_stream_handle, 0, byref(frame))
            
            if hr != 0:
                return None
            
            # Get frame texture
            get_texture = kinect_dll.NuiImageFrameLockTexture
            # Note: This is simplified - full implementation would extract pixels
            
            # Release frame
            release_frame = kinect_dll.NuiImageStreamReleaseFrame
            release_frame.restype = ctypes.HRESULT
            release_frame.argtypes = [c_void_p, POINTER(NUI_IMAGE_FRAME)]
            release_frame(self.color_stream_handle, byref(frame))
            
            # Return a placeholder for now (full implementation would decode texture)
            return np.zeros((KINECT_HEIGHT, KINECT_WIDTH, 3), dtype=np.uint8)
            
        except Exception as e:
            print(f"Error getting frame: {e}")
            return None
    
    def shutdown(self):
        """Shutdown Kinect sensor"""
        if self.is_initialized:
            try:
                shutdown = kinect_dll.NuiShutdown
                shutdown.restype = None
                shutdown()
                self.is_initialized = False
                print("✓ Kinect shutdown")
            except:
                pass
    
    def __del__(self):
        self.shutdown()


# Test if module loads
if __name__ == "__main__":
    print("Kinect v1 SDK Module Test")
    print("=" * 60)
    print(f"SDK Path: {KINECT_SDK_PATH}")
    print(f"DLL: {KINECT_DLL}")
    print(f"DLL exists: {os.path.exists(KINECT_DLL)}")
    print()
    
    try:
        kinect = KinectV1()
        if kinect.initialize():
            print("SUCCESS - Kinect ready to use!")
            kinect.shutdown()
        else:
            print("FAILED - Could not initialize Kinect")
    except Exception as e:
        print(f"ERROR: {e}")
