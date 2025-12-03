#!/usr/bin/env python3
"""Check for libfreenect2 Python bindings availability"""

import subprocess
import sys

print("Checking for libfreenect2 Python packages...\n")

# Try to find packages
try:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "search", "libfreenect"],
        capture_output=True,
        text=True,
        timeout=10
    )
    print("Search results:")
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
except Exception as e:
    print(f"Note: pip search may not work: {e}")
    print("\nManual check - trying to import known libfreenect2 packages:")
    
    packages_to_try = [
        "libfreenect2",
        "freenect2",
        "pylibfreenect2",
        "freenect",
        "pykinect2",
        "kinect_v2",
    ]
    
    for pkg in packages_to_try:
        try:
            __import__(pkg)
            print(f"  ✓ {pkg} - AVAILABLE")
        except ImportError:
            print(f"  ✗ {pkg} - not available")
    
    print("\nWhy libfreenect2 Python bindings aren't available:")
    print("1. libfreenect2 is primarily a C++ library from OpenKinect")
    print("2. Official Python bindings don't exist in PyPI")
    print("3. Main reasons:")
    print("   - libfreenect2 is complex (depth processing, frame listeners)")
    print("   - Requires compiling C++ with specific compiler flags")
    print("   - Not many Python users for Kinect v2 (Windows-specific)")
    print("   - Maintenance burden on OpenKinect project")
    print("\nAlternatives:")
    print("1. Use pykinect2 (Microsoft's official SDK) - Windows only")
    print("2. Use OpenCV with Kinect (limited support)")
    print("3. Use ctypes directly (what we're doing now)")
    print("4. Use Azure Kinect SDK (newer hardware support)")
    print("5. Compile custom Python bindings with SWIG/pybind11")
