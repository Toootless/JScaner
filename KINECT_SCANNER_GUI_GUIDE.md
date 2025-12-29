# Kinect Scanner GUI - Next Generation

## Overview

The **Kinect Scanner GUI** is an enhanced, user-friendly version of the Kinect scanner with:
- **Live Camera Preview** - Real-time feed from Kinect v1
- **Single Image Capture** - One-click image collection
- **Batch Capture** - Automated multi-image capture with configurable interval
- **Metadata Tracking** - Automatic JSON manifest export
- **Real-time Statistics** - Live counter of captured images
- **Utilities** - Quick access to capture folder and manifest export

## Features

### 📷 Live Preview
- Real-time camera feed in the main window
- Frame resolution: 640x480 @ 30 FPS
- Display overlay showing current capture count
- Batch capture indicator during multi-image collection

### Single Capture
- **"📷 Capture Single Image"** button
- One click = one high-quality image
- Automatic timestamped filename: `scan_YYYYMMDD_HHMMSS_mmm.jpg`
- Instant feedback in status bar

### Batch Capture
- **"🔄 Start Batch Capture"** button
- Configurable image count (e.g., 10, 50, 100)
- Configurable capture interval in seconds (0.5 to 5.0 recommended)
- Real-time progress counter
- Stop button to cancel mid-batch
- Perfect for automated scanning sessions

### Status & Statistics
- **Live Status Display** - Current operation status
- **Image Counter** - Total captured images this session
- **Batch Counter** - Current position in batch capture

### Utilities
- **📁 Open Capture Folder** - Quick access to images on disk
- **💾 Export Manifest** - Create JSON file listing all captured images with metadata

## Controls Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    LIVE CAMERA PREVIEW                       │
│                      (640x480 feed)                           │
│                                                               │
│                   [Camera Feed Display]                       │
│                                                               │
└─────────────────────────────────────────────────────────────┘

IMAGE COLLECTION  │  STATUS & STATS  │  UTILITIES
─────────────────────────────────────────────────────
📷 Capture Single │  Status: Ready   │  📁 Open Folder
                  │  Captured: 15    │  💾 Export Manifest
Batch Capture:    │                  │
Count: [10]       │                  │
Interval: [1.0]   │                  │
🔄 Start Batch    │                  │
⏹ Stop Batch      │                  │
```

## Usage Guide

### Basic Single Image Capture
1. Launch GUI: `run_kinect_scanner_gui.bat`
2. Wait for "Camera connected ✓" in status
3. Position object in view
4. Click **"📷 Capture Single Image"**
5. Image saved automatically
6. Counter increments

### Batch Capture Session (e.g., 360° object scan)
1. Set **Count** to desired number (e.g., 12 for 360° with 30° intervals)
2. Set **Interval** to time between captures (e.g., 0.5 for continuous)
3. Position object at first angle
4. Click **"🔄 Start Batch Capture"**
5. Rotate object between each capture
6. Watch progress counter
7. Click **"⏹ Stop Batch"** to cancel if needed

### Export Captured Images
1. Click **"💾 Export Manifest"**
2. JSON file created: `manifest.json`
3. Contains:
   - Total image count
   - Image filenames
   - File sizes
   - Creation timestamps

### Open Capture Folder
- Click **"📁 Open Capture Folder"**
- Windows Explorer opens showing all captured images
- Browse/preview images
- Copy/move files as needed

## File Locations

```
Project Root/
├── kinect_scanner_gui.py           [GUI Application]
├── run_kinect_scanner_gui.bat      [Windows Launcher]
├── run_kinect_scanner_gui.ps1      [PowerShell Launcher]
└── data/
    └── captured/
        ├── scan_20251229_143022_456.jpg
        ├── scan_20251229_143023_789.jpg
        ├── ...
        └── manifest.json
```

## Keyboard Shortcuts
(Future enhancement - currently button-driven)

## Troubleshooting

### Issue: "Camera not connected"
- **Solution**: Check Kinect USB cable connection
- Ensure Kinect drivers are installed (see KINECT_SETUP.md)
- Try running test_kinect_v1.py for hardware diagnostics

### Issue: Preview freezes
- **Solution**: Click close (X) to exit
- Restart the application
- Check if another program is using the camera

### Issue: Batch capture stops mid-sequence
- **Solution**: Check camera power connection
- Ensure USB cable is secure
- Restart the application

### Issue: Low frame rate or stuttering
- **Solution**: Close other applications
- Check CPU usage (Task Manager)
- Ensure USB connection is direct (no hubs)
- Reduce preview resolution if needed

### Issue: Cannot export manifest
- **Solution**: Ensure data/captured/ folder exists
- Check write permissions on disk
- Verify at least one image was captured

## System Requirements

- **Python**: 3.11 or later
- **Windows**: Windows 10 or 11
- **RAM**: 2 GB minimum (4 GB recommended)
- **CPU**: Intel Core i5 / AMD Ryzen 5 or better
- **USB**: Direct USB 2.0/3.0 connection (no hubs recommended)
- **Kinect v1**: Xbox 360 Kinect with power supply

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| opencv-python | ≥4.8.0 | Camera capture and image processing |
| numpy | ≥1.24.0 | Numerical operations |
| Pillow | ≥10.0.0 | Image format support |
| tkinter | built-in | GUI framework |

**Note**: tkinter is included with Python, no separate installation needed.

## Performance Tips

1. **Faster Batch Capture**: Reduce interval to 0.3-0.5 seconds
2. **Better Quality**: Use longer intervals (1-2 seconds) for steady captures
3. **Large Batches**: Capture in multiple sessions of 20-30 images
4. **Storage**: Save captured images to external SSD for speed
5. **Resolution**: GUI optimizes display - actual saves are always full 640x480

## Advanced Features (Next Version)

- [ ] Grid overlay for alignment
- [ ] Image preview gallery in GUI
- [ ] Manual calibration tool
- [ ] 3D point cloud preview
- [ ] Real-time image filters
- [ ] Auto-export to processing pipeline
- [ ] Recording video sequences
- [ ] Multi-camera support
- [ ] Camera settings adjustment (brightness, contrast, etc.)

## Comparison with CLI Version

| Feature | CLI | GUI |
|---------|-----|-----|
| Live Preview | Text-based | Visual window |
| Capture Control | Commands | Buttons |
| Batch Capture | ✓ | ✓ |
| Manifest Export | ✓ | ✓ |
| Learning Curve | Moderate | Easy |
| Speed | Fast | Fast |
| Automation | ✓ | ✓ |
| User Experience | Technical | Intuitive |

**Recommendation**: Use GUI for interactive sessions, CLI for automated/scripted capture.

## Files in This Package

- `kinect_scanner_gui.py` - Main GUI application (700+ lines)
- `run_kinect_scanner_gui.bat` - Windows batch launcher
- `run_kinect_scanner_gui.ps1` - PowerShell launcher
- `KINECT_SCANNER_GUI_GUIDE.md` - This file

## Quick Start

```bash
# Option 1: Batch launcher (easiest)
run_kinect_scanner_gui.bat

# Option 2: PowerShell launcher
run_kinect_scanner_gui.ps1

# Option 3: Direct Python
python kinect_scanner_gui.py
```

## Support

For issues or questions:
1. Check KINECT_SETUP.md for hardware setup
2. Run test_kinect_v1.py for diagnostics
3. Review troubleshooting section above
4. Check file permissions on data/ folder

---

**Version**: 2.0 (GUI Enhanced)
**Last Updated**: December 2025
**Status**: Production Ready ✓
