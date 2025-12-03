# Kinect v1 with libusbK - Setup Guide

Your Kinect v1 has been detected with **libusbK drivers**, which means it's using raw USB access instead of standard Windows camera drivers.

## Current Status

```
✓ Kinect v1 detected in Device Manager under libusbK
✗ libfreenect.dll not found - cannot access device yet
```

## Setup Steps

### Option 1: Build libfreenect with vcpkg (Recommended)

1. **Install vcpkg** (if not already installed):
   ```powershell
   git clone https://github.com/Microsoft/vcpkg.git C:\vcpkg
   cd C:\vcpkg
   .\bootstrap-vcpkg.bat
   ```

2. **Install libfreenect library**:
   ```powershell
   C:\vcpkg\vcpkg install libfreenect:x64-windows
   ```

3. **Copy libfreenect DLL to project**:
   ```powershell
   Copy-Item "C:\vcpkg\installed\x64-windows\bin\freenect.dll" `
     -Destination "c:\Users\johnj\OneDrive\Documents\VS_projects\3dscaning\freenect.dll"
   ```

4. **Restart JScaner**:
   ```bash
   python main.py
   ```

### Option 2: Use Pre-built Binaries

1. Download pre-compiled libfreenect binaries from:
   - https://github.com/OpenKinect/libfreenect/releases
   
2. Extract `freenect.dll` to the project root directory

3. Restart JScaner

### Option 3: Check if Kinect Works with OpenCV First

If you prefer to skip libfreenect setup, try:

1. Install standard Kinect v1 drivers from Microsoft
2. This will expose Kinect as a regular camera to Windows
3. OpenCV can then access it directly

## Verify Installation

After setting up libfreenect, restart JScaner and you should see:

```
✓ libfreenect loaded from C:\...
✓ Kinect v1 with libusbK initialized
✓ Kinect v1 activated - RGB enabled!
```

## What Each File Does

| File | Purpose |
|------|---------|
| `freenect.dll` | libfreenect runtime library (C++ wrapper) |
| `kinect_v1_libfreenect.py` | Python interface to libfreenect |
| `kinect_capture.py` | Camera abstraction layer (tries libfreenect, falls back to OpenCV) |

## Troubleshooting

### "libfreenect.dll not found"
- Check that freenect.dll is in the project root or expected path
- Verify you installed libfreenect via vcpkg

### "Cannot find a process with the name"
- This is just a PowerShell error when no process exists - ignore it
- JScaner should still launch

### Kinect still shows black screen
- Verify libusbK is controlling the device (check Device Manager)
- Try using standard Windows Kinect drivers as fallback
- Check USB power (may need powered hub)

## Next Steps

1. Install libfreenect using Option 1 above
2. Copy freenect.dll to project
3. Restart JScaner
4. Live Kinect feed should appear in preview

## References

- libfreenect Project: https://github.com/OpenKinect/libfreenect
- OpenKinect Wiki: https://openkinect.org/wiki/Main_Page
- libusbK Driver: https://sourceforge.net/projects/libusbk/

---

**Note**: Once libfreenect is set up with libusbK drivers, you'll have full access to Kinect v1's RGB and depth sensors for advanced 3D reconstruction features.
