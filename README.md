# JScaner

A Python 3D scanning application that reconstructs 3D objects from multiple photographs taken against a reference grid. Supports both advanced Open3D reconstruction and fallback methods for maximum compatibility.

## Features

- **Advanced Grid Detection**: Multiple algorithms for detecting calibration patterns including 3D printer beds
- **Dual Camera Support**: Works with Kinect v1 (Xbox 360) or standard USB webcams
- **GPU Acceleration**: NVIDIA RTX 3060 support with CuPy for enhanced performance
- **Auto-Load Calibration**: Automatically loads last saved calibration on startup
- **External Image Import**: Load images from outside sources for processing or calibration
- **Custom Image Naming**: Name captured images with custom filenames
- **Fallback 3D Reconstruction**: Works without Open3D using SciPy and scikit-learn
- **Multi-view Processing**: Analyzes multiple photos to reconstruct 3D geometry
- **STL Export**: Generates standard 3D model files for 3D printing with fallback support
- **Interactive GUI**: User-friendly tabbed interface for image capture and processing
- **Enhanced Computer Vision**: Harris corner detection, CLAHE preprocessing, and line-based grid detection

## System Requirements

### Python Compatibility
- **Python 3.14**: Fully supported with fallback 3D reconstruction
- **Python 3.11-3.13**: Full Open3D support available
- **Python 3.8-3.10**: Legacy support (may require older dependency versions)

### Hardware
- **Camera Options**:
  - Kinect v1 (Xbox 360 Kinect) - preferred with Windows drivers
  - Logitech HD Pro Webcam C920 (standard USB webcam)
  - Any OpenCV-compatible camera
- **NVIDIA GPU**: Optional, enables CuPy acceleration (RTX 3060 tested)
- Reference grid (3D printer bed or printed calibration pattern)
- Windows/Linux/macOS

### GPU Acceleration (Enabled)
- **NVIDIA RTX 3060** (11GB VRAM) - Fully supported and tested
- **CUDA 13.0** toolkit installed and configured
- **CuPy 13.6.0** library for GPU-accelerated processing
- Provides significant performance improvements for point cloud processing and reconstruction

### Webcam Specifications (C920)
- **Resolution**: 1920x1080 (Full HD)
- **Frame Rate**: 30 FPS
- **Autofocus**: Yes (important for sharp grid detection)
- **Field of View**: 78° diagonal
- **Lens**: Carl Zeiss optics with 20-step autofocus

## Installation

### Python 3.10+ Installation (Current Setup)

1. Clone or download this repository
2. Install core dependencies:
   ```bash
   pip install numpy opencv-python scipy scikit-learn matplotlib tqdm cupy open3d pillow trimesh
   ```

3. For GPU acceleration (NVIDIA GPUs with CUDA 13.0):
   ```bash
   pip install cupy
   ```

### Python 3.11-3.13 Installation (Full Open3D Support)

1. Clone or download this repository  
2. Install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Verify Installation

```bash
python main.py
```

You should see:
- ✓ GPU acceleration status
- ✓ Camera detection
- ✓ 3D reconstruction engine status

## Usage

1. **Setup**: Calibration auto-loads from `cal.json` if available
2. **Capture**: Take multiple photos using the built-in camera interface
   - Click "Capture Image" to save frames
   - Enter custom names or use auto-numbering
   - View save location with "Show Save Location" button
3. **Import**: Load external images with "Load Images" button
   - Select purpose: Processing or Calibration
   - Images marked with [EXT] prefix
4. **Process**: Run 3D reconstruction with GPU acceleration
5. **Export**: Save as STL file for 3D printing

### Quick Start

```bash
python main.py
```

### New Features

- **Auto-Load**: Last calibration loads automatically on startup
- **Custom Naming**: Name each captured image before saving
- **Import Images**: Load external photos for processing or calibration
- **Save Location**: View and access captured image directory
- **GPU Status**: Real-time GPU acceleration status display

## Project Structure

- `src/core/`: Core computer vision and 3D reconstruction algorithms
- `src/gui/`: User interface components
- `data/`: Sample data and calibration patterns
- `examples/`: Example usage and tutorials
- `tests/`: Unit tests

## Camera Setup

### Kinect v1 (Xbox 360)
- **Status**: ✅ **FULLY WORKING**
- **Setup**: Install Windows SDK 1.8, connect to USB, select in GUI
- **Driver**: Uses standard Windows Kinect drivers via OpenCV
- **Frame Size**: 640x480 @ 30 FPS
- **Resolution**: 640x480 RGB (no depth support in this build)
- **Instructions**: See [Kinect v1 Setup Guide](docs/KINECT_V1_INTEGRATION.md)

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