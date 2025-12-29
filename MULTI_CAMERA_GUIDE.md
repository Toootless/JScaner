# Multi-Camera Support - Kinect Scanner GUI Update

## What Changed

The Kinect Scanner GUI now includes **automatic camera detection and selection** with:

- 📷 **Auto-detect** - Scans system for all available cameras
- 🔄 **Switch cameras** - Dropdown menu to select any camera
- 📊 **Camera info** - Displays resolution, FPS, and backend type
- 🔌 **Refresh button** - Rescan for newly connected cameras
- 📝 **Manifest tracking** - Logs which camera was used

## Camera Detection

### How It Works

When you launch the GUI:

1. **Automatic Scan**: Application scans cameras 0-9
2. **Detection**: For each camera found, it reads:
   - Resolution (width × height)
   - Frame rate (FPS)
   - Backend type (DirectShow, V4L, etc.)
3. **Display**: Shows all found cameras in dropdown menu

## Using Multi-Camera Feature

### Starting with Specific Camera

#### From Command Line
```bash
python kinect_scanner_gui.py  # Defaults to camera 0
```

#### From Batch File
Edit `run_kinect_scanner_gui.bat`:
```batch
REM Change this line from:
python kinect_scanner_gui.py

REM To specify camera (e.g., camera 1):
python kinect_scanner_gui.py --camera 1
```

### Switching Cameras in GUI

1. **Open dropdown** - "📷 Camera Selection" at top
2. **See all cameras** - Shows camera ID and details
3. **Click camera** - Instantly switches to that camera
4. **Preview updates** - Live feed switches immediately

### Camera Selection Interface

```
┌─────────────────────────────────────────────────────────┐
│ 📷 Camera Selection:  [Dropdown ▼]  Current: Camera 0   │
│                                              🔄 Refresh  │
└─────────────────────────────────────────────────────────┘
```

### Example Camera List

When you click the dropdown, you might see:

```
Camera 0: Default Webcam - 640x480 @ 30fps
Camera 1: Kinect v1 (DirectShow) - 640x480 @ 30fps
Camera 3: USB HD Webcam (USB) - 1280x720 @ 30fps
```

## Identifying Your Kinect v1

Look for cameras with these characteristics:

| Type | Name Pattern | Resolution | Backend |
|------|--------------|-----------|---------|
| **Kinect v1** | Often "Camera X" | 640×480 | DirectShow |
| Webcam | "Webcam" or "HD" | Varies | DirectShow |
| USB Camera | USB Camera | Varies | USB/V4L |

**Tip**: Kinect v1 typically shows as one of the higher-numbered cameras (1, 2, or 3).

## Troubleshooting Multi-Camera

### Camera Not Detected

**Problem**: Your camera doesn't appear in the list

**Solution**:
1. Check USB connection is secure
2. Click **"🔄 Refresh"** button to rescan
3. Wait 3-5 seconds for detection
4. If still missing, try:
   - Different USB port
   - Restarting application
   - Checking Device Manager for unknown devices

### Wrong Camera Selected

**Problem**: Getting webcam instead of Kinect

**Solution**:
1. Try each camera in dropdown one at a time
2. Watch the preview to see which is Kinect
3. Kinect v1 usually shows **640×480** resolution
4. Kinect has no fisheye or wide-angle distortion
5. Switch to that camera number

### Camera Switches But Preview Freezes

**Problem**: Selecting new camera causes interface to freeze

**Solution**:
1. Wait 3-5 seconds (normal camera switching time)
2. If frozen, close and restart application
3. Check that only one application is using cameras
4. Ensure enough USB bandwidth available

### "No Cameras Detected" Message

**Problem**: Application finds zero cameras

**Solution**:
1. Connect camera to USB port
2. Wait 5 seconds for Windows to detect
3. Install camera drivers if needed:
   - Kinect v1: Xbox Kinect driver
   - Generic webcam: Windows Update usually auto-installs
4. Try different USB port
5. Click "🔄 Refresh" button

## Advanced: Specifying Camera at Launch

### Via Python

```python
python kinect_scanner_gui.py --camera 1
```

### Via Batch File

```batch
@echo off
python kinect_scanner_gui.py --camera 1
pause
```

### Via PowerShell

```powershell
python kinect_scanner_gui.py -camera 1
```

## Camera Information in Manifest

When you export images, the manifest.json now includes:

```json
{
  "export_time": "2025-12-29T14:30:22.123456",
  "total_images": 12,
  "output_directory": "...",
  "camera_id": 1,
  "camera_name": "Camera 1 (DirectShow) - 640x480 @ 30fps",
  "images": [...]
}
```

This helps track which camera was used for each scan session.

## Multi-Camera Workflow

### Scenario: Multiple Cameras on One PC

```
System has:
- Camera 0: Built-in webcam (not for scanning)
- Camera 1: Kinect v1 (for scanning)
- Camera 2: USB HD camera (backup)

Solution:
1. Launch GUI
2. Click dropdown, select Camera 1
3. See live Kinect feed
4. Capture images from Kinect
5. (Optional) Switch to Camera 2 for comparison
```

### Scenario: Multiple PCs with Different Cameras

```
PC A has: Kinect v1 on Camera 1
PC B has: Kinect v1 on Camera 0
PC C has: Kinect v1 on Camera 3

Solution:
- Each PC detects its Kinect automatically
- Just click refresh if not found on default
- Application finds correct camera each time
```

## Performance Notes

- **Camera detection**: Takes 2-5 seconds on startup
- **Camera switching**: Takes 1-2 seconds
- **Refresh scan**: Takes 2-5 seconds
- **Live preview**: ~30 FPS regardless of camera

## FAQ

**Q: Why are there blank camera numbers in the dropdown?**
A: The application scans 0-9 but only shows cameras that actually open successfully.

**Q: Can I use multiple cameras at once?**
A: Current version: one camera at a time. Future enhancement could support simultaneous captures.

**Q: How do I know if I'm using the right camera?**
A: Look at the live preview - Kinect v1 has specific appearance, no lens distortion, 640×480 resolution.

**Q: What if camera ID changes between restarts?**
A: Sometimes Windows reassigns camera IDs. Just use the dropdown to select the camera by checking the preview.

**Q: Can I name cameras?**
A: Not in current version. Identification is by camera ID and detected properties.

**Q: What backends does it support?**
A: All OpenCV backends: DirectShow (Windows), V4L (Linux), AVFoundation (Mac), etc.

## Next Steps

1. **Test your camera**:
   - Launch GUI
   - Click dropdown
   - Try each camera briefly
   - Watch live preview
   - Identify your Kinect

2. **Lock in selection**:
   - Once you find your Kinect camera ID
   - Note the number (e.g., Camera 1)
   - Use that camera for consistent results

3. **Backup method**:
   - Note which camera works
   - Document it for future reference
   - If number changes, repeat steps 1-3

---

**Version**: 2.1 (Multi-Camera Support)
**Date**: December 29, 2025
**Status**: Production Ready
