#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.kinect_capture import KinectCapture

print('Testing Kinect initialization...')
kinect = KinectCapture()
print(f'Kinect available: {kinect.available}')
print(f'Kinect device: {kinect.dev}')

if kinect.is_available():
    print('Attempting to initialize...')
    result = kinect.initialize()
    print(f'Initialize result: {result}')
    
    if result:
        print('Getting RGB frame...')
        frame = kinect.get_rgb_frame()
        if frame is not None:
            print(f'Frame shape: {frame.shape}')
            print(f'Frame max value: {frame.max()}')
        else:
            print('Frame is None')
else:
    print('Kinect not available')
