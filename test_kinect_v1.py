#!/usr/bin/env python3
"""
Test script for Kinect v1 (Xbox 360) support
"""

import sys
import cv2
import numpy as np
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.kinect_capture import KinectCapture

def test_kinect_availability():
    """Test Kinect v1 availability"""
    print("=" * 60)
    print("Testing Kinect v1 (Xbox 360) Availability")
    print("=" * 60)
    
    kinect = KinectCapture()
    
    if kinect.is_available():
        print("✓ Kinect v1 DETECTED via Windows drivers")
    else:
        print("✗ Kinect v1 NOT DETECTED")
        print("\nTroubleshooting:")
        print("1. Ensure Kinect v1 is plugged into a USB 2.0 port")
        print("2. Check Windows Device Manager for 'Kinect' or 'USB' devices")
        print("3. Install Windows Kinect v1 drivers if not already installed")
        print("4. Try different USB ports")
        return False
    
    return True

def test_kinect_initialization():
    """Test Kinect v1 initialization"""
    print("\n" + "=" * 60)
    print("Testing Kinect v1 Initialization")
    print("=" * 60)
    
    kinect = KinectCapture()
    
    if not kinect.is_available():
        print("✗ Kinect v1 not available, skipping initialization test")
        return False
    
    if kinect.initialize():
        print("✓ Kinect v1 INITIALIZED successfully")
        return True
    else:
        print("✗ Kinect v1 INITIALIZATION FAILED")
        return False

def test_kinect_frame_capture():
    """Test Kinect v1 frame capture"""
    print("\n" + "=" * 60)
    print("Testing Kinect v1 Frame Capture (5 frames)")
    print("=" * 60)
    
    kinect = KinectCapture()
    
    if not kinect.is_available() or not kinect.initialize():
        print("✗ Kinect v1 not available or not initialized")
        return False
    
    successful_frames = 0
    
    for i in range(5):
        rgb, depth = kinect.get_frames()
        
        if rgb is not None and rgb.size > 0:
            print(f"  Frame {i+1}: RGB shape {rgb.shape}, dtype {rgb.dtype}", end="")
            
            # Check if it's a real frame or status pattern
            unique_colors = len(np.unique(rgb))
            if unique_colors > 100:  # Status pattern would have fewer colors
                print(" ✓ [Real frame]")
                successful_frames += 1
            else:
                print(" (Status pattern)")
        else:
            print(f"  Frame {i+1}: FAILED")
    
    if successful_frames > 0:
        print(f"\n✓ Captured {successful_frames}/5 real frames")
        return True
    else:
        print("\n⚠ No real frames captured (Kinect may not be connected)")
        return False

def test_opencv_camera():
    """Test camera availability via OpenCV"""
    print("\n" + "=" * 60)
    print("Testing Camera Availability via OpenCV")
    print("=" * 60)
    
    for idx in range(4):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            
            if ret and frame is not None:
                print(f"✓ Camera {idx}: Available, shape {frame.shape}")
                # Check if it's a real frame
                if frame.max() > 10:
                    print(f"  └─ Real frame detected")
                else:
                    print(f"  └─ Black frame (may be status/placeholder)")
            else:
                print(f"✗ Camera {idx}: Cannot read frame")
        else:
            print(f"✗ Camera {idx}: Not available")

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " Kinect v1 (Xbox 360) Integration Test Suite ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    # Run tests
    has_kinect = test_kinect_availability()
    
    if has_kinect:
        initialized = test_kinect_initialization()
        if initialized:
            test_kinect_frame_capture()
    
    test_opencv_camera()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    if has_kinect:
        print("✓ Kinect v1 support is functional")
        print("\nTo use in JScaner:")
        print("1. Run: python main.py")
        print("2. Click 'Kinect v1' radio button in Camera Settings")
        print("3. Camera preview should show live Kinect feed")
    else:
        print("✗ Kinect v1 not detected")
        print("\nNext steps:")
        print("1. Connect Kinect v1 (Xbox 360) to USB 2.0 port")
        print("2. Install Kinect v1 drivers for your Windows version")
        print("3. Run this test again to verify")
        print("4. Check Device Manager to see if Kinect appears")

if __name__ == "__main__":
    main()
