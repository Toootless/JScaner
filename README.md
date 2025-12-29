# Kinect v1 Scanner - Professional 3D Scanning Suite

[![Version](https://img.shields.io/badge/version-2.1-blue.svg)](https://github.com/yourusername/kinect-scanner)
[![Status](https://img.shields.io/badge/status-Production%20Ready-green.svg)](https://github.com/yourusername/kinect-scanner)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A professional-grade 3D scanning application for Kinect v1 (Xbox 360 Kinect) cameras on Windows 10/11, featuring an intuitive graphical interface with automatic multi-camera detection.

## 🎯 Key Features

### Core Scanning
- **📷 Live Camera Preview** - Real-time 640×480 video feed from any camera
- **Single Image Capture** - One-click to save high-quality images
- **🔄 Batch Capture** - Automated multi-image collection with configurable intervals (0.2-5 seconds)
- **📊 Real-time Statistics** - Live counter showing captured image count
- **💾 Manifest Export** - Automatic JSON metadata export

### Multi-Camera Support (v2.1)
- **🔍 Auto-Detection** - Automatically scans and lists all connected cameras
- **📱 Camera Selection** - Simple dropdown menu to switch cameras instantly
- **🔄 Refresh Button** - Rescan system for newly connected devices
- **📝 Camera Tracking** - Records camera ID and properties in manifest.json
- **⚡ Fast Switching** - Switch cameras in <2 seconds

### User Interface
- **🎨 Professional GUI** - Clean, intuitive tkinter-based interface
- **⚙️ No Command-Line** - Everything is point-and-click
- **🚀 Fast Startup** - Minimal overhead, instant camera access
- **📁 Quick Folder Access** - One-click to open captured images directory

## 📋 System Requirements

| Component | Requirement |
|-----------|------------|
| **OS** | Windows 10 or Windows 11 |
| **Python** | 3.11 or later (3.12, 3.13, 3.14 supported) |
| **RAM** | 2 GB minimum (4 GB recommended) |
| **Storage** | 5 GB free space |
| **USB** | Direct USB 2.0/3.0 connection |
| **Camera** | Xbox 360 Kinect v1 + power supply |

## 🚀 Quick Start

### 30-Second Setup

```bash
# Extract deployment package
unzip Kinect_Scanner_Deployment.zip

# Run automated setup (handles everything)
AUTOMATED_SETUP.bat

# Launch the scanner
run_kinect_scanner_gui.bat
```

### First Scan

1. Launch `run_kinect_scanner_gui.bat`
2. See "Camera Selection" dropdown at top
3. Try each camera to find your Kinect
4. Click **"📷 Capture Single Image"**
5. Images save to `data/captured/`

## 📦 Installation

### Method 1: Automated (Recommended)

```batch
# Windows batch file - handles everything
AUTOMATED_SETUP.bat
```

This automatically:
- Downloads Python 3.12 (if needed)
- Installs Visual C++ Runtime (if needed)
- Installs all Python packages
- Verifies Kinect hardware
- Starts the scanner

### Method 2: Manual Installation

```bash
# 1. Install Python 3.11+ from python.org

# 2. Install required packages
pip install -r requirements_kinect_scanner.txt

# 3. Install Kinect drivers (see docs/KINECT_TARGET_PC_SETUP.md)

# 4. Connect Kinect v1 hardware

# 5. Run the scanner
python kinect_scanner_gui.py
```

### Method 3: CLI Version (Power Users)

```bash
# Original command-line interface
python kinect_scanner.py
```

## 📚 Documentation

### Quick Start Guides
- **[MULTI_CAMERA_QUICK_REF.md](MULTI_CAMERA_QUICK_REF.md)** - 2-minute overview of multi-camera features
- **[KINECT_SCANNER_GUI_QUICK_START.md](KINECT_SCANNER_GUI_QUICK_START.md)** - Step-by-step quickstart
- **[START_HERE_KINECT_SCANNER.md](START_HERE_KINECT_SCANNER.md)** - Complete beginner guide

### Feature Guides
- **[KINECT_SCANNER_GUI_GUIDE.md](KINECT_SCANNER_GUI_GUIDE.md)** - Complete GUI reference & controls
- **[MULTI_CAMERA_GUIDE.md](MULTI_CAMERA_GUIDE.md)** - Multi-camera support & troubleshooting
- **[CHOOSE_YOUR_VERSION.md](CHOOSE_YOUR_VERSION.md)** - GUI vs CLI comparison

### Troubleshooting
- **[CAMERA_SELECTION_TROUBLESHOOTING.md](CAMERA_SELECTION_TROUBLESHOOTING.md)** - Camera identification issues
- **[docs/KINECT_TARGET_PC_SETUP.md](docs/KINECT_TARGET_PC_SETUP.md)** - Hardware setup instructions
- **[INDEX_DOCUMENTATION.md](INDEX_DOCUMENTATION.md)** - Master documentation index

## 🔧 Camera Selection (Multi-Camera v2.1)

### Identifying Your Kinect

Look for these characteristics:

| Feature | Kinect v1 | Other Cameras |
|---------|-----------|---------------|
| **Resolution** | 640×480 ✓ | Usually different |
| **Image** | Rectangular | Wide-angle |
| **Distortion** | None | Possible fisheye |
| **FPS** | 30 @ 640×480 | Varies |

### How to Find It

1. Launch GUI (`run_kinect_scanner_gui.bat`)
2. Click dropdown at top - see all cameras
3. Try each camera by clicking
4. Watch live preview
5. When you see the Kinect image (640×480, rectangular) → **use that one**

### If Kinect Not Found

1. Click the **"🔄 Refresh"** button to rescan
2. Check USB connection
3. Verify Kinect power supply is plugged in
4. See [CAMERA_SELECTION_TROUBLESHOOTING.md](CAMERA_SELECTION_TROUBLESHOOTING.md) for detailed help

### Standard Webcam (Logitech C920, etc.)
- **Status**: ✅ Fully Supported
- **Setup**: Connect USB, select in Camera Settings, ready to use
- **Resolution**: 1920x1080 (Full HD)
- **Frame Rate**: 30 FPS

### Camera Selection in JScaner
1. Launch JScaner: `python main.py`
2. Look at **Camera Settings** panel (left sidebar)
3. Click radio button:
   - ⭕ **🎮 Xbox Kinect v1** → Use Kinect camera
   - ⭕ **📷 Logitech Webcam** → Use USB webcam
4. Camera preview updates immediately

## Technical Details

The system uses:
- **OpenCV** for image processing and camera calibration
- **NumPy** for numerical computations
- **Open3D** for 3D geometry processing
- **Tkinter** for the graphical interface

## Grid Calibration

The reference grid provides known measurements that allow the system to:
- Determine real-world scale
- Correct for camera distortion
- Establish coordinate systems
- Validate reconstruction accuracy

## Contributing

This project is designed for educational and research purposes. Feel free to experiment and improve the algorithms.

## License

MIT License - See LICENSE file for details.