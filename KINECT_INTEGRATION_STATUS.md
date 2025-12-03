# Kinect v2 Integration Status

## Current Status
- ✓ libfreenect2 DLL detected and loaded
- ✓ Kinect hardware detection working
- ⚠ Real-time frame capture: Using test pattern display (pending full implementation)
- ✓ GUI integration complete with camera selection
- ✓ Auto-start functionality working

## Why Real Frames Aren't Working Yet

### Issue 1: pykinect2 Compatibility
- **Installation**: ✓ Installed successfully  
- **Problem**: AssertionError on struct size with Python 3.11+ 64-bit
- **Root cause**: pykinect2 has hardcoded struct sizes that don't match Python 3.11
- **Status**: Known issue, package is outdated (v0.1.0 from ~2015)

### Issue 2: libfreenect2 C++ Library
- **DLL Status**: ✓ Loaded successfully from vcpkg
- **Problem**: No exported Python functions accessible
- **Root cause**: libfreenect2 requires complex ctypes wrapping or Python bindings
- **Details**: Frame listeners, depth processors need C++ callback patterns

### Issue 3: Missing Python Bindings
**No official libfreenect2 Python package exists because:**
1. libfreenect2 is C++-only library
2. Complex API with frame listeners (C++ patterns)
3. Small Python user base for Kinect v2
4. Maintenance burden on OpenKinect project

## Workaround: Test Pattern Display

JScaner now displays a colorful **test pattern** showing:
- "Kinect v2 Sensor"
- "Ready for Scanning"  
- Instructions to click "Capture Image"

This provides visual feedback that Kinect is detected and initialized.

## Alternative Solutions

### 1. Use OpenCV Kinect Support (Easiest)
OpenCV can access Kinect through UVC (USB Video Class):
```python
# Kinect v2 RGB stream as camera index 1
cap = cv2.VideoCapture(1)
ret, frame = cap.read()
```

### 2. Install Microsoft Kinect SDK
If you want real pykinect2 frames:
1. Download Microsoft Kinect for Windows SDK 2.0
2. Install full SDK (includes drivers)
3. Requires Windows 10/11 and .NET Framework
4. Workaround Python 3.11 issue with custom bindings

### 3. Compile Custom libfreenect2 Bindings
Using pybind11 or SWIG to wrap libfreenect2:
```bash
# Advanced option - requires C++ compiler and CMake
pip install pybind11
# Then compile custom wrapper
```

### 4. Use Azure Kinect SDK
Microsoft's newer sensor with better Python support:
```
pip install azure-kinect-sensor
```

## Recommended Next Steps

**Option A**: Accept test pattern for now (recommended for quick setup)
- Kinect detection ✓
- Camera switching ✓  
- 3D scanning workflow ready ✓
- Real frames: Coming soon

**Option B**: Install Microsoft Kinect SDK 2.0
- Enables pykinect2 (with Python 3.10 compatibility)
- Full Kinect driver support
- Real RGB + depth frame capture

**Option C**: Switch to OpenCV UVC access
- Try camera index 1: `cv2.VideoCapture(1)`
- May work with libfreenect2 drivers
- Simpler than full SDK

## Code Structure

- `src/core/kinect_capture.py` - Kinect device abstraction
- `src/core/image_capture.py` - Camera switching logic  
- `src/gui/main_window.py` - Camera selection UI
- `check_libfreenect_bindings.py` - Diagnostic tool

## Files to Update When Real Frames Available

1. `kinect_capture.py::_capture_kinect_frame()` - Add actual frame reading
2. `kinect_capture.py::get_rgb_frame()` - Remove test pattern fallback
3. `kinect_capture.py::get_depth_frame()` - Implement depth capture
4. `requirements.txt` - Add final Kinect package once stable

---

**Status**: Kinect integration complete at detection/UI level. Real frame capture pending Python bindings or libfreenect2 C API wrapper completion.
