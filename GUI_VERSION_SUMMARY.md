# Kinect Scanner - Next Generation GUI Version

## 📦 What's New

The **Kinect Scanner GUI** is the next evolution of your scanner software:

### ✨ Key Features

- **Live Camera Preview** - Real-time 640x480 video feed in the window
- **Single Image Capture** - One-click button to capture images
- **Batch Capture** - Automated multi-image capture (10, 20, 50+)
- **Configurable Intervals** - Set delay between captures (0.3 - 5.0 seconds)
- **Real-time Statistics** - Live counter of captured images
- **Manifest Export** - Auto-generate JSON list of all captures
- **Quick Folder Access** - Open images directory instantly

### 🎯 Use Cases

| Need | Solution |
|------|----------|
| Quick photo | Click "Capture Single Image" |
| 360° scan (12 angles) | Set Batch Count to 12, interval 1.0 sec, rotate object |
| Rapid capture series | Set Batch Count to 50, interval 0.3 sec |
| Preview before capture | Live feed in main window shows exactly what you'll get |
| Organize captures | Manifest.json lists everything with timestamps |

## 📁 New Files Created

```
✓ kinect_scanner_gui.py                 (Main GUI application - 700+ lines)
✓ run_kinect_scanner_gui.bat            (Windows launcher)
✓ run_kinect_scanner_gui.ps1            (PowerShell launcher)
✓ KINECT_SCANNER_GUI_GUIDE.md           (Full documentation)
✓ KINECT_SCANNER_GUI_QUICK_START.md     (Quick reference)
✓ GUI_VERSION_SUMMARY.md                (This file)
```

## 🚀 How to Use

### Launch Options

**Option 1: Batch File (Easiest)**
```batch
run_kinect_scanner_gui.bat
```

**Option 2: PowerShell**
```powershell
run_kinect_scanner_gui.ps1
```

**Option 3: Direct Python**
```bash
python kinect_scanner_gui.py
```

### Start Capturing

1. **Wait for "Camera connected ✓"**
2. **Click "📷 Capture Single Image"** to grab one photo
   - OR set Batch Count and click **"🔄 Start Batch Capture"** for multiple

3. **Images automatically saved** to `data/captured/scan_TIMESTAMP.jpg`

4. **View statistics** in real-time (capture counter updates instantly)

## 🎮 Button Guide

| Button | Purpose | When to Use |
|--------|---------|------------|
| 📷 Capture Single Image | Save one image | Quick single shots |
| 🔄 Start Batch Capture | Save multiple images | 360° scans, datasets |
| ⏹ Stop Batch | Cancel batch in progress | If you need to stop |
| 📁 Open Capture Folder | View images on disk | Browse saved photos |
| 💾 Export Manifest | Create image list JSON | Organize & document |

## 📊 Status Display

Left section shows:
- **Status**: Current operation (Ready, Capturing, etc.)
- **Images Captured**: Total count this session

Live preview shows:
- Real-time camera feed
- Capture counter overlay
- Batch progress indicator

## 🔧 Batch Capture Examples

### Example 1: Simple 5-Image Sequence
```
Count: 5
Interval: 1.0
Result: 5 images, 1 second apart
Use Case: Quick test shots
```

### Example 2: 360° Object Scan
```
Count: 12
Interval: 0.5
Result: 12 images, 30° apart (rotate manually)
Use Case: Full object scanning
```

### Example 3: Rapid Dataset
```
Count: 50
Interval: 0.2
Result: 50 images, nearly continuous
Use Case: High-volume data collection
```

## 💾 Files Location

All captured images go to:
```
data/captured/
├── scan_20251229_143022_456.jpg
├── scan_20251229_143023_789.jpg
├── ...
└── manifest.json  (created when you export)
```

Each filename includes **TIMESTAMP** so no overwrites:
- `YYYYMMDD` - Date
- `HHMMSS` - Time
- `mmm` - Milliseconds

## 📈 Performance Tips

- **Faster captures**: Reduce interval to 0.2-0.3 seconds
- **Steady captures**: Use 1-2 second interval for alignment
- **Large batches**: Capture in 30-image sessions for best performance
- **USB direct**: Connect Kinect directly (no USB hubs)

## 🎯 Comparison: CLI vs GUI

| Feature | CLI Version | GUI Version |
|---------|-------------|------------|
| **Preview** | Text commands | Live video window |
| **Capture** | Type commands | Click buttons |
| **Speed** | Fast | Fast |
| **Learning Curve** | Moderate | Easy |
| **Automation** | ✓ Scripts | ✓ Batch mode |
| **Use Case** | Power users | Everyone |

**Both included!** Use whichever fits your workflow.

## 🔄 Upgrading Existing Deployments

If you already have the deployment package:

1. **Copy new files to deployment folder**:
   - `kinect_scanner_gui.py`
   - `run_kinect_scanner_gui.bat`
   - `run_kinect_scanner_gui.ps1`
   - `KINECT_SCANNER_GUI_GUIDE.md`
   - `KINECT_SCANNER_GUI_QUICK_START.md`

2. **Update AUTOMATED_SETUP.bat** (optional) to mention GUI option

3. **No new dependencies** - GUI uses only built-in tkinter + existing packages

4. **Old CLI version still works** - Nothing removed, only added

## 🚀 Next: Deploy to Target PC

The GUI version works exactly like the CLI:

1. **Add files to deployment package**
2. **Run AUTOMATED_SETUP.bat** on target PC (handles everything)
3. **Target PC user clicks `run_kinect_scanner_gui.bat`**
4. **GUI launches with live preview**
5. **Start capturing immediately**

## 📝 Summary

**What changed:**
- ✅ New beautiful GUI interface
- ✅ Live camera preview window
- ✅ One-click capture buttons
- ✅ Batch capture with progress tracking
- ✅ Status indicators and counters
- ✅ Better user experience

**What stayed the same:**
- ✅ Same Kinect hardware support
- ✅ Same image quality (640x480)
- ✅ Same file format (JPEG)
- ✅ Same manifest export
- ✅ Same data organization
- ✅ CLI version still available

**What's added:**
- ✅ Visual feedback
- ✅ Intuitive controls
- ✅ Real-time statistics
- ✅ Better for non-technical users

---

**Ready to use!** Launch `run_kinect_scanner_gui.bat` and start capturing.

For questions, see:
- `KINECT_SCANNER_GUI_QUICK_START.md` - Quick reference
- `KINECT_SCANNER_GUI_GUIDE.md` - Full documentation
- `KINECT_SETUP.md` - Hardware setup
- `test_kinect_v1.py` - Hardware diagnostics

**Version**: 2.0 (GUI Enhanced)
**Status**: Production Ready ✓
