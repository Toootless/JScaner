#!/usr/bin/env python3
"""
Performance Benchmark Script

Compare CPU vs GPU performance for image processing operations.
"""

import cv2
import numpy as np
import time
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.gpu_acceleration import get_gpu_accelerator

def benchmark_operations():
    """Benchmark various image processing operations."""
    
    gpu_accel = get_gpu_accelerator()
    
    print("Performance Benchmark")
    print("=" * 50)
    gpu_accel.print_device_info()
    print()
    
    # Create test images of different sizes
    test_sizes = [(640, 480), (1920, 1080), (3840, 2160)]
    
    for width, height in test_sizes:
        print(f"\nTesting with {width}x{height} image:")
        print("-" * 40)
        
        # Generate test image
        test_image = np.random.randint(0, 256, (height, width), dtype=np.uint8)
        
        # Gaussian Blur Benchmark
        print("Gaussian Blur (5x5, sigma=1.0):")
        
        # CPU version
        start_time = time.time()
        for _ in range(10):  # Run multiple times for average
            cpu_result = cv2.GaussianBlur(test_image, (5, 5), 1.0)
        cpu_time = (time.time() - start_time) / 10
        
        # GPU version
        start_time = time.time()
        for _ in range(10):
            gpu_result = gpu_accel.gaussian_blur_gpu(test_image, (5, 5), 1.0)
        gpu_time = (time.time() - start_time) / 10
        
        print(f"  CPU: {cpu_time*1000:.2f}ms")
        print(f"  GPU: {gpu_time*1000:.2f}ms")
        if cpu_time > 0:
            speedup = cpu_time / gpu_time if gpu_time > 0 else float('inf')
            print(f"  Speedup: {speedup:.2f}x")
        
        # Canny Edge Detection Benchmark
        print("Canny Edge Detection (50, 150):")
        
        # CPU version
        start_time = time.time()
        for _ in range(10):
            cpu_edges = cv2.Canny(test_image, 50, 150)
        cpu_time = (time.time() - start_time) / 10
        
        # GPU version
        start_time = time.time()
        for _ in range(10):
            gpu_edges = gpu_accel.canny_edge_gpu(test_image, 50, 150)
        gpu_time = (time.time() - start_time) / 10
        
        print(f"  CPU: {cpu_time*1000:.2f}ms")
        print(f"  GPU: {gpu_time*1000:.2f}ms")
        if cpu_time > 0:
            speedup = cpu_time / gpu_time if gpu_time > 0 else float('inf')
            print(f"  Speedup: {speedup:.2f}x")
        
        # CLAHE Contrast Enhancement
        print("CLAHE Contrast Enhancement:")
        
        # CPU version
        start_time = time.time()
        for _ in range(10):
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
            cpu_enhanced = clahe.apply(test_image)
        cpu_time = (time.time() - start_time) / 10
        
        # GPU version
        start_time = time.time()
        for _ in range(10):
            gpu_enhanced = gpu_accel.enhance_contrast_gpu(test_image, 3.0, (8, 8))
        gpu_time = (time.time() - start_time) / 10
        
        print(f"  CPU: {cpu_time*1000:.2f}ms")
        print(f"  GPU: {gpu_time*1000:.2f}ms")
        if cpu_time > 0:
            speedup = cpu_time / gpu_time if gpu_time > 0 else float('inf')
            print(f"  Speedup: {speedup:.2f}x")
        
        # Harris Corner Detection
        print("Harris Corner Detection:")
        
        # CPU version
        start_time = time.time()
        for _ in range(5):  # Fewer iterations as this is slower
            cpu_corners = cv2.cornerHarris(test_image, 2, 3, 0.04)
        cpu_time = (time.time() - start_time) / 5
        
        # GPU version
        start_time = time.time()
        for _ in range(5):
            gpu_corners = gpu_accel.harris_corners_gpu(test_image, 2, 3, 0.04)
        gpu_time = (time.time() - start_time) / 5
        
        print(f"  CPU: {cpu_time*1000:.2f}ms")
        print(f"  GPU: {gpu_time*1000:.2f}ms")
        if cpu_time > 0:
            speedup = cpu_time / gpu_time if gpu_time > 0 else float('inf')
            print(f"  Speedup: {speedup:.2f}x")

def benchmark_grid_detection():
    """Benchmark grid detection performance."""
    print(f"\nGrid Detection Benchmark")
    print("=" * 50)
    
    # Load the test image
    test_image_path = "WIN_20251114_14_58_32_Pro.jpg"
    
    if not os.path.exists(test_image_path):
        print(f"Test image '{test_image_path}' not found. Skipping grid detection benchmark.")
        return
    
    from core.grid_calibration import GridDetector
    
    test_image = cv2.imread(test_image_path)
    if test_image is None:
        print("Could not load test image")
        return
    
    detector = GridDetector(grid_size_mm=(10.0, 10.0))
    
    print("Testing grid detection with GPU acceleration...")
    
    # Test multiple pattern sizes
    test_patterns = [(9, 6), (10, 7), (15, 15)]
    
    for pattern in test_patterns:
        print(f"\nPattern {pattern[0]}x{pattern[1]}:")
        
        start_time = time.time()
        corners, vis_image = detector.detect_and_visualize_grid(test_image, pattern, save_debug=False)
        detection_time = time.time() - start_time
        
        if corners is not None:
            print(f"  ✓ Detected {len(corners)} points in {detection_time*1000:.2f}ms")
        else:
            print(f"  ✗ Detection failed in {detection_time*1000:.2f}ms")

if __name__ == "__main__":
    try:
        benchmark_operations()
        benchmark_grid_detection()
    except KeyboardInterrupt:
        print("\nBenchmark interrupted by user.")
    except Exception as e:
        print(f"Benchmark error: {e}")
        import traceback
        traceback.print_exc()