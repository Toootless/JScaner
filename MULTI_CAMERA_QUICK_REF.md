# Multi-Camera Update - Quick Reference

## Problem → Solution

| Issue | Before | After |
|-------|--------|-------|
| **Wrong camera** | Always Camera 0 | Dropdown menu to select |
| **System webcam used** | No way to switch | Click dropdown → select |
| **Kinect not detected** | Manual workaround | Auto-detects, shows list |
| **Camera switching** | Required restart | 1-click, instant switch |
| **Multiple cameras** | Confusing setup | Clear selection interface |

## One-Line Summary

**App now auto-detects ALL cameras and lets you click to switch between them.**

## 30-Second Setup

```
1. Run: run_kinect_scanner_gui.bat
2. See: "📷 Camera Selection" dropdown at top
3. Click: Try each camera (watch preview)
4. Find: The one showing Kinect image
5. Scan: Start capturing!
```

## What You'll See

```
At top of window:
┌─────────────────────────────────────────┐
│ 📷 Camera Selection: [Camera 0 ▼] 🔄   │
│                                         │
│ Current: Camera 0 (Default) - 640×480   │
└─────────────────────────────────────────┘

Click dropdown to choose Camera 1, 2, 3...
```

## Camera Identification Quick Chart

| Camera | Likely Device | How to Spot |
|--------|--------------|-----------|
| **0** | Built-in webcam | Skip this one |
| **1** | First USB device | Might be Kinect |
| **2** | Second USB device | Might be Kinect |
| **3+** | More USB devices | Try each |
| **Kinect v1** | 640×480 | Rectangular, no distortion |

## Testing Each Camera (< 1 minute)

```
Camera 0: Click in dropdown
          Watch preview 3 sec
          Not the Kinect? → Try next

Camera 1: Click in dropdown
          Watch preview 3 sec
          Is this it? → YES or try next

Camera 2: Same process...
          Keep going until you find it!
```

## Success Indicator

✓ You found it when:
- Preview shows **rectangular, undistorted** image
- No fisheye or wide-angle distortion
- Image is **clear and sharp**
- Resolution shows **640×480**

## If Kinect Not in List

**Quick fix**:
1. Click **"🔄 Refresh"** button
2. Wait 3-5 seconds
3. Try dropdown again

**Or**:
1. Unplug Kinect
2. Wait 5 seconds
3. Plug back in
4. Click Refresh

## File Changes

```
✅ Updated: kinect_scanner_gui.py
   • New camera detection
   • New dropdown menu
   • New refresh button
   
✅ Added: MULTI_CAMERA_GUIDE.md
✅ Added: CAMERA_SELECTION_TROUBLESHOOTING.md
✅ Added: MULTI_CAMERA_UPDATE.md
```

## No Other Changes Needed

- Capture buttons work the same
- Image quality unchanged
- Same file format (JPEG)
- Same data location
- Backward compatible

## Most Important Points

1. **Dropdown at top** - Camera selection
2. **Click and watch preview** - Shows live feed
3. **Switch until Kinect appears** - Easy to identify
4. **Refresh button** - If camera missing
5. **Select, then capture** - Start scanning

## Keyboard Shortcuts

- **Tab**: Move between dropdown options
- **Arrow keys**: Navigate dropdown
- **Enter**: Confirm selection
- **Alt+F4**: Close window

## Manifest Includes

When you export images, metadata now shows:

```json
{
  "camera_id": 1,
  "camera_name": "Camera 1 (DirectShow) - 640x480 @ 30fps",
  "images": [...]
}
```

Tracks which camera was used!

## Troubleshooting Flowchart

```
App starts
    ↓
See camera dropdown?
    ├─ YES → Try each camera (watch preview)
    │          Found Kinect? → START SCANNING ✓
    │          Not found? → Click "🔄 Refresh"
    │
    └─ NO → Something wrong
              See CAMERA_SELECTION_TROUBLESHOOTING.md
```

## Common Camera Resolutions

| Device | Resolution | Backend |
|--------|-----------|---------|
| Kinect v1 | **640×480** ✓ | DirectShow |
| System webcam | 1280×720 | DirectShow |
| USB HD camera | 1920×1080 | USB |
| Laptop built-in | 1366×768 | Built-in |

**Kinect is very distinctive: exactly 640×480**

## Testing Commands

### Manual camera scan (PowerShell)
```powershell
python -c "
import cv2
for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(f'Camera {i}: {int(w)}x{int(h)}')
        cap.release()
"
```

### Quick test script
```bash
python test_kinect_v1.py
(Specific Kinect hardware test)
```

## Bottom Line

**The program now finds your Kinect automatically and lets you select it from a simple dropdown menu. No more wrong camera!**

---

**Need details?** Read:
- `MULTI_CAMERA_GUIDE.md` - Complete feature guide
- `CAMERA_SELECTION_TROUBLESHOOTING.md` - Problem solving
- `MULTI_CAMERA_UPDATE.md` - Technical details

**Ready to use?** Just run:
```
run_kinect_scanner_gui.bat
```

---

**Version**: 2.1 (Multi-Camera Support)
**Status**: Production Ready ✓
**Last Updated**: December 29, 2025
