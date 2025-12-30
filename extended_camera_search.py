#!/usr/bin/env python3
"""
Extended camera search - tries up to camera index 20
Some systems assign Kinect to higher indices
"""

import cv2

print("Extended Camera Index Search (0-20)")
print("=" * 70)

found = []

for i in range(21):
    # Try with DirectShow first (most reliable on Windows)
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret and frame is not None:
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            print(f"✓ Camera {i:2d}: {w}x{h} @ {fps}fps (DirectShow)")
            found.append(i)
        cap.release()
    
    # Also try default backend
    if i not in found:
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                backend = int(cap.get(cv2.CAP_PROP_BACKEND))
                print(f"✓ Camera {i:2d}: {w}x{h} (backend {backend})")
                found.append(i)
            cap.release()

print("\n" + "=" * 70)
print(f"Found {len(found)} camera(s) at indices: {found}")

if len(found) > 1:
    print(f"\n✓ KINECT FOUND! Try camera index {found[1]} in your scanner")
elif len(found) == 1:
    print("\n✗ Only laptop webcam found")
    print("\nThe 'Kinect for Windows Camera' device in Device Manager")
    print("is not accessible via standard OpenCV methods.")
    print("\nThis Kinect requires the Kinect SDK API, not webcam API.")
else:
    print("\n✗ No cameras found at all!")

print("=" * 70)
