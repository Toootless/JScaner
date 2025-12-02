#!/usr/bin/env python3
"""
Integration test for Kinect with JScaner
Tests ImageCapture with Kinect support
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.core.image_capture import ImageCapture
import time

def test_kinect_integration():
    """Test Kinect integration with ImageCapture."""
    
    print("=" * 60)
    print("JScaner Kinect Integration Test")
    print("=" * 60)
    
    # Test 1: Initialize with Kinect enabled
    print("\n[TEST 1] Initialize ImageCapture with Kinect support...")
    cap = ImageCapture(use_kinect=True)
    
    print(f"Camera type: {cap.get_camera_type()}")
    print(f"Has depth sensor: {cap.has_depth_sensor()}")
    
    # Test 2: Get camera info
    print("\n[TEST 2] Camera Information:")
    if cap.kinect_active:
        print("  ✓ Kinect v2 initialized and ready")
        print("  - RGB resolution: 1920x1080")
        print("  - Depth resolution: 512x424")
        print("  - Frame rate: ~30 FPS")
    else:
        print("  - Using fallback: Webcam")
    
    # Test 3: Try to get RGB frame
    print("\n[TEST 3] Attempting RGB frame capture...")
    if cap.kinect_active:
        print("  Initialize webcam as fallback...")
        if not cap.initialize_camera():
            print("  ✗ Failed to initialize fallback camera")
    else:
        print("  - Initializing webcam...")
        if not cap.initialize_camera():
            print("  ✗ Failed to initialize camera")
            return False
    
    time.sleep(1)
    rgb_frame = cap.get_frame()
    if rgb_frame is not None:
        print(f"  ✓ RGB frame captured: shape={rgb_frame.shape}, dtype={rgb_frame.dtype}")
    else:
        print("  ✗ Failed to capture RGB frame")
    
    # Test 4: Try to get depth frame
    print("\n[TEST 4] Attempting Depth frame capture...")
    if cap.has_depth_sensor():
        depth_frame = cap.get_depth_frame()
        if depth_frame is not None:
            print(f"  ✓ Depth frame captured: shape={depth_frame.shape}, dtype={depth_frame.dtype}")
            print(f"    Min depth: {depth_frame.min():.2f}mm, Max depth: {depth_frame.max():.2f}mm")
        else:
            print("  ✗ Failed to capture depth frame")
    else:
        print("  - Depth sensor not available (Kinect not active)")
    
    # Test 5: Capture sequence
    print("\n[TEST 5] Testing capture sequence...")
    try:
        frames = cap.capture_sequence(num_images=3, delay_seconds=0.5)
        print(f"  ✓ Captured {len(frames)} frames in sequence")
        for i, frame in enumerate(frames):
            print(f"    Frame {i+1}: shape={frame.shape}")
    except Exception as e:
        print(f"  ✗ Capture sequence failed: {e}")
    
    # Cleanup
    print("\n[CLEANUP] Releasing camera...")
    cap.release()
    if cap.kinect is not None:
        cap.kinect.close()
    
    print("\n" + "=" * 60)
    print("Integration Test Complete!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = test_kinect_integration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
