# Kinect Scanner GUI - Quick Start

## 30-Second Setup

1. **Launch**: Double-click `run_kinect_scanner_gui.bat`
2. **Wait**: See "Camera connected ✓"
3. **Capture**: Click **"📷 Capture Single Image"** button
4. **Done**: Images save automatically to `data/captured/`

## What You'll See

```
┌─────────────────────────────────────────────────────────────┐
│                    LIVE CAMERA PREVIEW                       │
│         [Real-time Kinect camera feed showing here]          │
│                      Captured: 3                              │
│                                                               │
└─────────────────────────────────────────────────────────────┘

[IMAGE COLLECTION] | [STATUS: Ready, Captured: 3] | [Open Folder] [Export]
```

## Common Tasks

### 📷 Capture One Image
```
Click: "📷 Capture Single Image"
Result: scan_TIMESTAMP.jpg saved
```

### 🔄 Capture 10 Images (One Per Second)
```
1. Change "Count" to 10
2. Keep "Interval" at 1.0 (seconds)
3. Click "🔄 Start Batch Capture"
4. Wait for completion
5. Result: 10 images saved with 1 second between each
```

### 🔄 Rapid Capture (No Delay)
```
1. Set "Count" to 20
2. Set "Interval" to 0.3 (300ms between captures)
3. Click "🔄 Start Batch Capture"
4. Result: 20 images captured rapidly
```

### 💾 Export Image List
```
Click: "💾 Export Manifest"
Result: manifest.json created listing all images
```

### 📁 Open Images Folder
```
Click: "📁 Open Capture Folder"
Result: Windows Explorer opens showing all saved images
```

## Status Messages

| Status | Meaning |
|--------|---------|
| Camera connected ✓ | Ready to capture |
| ✓ Captured: filename | Single image saved |
| Batch: 5/10 | Capturing 5 of 10 images |
| ✓ Batch complete: 10 images | Batch finished |
| Batch stopped by user | You clicked Stop |

## Button States

| Button | State | Meaning |
|--------|-------|---------|
| 📷 Capture Single | Always enabled | Click anytime |
| 🔄 Start Batch | Enabled | Ready for batch |
| 🔄 Start Batch | Disabled (grayed) | Batch running |
| ⏹ Stop Batch | Disabled | No batch running |
| ⏹ Stop Batch | Enabled | Click to stop batch |

## File Organization

```
data/captured/
├── scan_20251229_143022_456.jpg     ← First capture
├── scan_20251229_143023_789.jpg     ← Second capture
├── scan_20251229_143024_012.jpg
├── ...
└── manifest.json                    ← Image list (export)
```

## Troubleshooting

**"Camera not connected"**
- Check Kinect USB cable
- Run `test_kinect_v1.py` to diagnose
- See KINECT_SETUP.md

**Preview not showing**
- Wait 3-5 seconds for camera to initialize
- Try restarting application
- Check if Kinect power is on

**Can't capture images**
- Ensure Kinect is powered on (LED visible)
- Check USB connection is direct (not through hub)
- Close any other camera applications

## Next Steps

- **Single captures**: Great for still object scanning
- **Batch capture**: Perfect for 360° rotation (12-36 images)
- **Multiple sessions**: Capture several batches to build dataset
- **Export manifest**: Use JSON file to import to main JScaner app

## Tips

✅ **Good**:
- Stable object positioning
- Consistent lighting
- Direct USB connection
- Steady hands or tripod

❌ **Avoid**:
- Moving object during capture
- Bright backlighting
- USB hubs
- Multiple USB devices

---

**Ready?** Double-click `run_kinect_scanner_gui.bat` to start!
