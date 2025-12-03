# Kinect v1 Integration Status

## Current Status: ✓ Kinect v1 (Xbox 360) Support Implemented

This document describes the Kinect v1 (Xbox 360 Kinect) integration in JScaner.

## Hardware Compatibility

- **Device**: Kinect v1 (Xbox 360 Kinect)
- **Connection**: USB 2.0 or USB 3.0 port
- **Supported Features**: RGB video capture
- **Unsupported Features**: Depth/IR sensor (requires Windows Kinect SDK)

## Implementation Details

### Camera Interface
- **Library**: OpenCV (cv2.VideoCapture)
- **Method**: Windows device enumeration
- **Resolution**: 640x480 (RGB)
- **Frame Rate**: Up to 30 FPS

### Installation Requirements

1. **Windows Kinect v1 Drivers**
   - Download from Microsoft Kinect for Windows v1 website
   - OR install drivers from Xbox 360 Kinect CD

2. **Python Dependencies** (Already installed in JScaner)
   - OpenCV (4.12.0.88)
   - NumPy (2.2.6)
   - cv2 for camera access

### How It Works

1. **Initialization**: 
   - App detects Kinect v1 via OpenCV device enumeration
   - Checks USB device at indices 0-3
   - Validates that frames are not pure black (indicates driver issue)

2. **Frame Capture**:
   - Uses `cv2.VideoCapture(device_id)` to access Kinect
   - Returns 640x480 BGR color frames
   - Gracefully falls back to status pattern if capture fails

3. **Camera Selection**:
   - Radio buttons in GUI allow switching between Kinect v1 and Webcam
   - Selection persists across app restart

## Usage in JScaner

### GUI Method
1. Launch JScaner: `python main.py`
2. Camera Settings panel (left sidebar)
3. Select **Kinect v1** radio button
4. Camera preview shows live feed

### Command Line
```python
from src.core.image_capture import ImageCapture

# Create capture with Kinect v1
cap = ImageCapture(use_kinect=True)

# Get frames
rgb_frame = cap.read_frame()  # 640x480 BGR image

# Switch cameras at runtime
cap.switch_camera(use_kinect=False)  # Switch to webcam
cap.switch_camera(use_kinect=True)   # Back to Kinect v1
```

## Troubleshooting

### Problem: Kinect Not Detected
1. Check USB connection (use USB 2.0 if possible)
2. Verify Windows Device Manager shows Kinect
3. Install official Kinect v1 drivers
4. Try different USB ports

### Problem: Black Screen
1. This usually means drivers aren't properly installed
2. Run Windows Update to get latest USB drivers
3. Reinstall Kinect drivers

### Problem: Low Frame Rate
1. Check USB port is powered (may need powered hub)
2. Try different USB port
3. Close other USB-intensive applications

## Testing

Run diagnostic test:
```bash
python test_kinect_v1.py
```

This will:
- Detect Kinect v1 availability
- Test initialization
- Capture 5 sample frames
- List all available cameras

## Technical Notes

### Why Not libfreenect/freenect?
- `freenect` package requires libfreenect C library compilation
- On Windows, this requires Visual Studio build tools + libfreenect source
- Complex setup with limited Python 3.11+ support
- OpenCV approach is simpler and more portable

### Why Not PyKinect2?
- PyKinect2 is for Kinect v2 (Xbox One), not Kinect v1
- Python 3.11+ incompatible (struct size assertion errors)
- Not applicable for Xbox 360 Kinect

### Depth/IR Support
- Kinect v1 has depth and IR sensors
- Full support requires Windows Kinect SDK (C# or C++)
- Current implementation focuses on RGB for 3D photogrammetry
- Depth would require additional Windows SDK installation

## Future Enhancements

1. **Windows Kinect SDK Integration**
   - Would add depth and IR sensor support
   - Requires Python bindings for SDK
   - More complex setup

2. **libfreenect Native Support**
   - If needed, could add with proper build environment setup
   - Would provide cross-platform support (Linux, macOS)

3. **Depth-Assisted Photogrammetry**
   - Use Kinect depth to improve reconstruction
   - Combine RGB + depth for better point cloud
   - More accurate mesh generation

## References

- Kinect v1 (Xbox 360): https://en.wikipedia.org/wiki/Kinect
- OpenCV VideoCapture: https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html
- Windows Kinect SDK: https://developer.microsoft.com/en-us/kinect

## Support

For issues with Kinect v1 integration:
1. Check Device Manager for Kinect device
2. Run `test_kinect_v1.py` diagnostic
3. Review troubleshooting section above
4. Check GitHub issues in 3dscaning repository
