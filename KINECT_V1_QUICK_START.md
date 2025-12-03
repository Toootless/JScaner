# Kinect v1 Setup - Quick Start

Your Kinect v1 is detected with **libusbK drivers**. To get it working with JScaner:

## Installation Steps (5 minutes)

### Step 1: Install vcpkg (if needed)
```powershell
git clone https://github.com/Microsoft/vcpkg.git C:\vcpkg
cd C:\vcpkg
.\bootstrap-vcpkg.bat
```

### Step 2: Build libfreenect
```powershell
C:\vcpkg\vcpkg install libfreenect:x64-windows
```

### Step 3: Copy freenect.dll to JScaner
```powershell
Copy-Item "C:\vcpkg\installed\x64-windows\bin\freenect.dll" `
  -Destination "C:\Users\johnj\OneDrive\Documents\VS_projects\3dscaning\freenect.dll"
```

### Step 4: Restart JScaner
```bash
python main.py
```

## Expected Result

When working correctly, you should see in the terminal:
```
✓ libfreenect loaded from ...
✓ Kinect v1 with libusbK initialized (libfreenect context created)
✓ Kinect v1 activated - RGB enabled!
```

And the camera preview should show live Kinect v1 feed (not the setup instructions).

## Status

| Item | Status |
|------|--------|
| Kinect Detection | ✓ Detected |
| Driver Type | libusbK (raw USB) |
| libfreenect | ✗ Not installed (next step) |
| Camera Feed | ⏳ Waiting for libfreenect |

---

**Next**: Follow the installation steps above, then restart JScaner!

For detailed information, see: `docs/KINECT_V1_LIBUSBK_SETUP.md`
