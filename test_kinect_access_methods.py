#!/usr/bin/env python3
"""
Test Kinect access via Windows Media Foundation
Tries all possible camera access methods
"""

import cv2
import sys

print("Testing Kinect Camera Access Methods")
print("=" * 60)

# Method 1: Try OpenNI/OpenNI2 backend specifically
print("\n[Method 1] OpenNI2 Backend")
print("-" * 60)
for i in range(3):
    try:
        cap = cv2.VideoCapture(i, cv2.CAP_OPENNI2)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✓ Camera {i} via OpenNI2: {frame.shape}")
            cap.release()
    except Exception as e:
        pass

# Method 2: DirectShow with device enumeration
print("\n[Method 2] DirectShow Backend")
print("-" * 60)
for i in range(5):
    try:
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                print(f"✓ Camera {i} via DirectShow: {w}x{h}")
            cap.release()
    except Exception as e:
        pass

# Method 3: Media Foundation
print("\n[Method 3] Media Foundation Backend")
print("-" * 60)
for i in range(5):
    try:
        cap = cv2.VideoCapture(i, cv2.CAP_MSMF)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                print(f"✓ Camera {i} via MSMF: {w}x{h}")
            cap.release()
    except Exception as e:
        pass

# Method 4: Try pykinect (if available)
print("\n[Method 4] PyKinect Library (Kinect SDK)")
print("-" * 60)
try:
    from pykinect import nui
    print("✓ pykinect module found!")
    try:
        nui.initialize()
        print("✓ Kinect initialized via pykinect!")
        nui.uninitialize()
    except Exception as e:
        print(f"✗ Could not initialize: {e}")
except ImportError:
    print("✗ pykinect not installed")
    print("  Install with: pip install pykinect")

# Method 5: Try pykinect2 (if available)
print("\n[Method 5] PyKinect2 Library (Kinect v2 SDK)")
print("-" * 60)
try:
    from pykinect2 import PyKinectV2
    from pykinect2.PyKinectV2 import *
    from pykinect2 import PyKinectRuntime
    print("✓ pykinect2 module found!")
    try:
        kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)
        if kinect:
            print("✓ Kinect initialized via pykinect2!")
            kinect.close()
    except Exception as e:
        print(f"✗ Could not initialize: {e}")
except ImportError:
    print("✗ pykinect2 not installed")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("\nIf no additional cameras found above, the Kinect")
print("likely requires pykinect library to access.")
print("\nNext step: Install pykinect")
print("  pip install pykinect")
print("\nNote: pykinect works with Kinect v1 (Xbox 360 / Kinect for Windows v1)")
print("=" * 60)
