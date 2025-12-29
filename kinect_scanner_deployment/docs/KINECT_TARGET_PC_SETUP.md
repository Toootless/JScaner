# Kinect v1 Scanner - Windows 11 Target PC Setup Guide

**Last Updated**: December 29, 2025  
**Purpose**: Complete setup instructions for running the Kinect v1 Scanner on a separate Windows 11 laptop

## Quick Summary

This document provides everything needed to set up and run the Kinect v1 Scanner (`kinect_scanner.py`) on a Windows 11 target PC. The scanner captures images from a Kinect v1 (Xbox 360) camera that are then processed by the main JScaner application.

---

## Required Programs & Drivers

### 1. **Python 3.11 or Higher** (REQUIRED)
- **Purpose**: Runtime environment for the scanner
- **Download**: https://www.python.org/downloads/
- **Installation**:
  ```powershell
  # Download installer and run
  # IMPORTANT: Check "Add Python to PATH" during installation
  ```
- **Verify Installation**:
  ```powershell
  python --version  # Should show Python 3.11+
  pip --version     # Should work without errors
  ```

### 2. **Kinect v1 (Xbox 360) Drivers** (REQUIRED)
- **Device**: Kinect v1 / Xbox 360 Kinect
- **Connection**: USB 2.0 or USB 3.0 port
- **Driver Options** (choose one):

#### Option A: Official Microsoft Drivers (Recommended)
1. Go to: https://www.microsoft.com/en-us/download/details.aspx?id=34808
2. Download "Kinect for Windows Runtime v1.8"
3. Run the installer
4. Restart your computer

#### Option B: Generic USB Drivers (Fallback)
If official drivers don't work:
1. Open Device Manager (Windows + X → Device Manager)
2. Find "Kinect" or unknown device
3. Right-click → Update driver
4. Select "Browse my computer for drivers"
5. Choose "Let me pick from a list of available drivers"
6. Select "USB Video Device" or similar
7. Complete installation

#### Option C: LibUSBK Drivers (Advanced)
If using libfreenect backend:
1. Download: https://github.com/libusb/libusb/wiki/libusb-on-windows
2. Follow installation in docs/KINECT_V1_LIBUSBK_SETUP.md

**Verify Drivers**:
```powershell
# Open Device Manager and check:
# - Cameras: Kinect should appear
# - Human Interface Devices: Kinect Sensor should appear
```

### 3. **Visual C++ Redistributable** (REQUIRED)
- **Purpose**: Required by OpenCV and other libraries
- **Download**: https://support.microsoft.com/en-us/help/2977003/
- **Choose**: "Visual Studio 2015-2022 Redistributable"
- **Installation**: Run installer and follow prompts
- **Verify**: Libraries should be installed in `C:\Windows\System32\`

### 4. **Git** (OPTIONAL but Recommended)
- **Purpose**: Clone the JScaner project
- **Download**: https://git-scm.com/download/win
- **Installation**: Use default settings
- **Verify**:
  ```powershell
  git --version
  ```

### 5. **Text Editor** (OPTIONAL)
- **Purpose**: Edit configuration files
- **Recommendations**:
  - Visual Studio Code: https://code.visualstudio.com/
  - Notepad++ https://notepad-plus-plus.org/
  - Or use built-in Notepad

---

## Setup Instructions

### Step 1: Install Python (5 minutes)

1. Download Python 3.11 or higher from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Wait for installation to complete
6. Open PowerShell and verify:
   ```powershell
   python --version
   pip --version
   ```

### Step 2: Install Kinect Drivers (5-10 minutes)

1. **Check Device Manager**:
   - Open Device Manager (Win + X → Device Manager)
   - Look for "Kinect" in "Cameras" or "Human Interface Devices"
   - If not found, Kinect is not connected

2. **Install Drivers**:
   - Download "Kinect for Windows Runtime v1.8" from Microsoft
   - Run installer
   - Follow prompts
   - Restart computer

3. **Verify Installation**:
   ```powershell
   # After restart, check Device Manager again
   # Kinect should show "Kinect Sensor" with no warning icons
   ```

### Step 3: Install Visual C++ Runtime (2 minutes)

1. Download Visual Studio 2015-2022 Redistributable
2. Run installer
3. Click "Install"
4. Restart computer

### Step 4: Get JScaner Files (5 minutes)

**Option A: Using Git** (Recommended)
```powershell
git clone https://github.com/username/JScaner.git
cd JScaner
```

**Option B: Manual Download**
1. Download JScaner ZIP file
2. Extract to desired location
3. Open PowerShell in that folder

### Step 5: Install Python Dependencies (3 minutes)

In PowerShell, navigate to the JScaner folder and run:

```powershell
# Install minimal requirements for Kinect scanning
pip install -r requirements_kinect_scanner.txt

