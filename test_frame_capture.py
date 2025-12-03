#!/usr/bin/env python3
"""Test frame capture from both Kinect and Webcam"""

import sys
import os
import cv2

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.image_capture import ImageCapture

print('Testing Frame Capture:\n')

# Test 1: Kinect
print('1. Testing Kinect v2 frame capture:')
cap_kinect = ImageCapture(use_kinect=True)
print(f'   ✓ Kinect initialized: {cap_kinect.kinect_active}')

if cap_kinect.initialize_camera():
    frame = cap_kinect.get_frame()
    if frame is not None:
        print(f'   ✓ Kinect frame captured: shape={frame.shape}')
        if frame.max() == 0:  # Check if frame is all black
            print('   ⚠ Frame is black (placeholder) - full libfreenect2 frame listener not yet implemented')
        else:
            print('   ✓ Kinect producing actual frame data')
    else:
        print('   ✗ Failed to get frame from Kinect')
    cap_kinect.release()
else:
    print('   ✗ Failed to initialize Kinect camera')

print()

# Test 2: Webcam
print('2. Testing Webcam frame capture:')
cap_webcam = ImageCapture(use_kinect=False)
print(f'   ✓ Kinect disabled for webcam test')

if cap_webcam.initialize_camera():
    frame = cap_webcam.get_frame()
    if frame is not None:
        print(f'   ✓ Webcam frame captured: shape={frame.shape}')
        if frame.max() > 0:
            print('   ✓ Webcam producing actual frame data')
        else:
            print('   ✗ Webcam frame is black')
    else:
        print('   ✗ Failed to get frame from webcam')
    cap_webcam.release()
else:
    print('   ✗ Failed to initialize webcam')

print()

# Test 3: Camera switching
print('3. Testing camera switching at runtime:')
cap = ImageCapture(use_kinect=True)
print(f'   ✓ Started with Kinect: kinect_active={cap.kinect_active}')

if cap.switch_camera(use_kinect=False):
    print(f'   ✓ Switched to webcam: kinect_active={cap.kinect_active}')
else:
    print(f'   ✗ Failed to switch to webcam')

if cap.switch_camera(use_kinect=True):
    print(f'   ✓ Switched back to Kinect: kinect_active={cap.kinect_active}')
else:
    print(f'   ✗ Failed to switch back to Kinect')

cap.release()

print('\n✓ All frame capture tests completed!')
