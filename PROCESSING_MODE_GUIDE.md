# JScaner Image Processing Mode - Quick Guide

## Overview

The program has been updated to **remove webcam support** and focus on **processing captured images and metadata files** for 3D reconstruction.

## ✅ What's New

- **📁 Image Processing Focus** - Load and process images with metadata
- **📊 Metadata Support** - Automatically reads JSON metadata files from Kinect captures  
- **🔄 Batch Processing** - Handle multiple images efficiently
- **🎯 Simplified UI** - Removed all camera/capture controls

## 🚀 How to Use

### Option 1: Quick Launch (Easiest)
```powershell
.\run_jscan_processor.bat
```

The application will:
1. Automatically load your 22 captured images
2. Read all metadata files (timestamps, camera info, resolution)
3. Display them ready for calibration and 3D reconstruction

### Option 2: Manual Launch
```powershell
python main_processor.py
```

## 📊 Loaded Images (22 Total)

Your captured data:
- **Images**: 22 JPG files from `scan_20251230_143607_001.jpg` to `scan_20251230_143650_022.jpg`
- **Metadata**: 22 JSON files with camera configuration
- **Camera**: Kinect v1 (640x480 @ 30fps via .NET SDK)
- **Resolution**: 640×480 pixels
- **Format**: BGR (OpenCV format)

## 🎯 Next Steps in GUI

### Tab 1: Calibration
1. Click **"Load with Metadata"** (optional - images are auto-loaded)
2. Set Grid Square Size: **10.0** mm (or your actual size)
3. Set Grid Pattern: **9 x 6** (or adjust if different)
4. Click **"Analyze Grid Patterns"** to auto-detect
5. Click **"Calibrate Camera"** to compute calibration matrix

### Tab 2: 3D Reconstruction
1. Click **"Reconstruct 3D Model"** to process all images
2. Click **"View Point Cloud"** to see 3D result
3. Monitor progress bar

### Tab 3: Export STL
1. Click **"Export STL"** to save as 3D model file
2. Choose output filename and location
3. Model ready for 3D printing or further processing

## 🗂️ Image Management

In Tab 1 (Capture tab):

- **Load Images from Folder** - Import additional images
- **Load with Metadata** - Load images + JSON metadata files
- **Clear Images** - Remove all loaded images
- **Show Images Folder** - Open the `captured/` directory

## 📋 Metadata Structure

Each image has an associated JSON file with:
```json
{
  "filename": "scan_20251230_143607_001.jpg",
  "timestamp": "20251230_143607",
  "sequence": 1,
  "camera": "Kinect v1 (640x480 @ 30fps via .NET SDK)",
  "resolution": {
    "width": 640,
    "height": 480
  },
  "format": "BGR"
}
```

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| GUI doesn't appear | Check Windows taskbar or use Alt+Tab to switch to window |
| "Python not found" | Install Python 3.11+: https://www.python.org/downloads/ |
| No images loaded | Ensure `captured/` folder is in the same directory as `main_processor.py` |
| Calibration fails | Ensure images show clear checkerboard pattern |
| 3D reconstruction too slow | Close other applications to free up RAM |

## 📁 File Structure

```
3dscaning/
├── main_processor.py          ← New image processor entry point
├── run_jscan_processor.bat    ← Launcher script
├── src/
│   └── gui/
│       └── main_window.py     ← Updated GUI (no camera, image processing)
└── captured/
    ├── scan_20251230_143607_001.jpg
    ├── scan_20251230_143607_001.json
    ├── scan_20251230_143609_002.jpg
    ├── scan_20251230_143609_002.json
    └── ... (22 images total)
```

## 🎓 Workflow Summary

1. **Launch** → `run_jscan_processor.bat`
2. **Load** → Images auto-load from `captured/` folder ✓
3. **Calibrate** → Set grid parameters and calibrate
4. **Reconstruct** → Process images to 3D point cloud
5. **Export** → Save as STL for 3D printing

## 🔧 Advanced: Custom Image Folders

To process different image sets:

1. Click **"Load with Metadata"** in the GUI
2. Select any folder containing JPG and JSON files
3. Files must follow the naming pattern:
   - `image_name.jpg`
   - `image_name.json` (corresponding metadata)

## 📝 Notes

- **Camera Support Removed**: Webcam and Kinect input disabled (processing mode only)
- **Metadata Required**: JSON files should accompany JPG files for best results
- **Batch Processing**: All images in folder are loaded simultaneously
- **Auto-calibration**: Grid patterns can be auto-detected from images

---

**Version**: 2.2  
**Mode**: Image Processing (No Camera Input)  
**Last Updated**: December 30, 2025
