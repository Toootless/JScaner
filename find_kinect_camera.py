#!/usr/bin/env python3
"""
Find Kinect Camera Index
Scans all camera indices and displays detailed info to help locate the Kinect
"""

import cv2
import numpy as np

def get_camera_backend_name(backend_id):
    """Convert backend ID to readable name."""
    backends = {
        0: "Auto",
        100: "V4L/V4L2",
        200: "IEEE1394",
        300: "DSHOW (DirectShow)",
        400: "PVAPI",
        500: "OpenNI",
        600: "OpenNI_ASUS",
        700: "Android",
        800: "XIAPI",
        900: "AVFOUNDATION",
        1000: "GIGANETIX",
        1100: "MSMF (Media Foundation)",
        1200: "WINRT",
        1300: "INTELPERC",
        1400: "OPENNI2",
        1500: "OPENNI2_ASUS",
        1600: "GPHOTO2",
        1700: "GSTREAMER",
        1800: "FFMPEG",
        1900: "IMAGES",
        2000: "ARAVIS",
        2100: "OPENCV_MJPEG",
        2200: "INTEL_MFX",
        2300: "XINE",
    }
    return backends.get(backend_id, f"Unknown ({backend_id})")

def test_camera(index, backend=None):
    """Test a specific camera index."""
    try:
        # Open camera with specific backend if provided
        if backend is not None:
            cap = cv2.VideoCapture(index, backend)
        else:
            cap = cv2.VideoCapture(index)
        
        if not cap.isOpened():
            return None
        
        # Get camera properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        backend_id = int(cap.get(cv2.CAP_PROP_BACKEND))
        backend_name = get_camera_backend_name(backend_id)
        
        # Try to grab a frame
        ret, frame = cap.read()
        frame_captured = ret and frame is not None
        
        # Get frame info if captured
        frame_info = ""
        if frame_captured:
            frame_info = f"Frame: {frame.shape}, dtype: {frame.dtype}"
            # Calculate average brightness to detect if it's actually working
            avg_brightness = np.mean(frame)
            frame_info += f", Avg brightness: {avg_brightness:.1f}"
        
        cap.release()
        
        return {
            'index': index,
            'width': width,
            'height': height,
            'fps': fps,
            'backend': backend_name,
            'backend_id': backend_id,
            'frame_captured': frame_captured,
            'frame_info': frame_info
        }
    except Exception as e:
        return None

def main():
    print("=" * 70)
    print("KINECT CAMERA FINDER")
    print("=" * 70)
    print()
    
    # Test camera indices 0-9 with default backend
    print("Scanning camera indices 0-9 (default backend)...")
    print("-" * 70)
    
    found_cameras = []
    
    for i in range(10):
        result = test_camera(i)
        if result:
            found_cameras.append(result)
            print(f"\n✓ Camera {i} FOUND:")
            print(f"  Resolution: {result['width']}x{result['height']}")
            print(f"  FPS: {result['fps']}")
            print(f"  Backend: {result['backend']}")
            print(f"  Frame captured: {'YES' if result['frame_captured'] else 'NO'}")
            if result['frame_info']:
                print(f"  {result['frame_info']}")
        else:
            print(f"✗ Camera {i}: Not available", end='\r')
    
    print("\n")
    print("=" * 70)
    
    # Try specific backends for found cameras
    if found_cameras:
        print("\nTrying specific backends for detected cameras...")
        print("-" * 70)
        
        # DirectShow is most common for Windows
        backends_to_try = [
            (cv2.CAP_DSHOW, "DirectShow"),
            (cv2.CAP_MSMF, "Media Foundation"),
        ]
        
        for cam in found_cameras[:2]:  # Test first 2 cameras
            print(f"\nCamera {cam['index']}:")
            for backend_id, backend_name in backends_to_try:
                result = test_camera(cam['index'], backend_id)
                if result and result['frame_captured']:
                    print(f"  ✓ {backend_name}: {result['width']}x{result['height']} @ {result['fps']}fps")
                else:
                    print(f"  ✗ {backend_name}: Failed")
    
    print("\n" + "=" * 70)
    print("\nSUMMARY:")
    print("-" * 70)
    
    if not found_cameras:
        print("❌ No cameras detected!")
        print("\nTroubleshooting:")
        print("1. Check if Kinect is plugged in and powered")
        print("2. Check Device Manager for camera devices")
        print("3. Try running as Administrator")
    else:
        print(f"Found {len(found_cameras)} camera(s):\n")
        for cam in found_cameras:
            is_likely_kinect = (
                cam['width'] == 640 and cam['height'] == 480 or
                cam['width'] == 1920 and cam['height'] == 1080 or
                'Media Foundation' in cam['backend'] or
                'DirectShow' in cam['backend']
            )
            
            marker = "🎯 LIKELY KINECT" if is_likely_kinect and cam['index'] > 0 else ""
            marker = "💻 Likely laptop webcam" if cam['index'] == 0 else marker
            
            print(f"  Camera {cam['index']}: {cam['width']}x{cam['height']} @ {cam['fps']}fps")
            print(f"            Backend: {cam['backend']} {marker}")
        
        print("\n" + "=" * 70)
        print("\nRECOMMENDATION:")
        print("-" * 70)
        
        if len(found_cameras) > 1:
            print(f"✓ Try using camera index {found_cameras[1]['index']} for Kinect")
            print(f"\nUpdate kinect_scanner_gui.py or kinect_scanner.py:")
            print(f"  Change: camera_id = 0")
            print(f"  To:     camera_id = {found_cameras[1]['index']}")
        else:
            print("Only one camera found (likely your laptop webcam)")
            print("\nPossible issues:")
            print("1. Kinect drivers not installed properly")
            print("2. Kinect not recognized as a camera device")
            print("3. Need to install 'Kinect for Windows SDK v1.8'")
            print("\nSee: KINECT_V1_LIBUSBK_TROUBLESHOOTING.md")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
