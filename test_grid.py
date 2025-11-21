#!/usr/bin/env python3
"""
Grid Detection Test Script

Test script to debug grid detection on 3D printer bed patterns.
"""

import cv2
import numpy as np
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.grid_calibration import GridDetector

def test_grid_detection():
    """Test grid detection with manual image input."""
    
    # Create grid detector
    detector = GridDetector(grid_size_mm=(10.0, 10.0))
    
    print("Grid Detection Test")
    print("==================")
    print("Instructions:")
    print("1. Place an image file (jpg, png) in the project directory")
    print("2. Enter the filename when prompted")
    print("3. The script will try to detect grid patterns")
    print()
    
    # Get image filename
    filename = input("Enter image filename (or press Enter for camera test): ").strip()
    
    if not filename:
        # Use camera
        print("Opening camera...")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        print("Press SPACE to capture image, ESC to exit")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            cv2.imshow('Camera - Press SPACE to test detection', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == 32:  # SPACE
                test_image = frame.copy()
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if 'test_image' not in locals():
            print("No image captured")
            return
            
    else:
        # Load image file
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' not found")
            return
        
        test_image = cv2.imread(filename)
        if test_image is None:
            print(f"Error: Could not load image '{filename}'")
            return
    
    print(f"\nImage loaded, size: {test_image.shape}")
    
    # Test different grid patterns
    test_patterns = [
        (5, 4), (6, 4), (7, 5), (8, 6), (9, 6), (10, 7), (11, 8),
        (4, 5), (4, 6), (5, 7), (6, 8), (6, 9), (7, 10), (8, 11)
    ]
    
    print("\nTesting grid detection...")
    print("=" * 50)
    
    # First, analyze what patterns might be present
    print("Analyzing possible patterns...")
    detected_patterns = detector.analyze_grid_patterns(test_image)
    
    if detected_patterns:
        print(f"Found {len(detected_patterns)} possible patterns:")
        for pattern in detected_patterns:
            print(f"  - {pattern[0]}x{pattern[1]} inner corners")
        test_patterns = detected_patterns + test_patterns
    
    # Test each pattern
    successful_detections = []
    
    for pattern in test_patterns:
        print(f"\nTesting pattern {pattern[0]}x{pattern[1]}...")
        corners, vis_image = detector.detect_and_visualize_grid(test_image, pattern, save_debug=True)
        
        if corners is not None:
            print(f"✓ SUCCESS: Detected {len(corners)} points with pattern {pattern}")
            successful_detections.append((pattern, corners, vis_image))
            
            # Show the result
            display_image = cv2.resize(vis_image, (800, 600))
            cv2.imshow(f'Grid Detection - {pattern[0]}x{pattern[1]}', display_image)
            cv2.waitKey(2000)  # Show for 2 seconds
            cv2.destroyAllWindows()
        else:
            print(f"✗ Failed to detect pattern {pattern}")
    
    print(f"\nSummary:")
    print(f"Tested {len(test_patterns)} patterns")
    print(f"Successful detections: {len(successful_detections)}")
    
    if successful_detections:
        print("\nSuccessful patterns:")
        for pattern, corners, _ in successful_detections:
            print(f"  - {pattern[0]}x{pattern[1]}: {len(corners)} points")
            
        # Test calibration with the best detection
        best_pattern, best_corners, best_vis = successful_detections[0]
        print(f"\nTesting calibration with pattern {best_pattern}...")
        
        try:
            # Create multiple copies of the same image for testing
            test_images = [test_image] * 5  # Simulate 5 images
            
            detector_cal = GridDetector(grid_size_mm=(10.0, 10.0))
            calibration = detector_cal.calibrate_camera(test_images, best_pattern)
            
            print("✓ Calibration successful!")
            print(f"  Reprojection error: {calibration['reprojection_error']:.3f}")
            print(f"  Successful detections: {calibration.get('successful_detections', 'N/A')}")
            
        except Exception as e:
            print(f"✗ Calibration failed: {e}")
    else:
        print("\nNo patterns detected. Try:")
        print("1. Ensure good lighting and contrast")
        print("2. Make sure the grid is flat and clearly visible")
        print("3. Try a different grid pattern or size")
        print("4. Check if the image contains a clear grid structure")

if __name__ == "__main__":
    test_grid_detection()