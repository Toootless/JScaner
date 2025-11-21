"""
Example script showing how to use the 3D scanner programmatically.
"""

import sys
import os
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.image_capture import ImageCapture
from core.grid_calibration import GridDetector
from core.reconstruction import StereoReconstructor
from core.stl_export import STLExporter

def main():
    """Example usage of the JScaner components."""
    print("JScaner - Example Usage")
    print("=" * 40)
    
    # Initialize components
    print("Initializing components...")
    image_capture = ImageCapture()
    grid_detector = GridDetector(grid_size_mm=(10.0, 10.0))
    reconstructor = StereoReconstructor()
    stl_exporter = STLExporter()
    
    print("Components initialized!")
    print("\nTo use this system:")
    print("1. Set up a calibration grid with 10mm squares")
    print("2. Take multiple photos of objects against the grid")
    print("3. Run camera calibration")
    print("4. Perform 3D reconstruction")
    print("5. Export as STL file")
    
    print(f"\nExample grid pattern: 9x6 checkerboard")
    print(f"Grid square size: 10.0mm x 10.0mm")
    print(f"Recommended images: 5-10 from different angles")
    
    # Test camera if available
    if image_capture.initialize_camera():
        print("\n✓ Camera detected and ready")
        camera_info = image_capture.get_camera_info()
        print(f"  Resolution: {camera_info['width']}x{camera_info['height']}")
        print(f"  FPS: {camera_info['fps']}")
        if camera_info.get('is_c920_compatible'):
            print("  ✓ Logitech C920 compatible camera detected")
            print("  ✓ Optimizing settings for 3D scanning...")
            image_capture.optimize_for_3d_scanning()
        image_capture.release()
    else:
        print("\n✗ No camera detected")
    
    print("\nRun 'python main.py' to start the GUI application.")

if __name__ == "__main__":
    main()