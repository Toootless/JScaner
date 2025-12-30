# Kinect v1 with libusbK - Complete Troubleshooting

Your Kinect v1 is detected with **libusbK drivers** but we're having trouble accessing it via Python. This guide covers all options.

## Status Report

```
✓ Kinect v1 detected in Device Manager (libusbK driver)
✓ PyUSB installed (USB library)
✗ PyUSB cannot enumerate Kinect (device access issue)
✗ libfreenect not compiled yet
```

## Solution Options (Try in Order)

### Option 1: Switch to Standard Windows Drivers (EASIEST)

Kinect v1 also works with standard Windows camera drivers. This avoids all the compilation issues:

1. **Install Kinect for Windows SDK v1.8**
   - Download from: https://www.microsoft.com/en-us/download/details.aspx?id=40278
   - This provides standard Windows drivers

2. **Remove libusbK driver**:
   - Device Manager → Right-click Kinect → Uninstall device
   - Check "Delete driver software"

3. **Let Windows reinstall it as a camera**
   - Windows Update will find the standard camera driver
   - Or manually select "Kinect for Windows" driver

4. **Restart JScaner**
   - Should now work with OpenCV backend (easiest path!)

**Pros**: No compilation, simple setup  
**Cons**: Requires Microsoft SDK installation

---

### Option 2: Build libfreenect with Visual Studio (ADVANCED)

If you have Visual Studio C++ tools:

1. **Install dependencies**:
   ```bash
   pip install cmake ninja
   ```

2. **Clone libfreenect**:
   ```bash
   git clone https://github.com/OpenKinect/libfreenect.git C:\libfreenect
   cd C:\libfreenect
   mkdir build
   cd build
   ```

3. **Build with CMake**:
   ```bash
   cmake -G "Visual Studio 17 2022" -A x64 ..
   cmake --build . --config Release
   ```

4. **Copy DLL to JScaner**:
   ```bash
   Copy-Item "C:\libfreenect\build\lib\Release\freenect.dll" `
     -Destination "C:\Users\johnj\OneDrive\Documents\____3dScanner\3dscaning\freenect.dll"
   ```

5. **Restart JScaner**

**Pros**: Full control, works with libusbK  
**Cons**: Requires Visual Studio, complex build

---

### Option 3: Configure PyUSB for libusbK (EXPERT)

If you want to stick with libusbK + PyUSB:

1. **Install WinUSB toolkit**:
   - Download from: https://github.com/pbatard/libwdi/releases
   - Extract and add to PATH

2. **Reinstall PyUSB for WinUSB**:
   ```bash
   pip uninstall pyusb -y
   pip install pyusb --no-cache-dir --force-reinstall
   ```

3. **Configure libusbK access**:
   - Use Zadig tool (included in libwdi)
   - Configure Kinect v1 to use WinUSB instead of libusbK

4. **Restart JScaner**

**Pros**: Works with libusbK in place  
**Cons**: Complex driver configuration

---

## My Recommendation

**Try Option 1 first** (Switch to Windows drivers):

```powershell
# 1. Download Kinect SDK v1.8
# https://www.microsoft.com/en-us/download/details.aspx?id=40278

# 2. Install it (just run the installer)

# 3. Then restart JScaner - should work immediately!
```

This is the simplest and most reliable approach. libusbK is for advanced use cases (robotics, game engines with custom drivers).

---

## Alternative: Use Webcam Instead

If Kinect setup is too complex, JScaner works great with a standard USB webcam:

1. Connect your Logitech C920 or other USB camera
2. Select it in the Camera Settings
3. Ready to scan!

All 3D reconstruction features work the same with any USB camera.

---

## Need Help?

Check which approach makes sense for your setup:
- **Have VS 2022?** → Option 2 (build libfreenect)
- **Want simplest solution?** → Option 1 (Microsoft SDK)
- **Expert with drivers?** → Option 3 (WinUSB)
- **Just want to scan?** → Use your webcam!

Let me know which option you want to try!
