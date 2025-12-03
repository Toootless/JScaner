#!/usr/bin/env python3
"""Test Kinect device directly"""

import cv2
import numpy as np
import sys

print("Testing Kinect device access...\n")

# Try different camera indices
print("Scanning for available cameras:")
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"  Camera {i}: {width}x{height} @ {fps} fps")
        
        # Try to read a frame
        for attempt in range(5):
            ret, frame = cap.read()
            if ret and frame is not None and frame.max() > 0:
                print(f"    ✓ Frame captured: {frame.shape}")
                # Show first few pixel values
                print(f"    Sample pixels: {frame[100, 100]}")
                break
        else:
            print(f"    ⚠ No valid frames from camera {i}")
        
        cap.release()
    else:
        print(f"  Camera {i}: Not available")

print("\n" + "="*60)
print("Testing pykinect2:")
try:
    from pykinect2 import PyKinectRuntime, FrameSourceTypes
    print("✓ pykinect2 imported")
except Exception as e:
    print(f"✗ pykinect2 error: {e}")
    print("  This is expected on Python 3.11+ (struct size incompatibility)")

print("\n" + "="*60)
print("Testing libfreenect2 DLL directly:")
import ctypes
from pathlib import Path

dll_path = Path("C:/Users/johnj/Downloads/vcpkg/installed/x64-windows/bin/freenect2.dll")
try:
    freenect2 = ctypes.CDLL(str(dll_path))
    print(f"✓ libfreenect2 DLL loaded: {dll_path}")
    
    # List available functions
    print("\nTrying to access functions:")
    funcs_to_try = [
        'freenect2_new',
        'freenect2_openDefaultDevice', 
        'freenect2_getNumDevices',
        'freenect2_openDevice',
        'freenect2_closeDevice',
    ]
    
    for func_name in funcs_to_try:
        try:
            func = getattr(freenect2, func_name)
            print(f"  ✓ {func_name} - accessible")
        except AttributeError:
            print(f"  ✗ {func_name} - not found")
            
except Exception as e:
    print(f"✗ Error loading libfreenect2: {e}")