# Or install manually
pip install opencv-python numpy Pillow tqdm
```

Expected output:
```
Successfully installed opencv-python-4.x.x
Successfully installed numpy-1.x.x
Successfully installed Pillow-1x.x
Successfully installed tqdm-4.x.x
```

### Step 6: Test Kinect Connection (2 minutes)

```powershell
python test_kinect_v1.py
```

Expected output:
```
✓ Kinect v1 (Xbox 360) - Device found!
✓ Camera initialized successfully
✓ Frame capture working
```

If there are errors, see "Troubleshooting" section below.

---

## Running the Scanner

### Basic Usage

```powershell
python kinect_scanner.py
```

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `h` | Show help | `h` |
| `c` | Capture single frame | `c` or `c my_photo` |
| `a` | Auto-capture sequence | `a 20` (capture 20 frames) |
| `i` | Camera info | `i` |
| `s` | Save manifest | `s` |
| `q` | Quit | `q` |

### Example Workflow

```powershell
# Start scanner
python kinect_scanner.py

# At prompt:
i               # Check camera is working
a 30            # Capture 30 photos automatically
s               # Save manifest file
q               # Quit and save

# Result: Images saved to data/captured/ folder
# manifest.json contains list of all captured images
```

---

## Processing Captured Images

### Step 1: Transfer Data
After capturing images, copy the `data/captured/` folder to your processing PC.

### Step 2: Process in JScaner
On the main JScaner PC:

```powershell
python main.py
```

Then use the GUI to:
1. Load calibration grid
2. Select captured images
3. Perform 3D reconstruction
4. Export as STL

---

## Troubleshooting

### Problem: "Kinect not found"

**Solution**:
1. Check USB connection (use USB 2.0 port if available)
2. Open Device Manager and verify Kinect appears
3. If not:
   - Unplug and wait 10 seconds
   - Plug back in
   - Restart computer
4. Try different USB port

### Problem: "No module named 'cv2'"

**Solution**:
```powershell
# Reinstall OpenCV
pip install --upgrade opencv-python

# Or try with specific version
pip install opencv-python==4.8.0.76
```

### Problem: "Cannot open camera"

**Solution**:
1. Ensure Kinect is the only USB camera device
2. Close other camera applications (Skype, Zoom, etc.)
3. Restart PowerShell and try again
4. Update Kinect drivers

### Problem: "Black/blank screen from camera"

**Solution**:
1. Ensure Kinect is properly powered (has external power supply)
2. Check USB connection
3. Wait 30 seconds for camera to initialize
4. Try different USB port
5. Reinstall drivers

### Problem: Script crashes with Python error

**Solution**:
```powershell
# Check Python version
python --version  # Must be 3.11+

# Reinstall all dependencies
pip install --upgrade --force-reinstall -r requirements_kinect_scanner.txt

