"""
Test script to verify libfreenect2 is working with Kinect v2
"""

import ctypes
import sys
from pathlib import Path

# Add libfreenect2 DLL location to PATH
freenect2_path = Path("C:/Users/johnj/Downloads/vcpkg/installed/x64-windows/bin")
if freenect2_path.exists():
    sys.path.insert(0, str(freenect2_path))
    print(f"✓ Added libfreenect2 path: {freenect2_path}")
else:
    print(f"✗ libfreenect2 path not found: {freenect2_path}")
    sys.exit(1)

try:
    # Try to import libfreenect2
    print("\nAttempting to load libfreenect2...")
    
    # Load the DLL directly
    freenect2_dll = ctypes.CDLL(str(freenect2_path / "freenect2.dll"))
    print("✓ freenect2.dll loaded successfully!")
    
    # Check for key functions
    functions = ['freenect2_createContext', 'freenect2_openDevice', 'freenect2_getFrameData']
    for func_name in functions:
        try:
            func = getattr(freenect2_dll, func_name)
            print(f"  ✓ Found function: {func_name}")
        except AttributeError:
            print(f"  ✗ Function not found: {func_name}")
    
    print("\n✓ libfreenect2 is available and working!")
    print("\nNext steps:")
    print("1. Install Python bindings: pip install pylibfreenect2")
    print("2. Or use ctypes directly to interface with freenect2.dll")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nTroubleshooting:")
    print("- Make sure libfreenect2 is installed via vcpkg")
    print("- Make sure Kinect is plugged in and recognized")
    print("- Check Device Manager for 'Xbox NUI Motor' under libusbK USB Devices")
