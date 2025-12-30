# Kinect v1 Integration - Feature Branch

## Branch Name
`feature/kinect-v1-dotnet-integration`

## Summary
Complete Kinect v1 camera integration using Python 3.9 and .NET SDK via pythonnet. The scanner now supports both standard webcams and Kinect v1 hardware with full metadata capture.

## Changes Made

### New Files Created
1. **src/core/kinect_v1_dotnet.py**
   - .NET SDK wrapper for Kinect v1 using pythonnet
   - OpenCV-compatible interface (read(), isOpened(), release(), get())
   - Direct Microsoft.Kinect.dll assembly access
   - Returns BGR frames compatible with existing pipeline

2. **find_kinect_camera.py**
   - Diagnostic tool to detect all available cameras
   - Tests multiple backends (DirectShow, Media Foundation, OpenNI2)
   - Identifies which camera index is Kinect vs webcam

3. **extended_camera_search.py**
   - Searches camera indices 0-20
   - Helps locate cameras assigned to higher indices

4. **test_kinect_access_methods.py**
   - Tests multiple Kinect access methods
   - Checks for pykinect, pykinect2, SDK availability

5. **check_kinect_status.ps1**
   - PowerShell script to check Kinect device status
   - Displays working/broken devices in Device Manager

6. **fix_kinect_drivers.ps1**
   - Automated driver repair tool (requires admin)
   - Resets and updates Kinect device drivers

7. **KINECT_NOT_DETECTED.md**
   - Troubleshooting guide for Kinect detection issues
   - Step-by-step fixes and verification checklist

8. **kinect_test_frame.jpg**
   - Test image captured from Kinect during verification

### Modified Files

1. **kinect_scanner_gui.py**
   - Updated `CameraDetector.get_available_cameras()` to detect Kinect v1
   - Modified `_connect_camera()` to support both OpenCV and Kinect devices
   - Fixed `_change_camera()` to handle string camera IDs (e.g., "kinect_v1")
   - Fixed `_refresh_cameras()` to rebuild dropdown menu dynamically
   - Added metadata JSON export to `_capture_single()`
   - Added metadata JSON export to `_batch_capture_worker()`
   - Metadata includes: filename, timestamp, sequence, camera info, resolution

2. **run_kinect_scanner_gui.bat**
   - Updated to use Python 3.9 instead of Python 3.11
   - Added pythonnet dependency check
   - Removed ellipsis characters causing syntax errors
   - Points to: `C:\Users\johnj\AppData\Local\Programs\Python\Python39\python.exe`

3. **run_kinect_scanner_gui.ps1**
   - Updated to use Python 3.9
   - Added pythonnet to dependency checks
   - Enhanced error messages for Kinect-specific issues

4. **Project path updates** (multiple files)
   - Updated all hardcoded paths from `VS_projects` to `____3dScanner`
   - Files: Untitled-1.md, KINECT_*.md, DEPLOYMENT_*.md, docs/*.md

## Technical Details

### Dependencies Added
- **pythonnet** (3.0.5+) - Python .NET interop
- **Python 3.9.5** - Required for pythonnet compatibility

### Kinect SDK Requirements
- Kinect for Windows SDK v1.8
- Microsoft.Kinect.dll assembly
- Location: `C:\Program Files\Microsoft SDKs\Kinect\v1.8\Assemblies`

### How It Works
1. pythonnet loads Microsoft.Kinect.dll assembly
2. Wrapper creates KinectV1Camera class with OpenCV-compatible interface
3. GUI auto-detects Kinect and adds to camera dropdown as "kinect_v1"
4. When selected, initializes .NET SDK and streams 640x480 @ 30fps BGR frames
5. Captures save both JPG image and JSON metadata file

### Metadata Format
```json
{
  "filename": "scan_20251230_142608_001.jpg",
  "timestamp": "20251230_142608",
  "sequence": 1,
  "camera": "Kinect v1 (640x480 @ 30fps via .NET SDK)",
  "resolution": {
    "width": 640,
    "height": 480
  },
  "format": "BGR"
}
```

## Testing Performed
- ✓ Kinect v1 detection and initialization
- ✓ Live preview at 30fps
- ✓ Single image capture with metadata
- ✓ Batch capture with metadata
- ✓ Camera switching (webcam ↔ Kinect)
- ✓ Refresh cameras functionality
- ✓ Test frame saved successfully

## Git Commands to Execute

```bash
# Add all changes
git add .

# Commit changes
git commit -m "feat: Add Kinect v1 integration via .NET SDK

- Implement pythonnet wrapper for Microsoft Kinect SDK v1.8
- Add auto-detection of Kinect v1 in camera dropdown
- Support Python 3.9 for .NET interop compatibility
- Add metadata JSON export for all captures
- Fix camera switching and refresh functionality
- Update launcher scripts for Python 3.9
- Add comprehensive troubleshooting tools and documentation

Closes: Kinect v1 support request"

# Create and checkout new branch
git checkout -b feature/kinect-v1-dotnet-integration

# Push to remote (if configured)
git push -u origin feature/kinect-v1-dotnet-integration
```

## Installation Instructions for New Users

1. Install Python 3.9
2. Install dependencies: `pip install pythonnet opencv-python numpy Pillow`
3. Install Kinect for Windows SDK v1.8
4. Plug in and power Kinect v1
5. Run: `.\run_kinect_scanner_gui.bat`
6. Select "Kinect v1" from camera dropdown

## Known Issues
- Requires Python 3.9 (pythonnet incompatible with 3.11+)
- Kinect must be powered externally via AC adapter
- Only one application can access Kinect at a time
- OpenCV warnings during camera enumeration (harmless)

## Future Enhancements
- Support Kinect v2 (requires different SDK)
- Add depth stream capture
- Implement IR camera access
- Add skeleton tracking metadata