# Run in verbose mode for debugging
python -u kinect_scanner.py
```

### Problem: Slow performance or low frame rate

**Solution**:
1. Close other applications using USB
2. Use USB 2.0 port instead of USB 3.0 (more stable for Kinect)
3. Reduce capture interval in auto-capture mode
4. Ensure adequate CPU resources

---

## Complete Software Checklist

Before running the scanner, verify you have:

- [ ] Python 3.11+ installed and added to PATH
- [ ] Kinect v1 drivers installed
- [ ] Visual C++ Redistributable installed
- [ ] JScaner files downloaded
- [ ] Python dependencies installed (`pip install -r requirements_kinect_scanner.txt`)
- [ ] Kinect hardware connected via USB
- [ ] test_kinect_v1.py runs successfully
- [ ] kinect_scanner.py starts without errors

---

## Performance Tips

### Optimal Setup
- Use **USB 2.0 port** (more stable than USB 3.0)
- Position Kinect on stable surface
- Ensure good lighting for RGB capture
- Use external hard drive for large capture sessions
- Close unnecessary background applications

### Capture Recommendations
- Capture 20-30 images per scanning session
- Wait 0.5-1 second between captures
- Move object or camera slightly between shots
- Ensure even lighting and no shadows
- Position object against reference grid

### File Management
- Organize captures by project: `data/captured/project_name/`
- Keep manifests for tracking
- Backup captures to external storage
- Use consistent naming conventions

---

## File Structure on Target PC

```
JScaner/
├── kinect_scanner.py           # Main scanning program
├── test_kinect_v1.py          # Test script
├── requirements_kinect_scanner.txt
├── data/
│   └── captured/              # Captured images go here
│       ├── scan_20250101_120000_001.jpg
│       ├── scan_20250101_120000_001_metadata.json
│       └── manifest.json
└── docs/
    └── KINECT_TARGET_PC_SETUP.md  # This file
```

---

## Support Resources

### Documentation Files
- **KINECT_V1_QUICK_START.md** - Quick setup guide
- **docs/KINECT_V1_INTEGRATION.md** - Technical details
- **docs/KINECT_V1_LIBUSBK_SETUP.md** - Advanced driver setup
- **README.md** - General JScaner documentation

### External Resources
- Microsoft Kinect Documentation: https://msdn.microsoft.com/en-us/library/hh438998.aspx
- OpenCV VideoCapture: https://docs.opencv.org/master/d8/dfe/classcv_1_1VideoCapture.html
- Python Documentation: https://docs.python.org/3/

---

## Network Transfer of Scans

### Option 1: USB Drive (Recommended)
1. Copy `data/captured/` folder to USB drive
2. Transfer to processing PC
3. Extract to processing machine's JScaner folder

### Option 2: Network Share (Windows)
1. On processing PC, create shared folder
2. On scanner PC, map network drive
3. Save captures directly to network share

### Option 3: Cloud Storage
1. Set up OneDrive sync to `data/captured/`
2. Files automatically sync to cloud and other PCs

---

## FAQ

**Q: Can I use Kinect v2 instead?**  
A: Kinect v2 requires different drivers and libraries. This guide is for Kinect v1 (Xbox 360 Kinect) only.

**Q: What if I don't have an external power supply for Kinect?**  
A: Kinect v1 requires external power. Most come with a power adapter. Without power, the device cannot initialize.

**Q: Can I use a USB hub?**  
A: Avoid hubs - connect Kinect directly to computer USB port for best reliability.

**Q: How many images should I capture?**  
A: 20-30 images per object provides good coverage for 3D reconstruction.

**Q: Can I preview images before processing?**  
A: Yes, use Windows Explorer to browse `data/captured/` folder.

**Q: Is there a GUI version of the scanner?**  
A: The current version is command-line. The full JScaner GUI is used for processing.

---

## Version Information

- **JScaner Version**: 2.0+
- **Python Support**: 3.11, 3.12, 3.13, 3.14
- **Windows Support**: Windows 10, Windows 11
- **Kinect Support**: Xbox 360 Kinect v1 only
- **Last Updated**: December 29, 2025

---

**Next Step**: Run the scanner with `python kinect_scanner.py` and follow the on-screen prompts!
