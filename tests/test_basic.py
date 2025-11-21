"""
Simple test script to verify basic functionality.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from core.image_capture import ImageCapture
        print("✓ ImageCapture imported")
    except ImportError as e:
        print(f"✗ ImageCapture import failed: {e}")
    
    try:
        from core.grid_calibration import GridDetector
        print("✓ GridDetector imported")
    except ImportError as e:
        print(f"✗ GridDetector import failed: {e}")
    
    try:
        from core.reconstruction import StereoReconstructor
        print("✓ StereoReconstructor imported")
    except ImportError as e:
        print(f"✗ StereoReconstructor import failed: {e}")
    
    try:
        from core.stl_export import STLExporter
        print("✓ STLExporter imported")
    except ImportError as e:
        print(f"✗ STLExporter import failed: {e}")

def test_opencv():
    """Test OpenCV functionality."""
    print("\nTesting OpenCV...")
    
    try:
        import cv2
        print(f"✓ OpenCV version: {cv2.__version__}")
        
        # Test camera detection
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✓ Camera detected")
            cap.release()
        else:
            print("✗ No camera detected")
    except ImportError:
        print("✗ OpenCV not available")

if __name__ == "__main__":
    test_imports()
    test_opencv()
    print("\nBasic tests completed!")