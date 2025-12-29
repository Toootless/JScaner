# JScaner Kinect Scanner - Complete Installation Checklist

**For: Windows 11 Target PC with Kinect v1 (Xbox 360)**  
**Date: December 29, 2025**  
**Purpose: Single-document checklist for setting up the Kinect scanning system**

---

## Pre-Installation Checklist

Before starting, verify you have:

- [ ] Windows 11 operating system (Windows 10 also works)
- [ ] Administrator access to the computer
- [ ] Kinect v1 (Xbox 360 Kinect) device
- [ ] Kinect power supply / USB cable
- [ ] Available USB 2.0 or 3.0 port
- [ ] Stable internet connection for downloads
- [ ] At least 5 GB free disk space
- [ ] At least 4 GB RAM (8+ GB recommended)

---

## Phase 1: System Software Installation

### 1.1 Python 3.11+ Installation

**Status**: ☐ Not Started | ☐ In Progress | ☐ Completed

**Steps**:
1. [ ] Visit https://www.python.org/downloads/
2. [ ] Download **Python 3.11 or higher**
3. [ ] Run installer (double-click .exe file)
4. [ ] **CRITICAL**: Check "Add Python to PATH"
5. [ ] Click "Install Now"
6. [ ] Wait for installation to complete (2-3 minutes)
7. [ ] **Verification**:
   - Open PowerShell
   - Type: `python --version`
   - Should show: `Python 3.11.x` or higher
   - Type: `pip --version`
   - Should show: `pip X.X.X`

**Troubleshooting**:
- If "command not found": Python not in PATH, reinstall
- If version is 3.10 or lower: Download higher version
- Administrator rights required for installation

**Estimated Time**: 5 minutes

---

### 1.2 Visual C++ Redistributable Installation

**Status**: ☐ Not Started | ☐ In Progress | ☐ Completed

**Steps**:
1. [ ] Visit: https://support.microsoft.com/en-us/help/2977003/
2. [ ] Download **"Visual Studio 2015-2022 Redistributable"**
3. [ ] Choose correct architecture:
   - [ ] x64 (for most modern computers)
   - [ ] x86 (if running 32-bit Python)
4. [ ] Run installer
5. [ ] Click "Install"
6. [ ] **CRITICAL**: Restart your computer
7. [ ] **Verification**:
   - Windows + R
   - Type: `systeminfo`
   - Check that Visual C++ redistributables are listed

**Estimated Time**: 3 minutes + restart

---

### 1.3 Kinect v1 Driver Installation

**Status**: ☐ Not Started | ☐ In Progress | ☐ Completed

**Preparation**:
1. [ ] Connect Kinect v1 to USB port
2. [ ] Ensure Kinect has power (LED should be green/orange)
3. [ ] Wait 30 seconds for device recognition

**Driver Installation (Choose ONE method)**:

#### Method A: Official Microsoft Drivers (Recommended)
1. [ ] Visit: https://www.microsoft.com/en-us/download/details.aspx?id=34808
2. [ ] Download "Kinect for Windows Runtime v1.8"
3. [ ] Run installer
4. [ ] Accept license terms
5. [ ] Click "Install"
6. [ ] **CRITICAL**: Restart your computer

#### Method B: Windows Auto-Install (Fallback)
1. [ ] Open Device Manager (Win + X → Device Manager)
2. [ ] Find unknown "Kinect" device (may show with warning icon)
3. [ ] Right-click → "Update driver"
4. [ ] Select "Search automatically for updated driver software"
5. [ ] Follow prompts
6. [ ] Restart computer

#### Method C: Manual Driver Install (Advanced)
1. [ ] Open Device Manager
2. [ ] Right-click Kinect device
3. [ ] "Update driver" → "Browse my computer"
4. [ ] Select generic "USB Video Device" driver
5. [ ] Complete installation

**Verification**:
- [ ] Open Device Manager
- [ ] Navigate to "Cameras"
- [ ] Should see "Kinect" or "Kinect Sensor"
- [ ] No warning icons (yellow exclamation marks)
- [ ] LED on Kinect is GREEN (not red)

**Estimated Time**: 5-10 minutes + restart

---

## Phase 2: JScaner Setup

### 2.1 Download JScaner Project

**Status**: ☐ Not Started | ☐ In Progress | ☐ Completed

#### Option A: Using Git (Recommended)
```powershell
# Open PowerShell in desired folder
git clone https://github.com/username/JScaner.git
cd JScaner
```

#### Option B: Manual Download
1. [ ] Download JScaner ZIP file
2. [ ] Extract to desired folder (e.g., `C:\Users\YourName\JScaner`)
3. [ ] Remember the folder path

**Estimated Time**: 2 minutes

---

### 2.2 Install Python Dependencies

**Status**: ☐ Not Started | ☐ In Progress | ☐ Completed

**Steps**:
1. [ ] Open PowerShell
2. [ ] Navigate to JScaner folder:
   ```powershell
   cd C:\path\to\JScaner
   ```
3. [ ] Run installation:
   ```powershell
   pip install -r requirements_kinect_scanner.txt
   ```
4. [ ] **Verification**:
   - Installation should complete without errors
   - See: "Successfully installed..."
   - Run: `pip list`
   - Should include: opencv-python, numpy, Pillow, tqdm

**If Installation Fails**:
- [ ] Try: `pip install --upgrade pip`
- [ ] Then retry: `pip install -r requirements_kinect_scanner.txt`
- [ ] Or manual install:
  ```powershell
  pip install opencv-python numpy Pillow tqdm
  ```

**Estimated Time**: 3-5 minutes (depends on internet speed)

---

## Phase 3: Hardware Testing

### 3.1 Kinect Connection Test

**Status**: ☐ Not Started | ☐ In Progress | ☐ Completed

**Steps**:
1. [ ] Ensure Kinect is connected and powered
2. [ ] Open PowerShell in JScaner folder
3. [ ] Run test script:
   ```powershell
   python test_kinect_v1.py
   ```

**Expected Output**:
```
✓ Kinect v1 (Xbox 360) - Device found!
✓ Camera initialized successfully
✓ Frame capture working
```

**If Test Fails**:
- [ ] Check Kinect power (LED should be green)
- [ ] Verify USB connection
- [ ] Try different USB port (preferably USB 2.0)
- [ ] Restart computer and retry
- [ ] See "Troubleshooting" section below

**Estimated Time**: 2 minutes

---

## Phase 4: Running the Scanner

### 4.1 Start the Scanner

**Status**: ☐ Not Started | ☐ In Progress | ☐ Completed

**Method A: Batch File (Easiest)**
1. [ ] Double-click: `run_kinect_scanner.bat`
2. [ ] Scanner should start automatically

**Method B: PowerShell Script**
1. [ ] Open PowerShell in JScaner folder
2. [ ] Run: `.\run_kinect_scanner.ps1`
3. [ ] Press Enter when prompted

**Method C: Manual Command Line**
```powershell
cd C:\path\to\JScaner
python kinect_scanner.py
```

**Expected Output**:
```
============================================================
  JScaner - Kinect v1 Scanner
  Standalone Image Capture & Export
============================================================

[STARTUP] Scanning for available cameras...
[INFO] Found 1 camera(s): [0]
[SUCCESS] Connected to camera 0
[INFO] Frame size: 640x480

>>>
```

**Estimated Time**: 1 minute to start

---

### 4.2 Basic Capture Test

**Status**: ☐ Not Started | ☐ In Progress | ☐ Completed

**Steps**:
1. [ ] At `>>>` prompt, type: `i` (view camera info)
2. [ ] Type: `c` (capture one photo)
3. [ ] Check output shows: `[CAPTURED] scan_...jpg`
4. [ ] Type: `i` (verify capture count increased)
5. [ ] Type: `q` (quit scanner)

**Verification**:
- [ ] Check folder: `data/captured/`
- [ ] Should contain `.jpg` files
- [ ] Should contain `.json` metadata files
- [ ] Check `manifest.json` file was created

**Estimated Time**: 2 minutes

---

## Phase 5: Production Setup

### 5.1 Create Organized Workflow

**Status**: ☐ Not Started | ☐ In Progress | ☐ Completed

**Steps**:
1. [ ] Create project folders:
   - [ ] `data/captured/Project1/`
   - [ ] `data/captured/Project2/`
   - etc.

2. [ ] For each scanning session:
   - [ ] Position object against reference grid
   - [ ] Adjust lighting
   - [ ] Start scanner: `python kinect_scanner.py`
   - [ ] Capture 20-30 images
   - [ ] Save manifest: type `s`
   - [ ] Exit: type `q`

3. [ ] Transfer files:
   - [ ] Copy `data/captured/` to processing PC
   - [ ] Or backup to external storage

**Estimated Time**: Variable

---

### 5.2 Integration with Main JScaner

**Status**: ☐ Not Started | ☐ In Progress | ☐ Completed

**On Processing PC**:
1. [ ] Copy captured images to processing JScaner folder
2. [ ] Run: `python main.py`
3. [ ] Use GUI to:
   - [ ] Load calibration grid
   - [ ] Select captured images
   - [ ] Process 3D reconstruction
   - [ ] Export as STL file

**Estimated Time**: Variable based on image count

---

## Troubleshooting Checklist

### Kinect Not Detected

**Steps to resolve**:
1. [ ] Check Device Manager (Win + X → Device Manager)
2. [ ] Verify Kinect appears under "Cameras"
3. [ ] If not:
   - [ ] Unplug Kinect from USB
   - [ ] Wait 10 seconds
   - [ ] Plug back in
   - [ ] Wait 30 seconds for detection
4. [ ] Try different USB port (USB 2.0 preferred)
5. [ ] Restart computer
6. [ ] Reinstall drivers
7. [ ] Check Kinect has power (green LED)

**If Still Not Working**:
- [ ] Kinect may be defective
- [ ] Try Kinect on different computer to verify
- [ ] Contact hardware support

---

### "No module named 'cv2'" Error

**Steps to resolve**:
1. [ ] Check Python installation:
   ```powershell
   python --version
   ```
2. [ ] Reinstall opencv-python:
   ```powershell
   pip install --upgrade opencv-python
   ```
3. [ ] Try specific version:
   ```powershell
   pip install opencv-python==4.8.0.76
   ```
4. [ ] Check pip is for correct Python:
   ```powershell
   pip --version  # Should mention your Python version
   ```

---

### Scanner Crashes on Start

**Steps to resolve**:
1. [ ] Check Python version: `python --version` (must be 3.11+)
2. [ ] Verify dependencies:
   ```powershell
   pip install -r requirements_kinect_scanner.txt --force-reinstall
   ```
3. [ ] Run with verbose output:
   ```powershell
   python -u kinect_scanner.py
   ```
4. [ ] Check permissions: Run PowerShell as Administrator
5. [ ] Restart computer and try again

---

### Black Screen / No Camera Feed

**Steps to resolve**:
1. [ ] Close other camera applications (Skype, Zoom, etc.)
2. [ ] Unplug and replug Kinect
3. [ ] Wait 30 seconds for initialization
4. [ ] Try different USB port
5. [ ] Check Kinect has external power
6. [ ] Verify driver installation
7. [ ] Restart computer

---

### Slow Performance / Dropped Frames

**Steps to improve**:
1. [ ] Close unnecessary applications
2. [ ] Use USB 2.0 port instead of USB 3.0
3. [ ] Ensure Kinect has dedicated USB port (not hub)
4. [ ] Check system resources:
   - [ ] Task Manager → Performance
   - [ ] Should have <80% CPU usage at idle
5. [ ] Increase capture interval:
   ```
   >>> a 20  (instead of a 30)
   ```

---

## Final Verification Checklist

**Before declaring setup complete**, verify ALL of these:

- [ ] `python --version` shows 3.11 or higher
- [ ] Device Manager shows "Kinect" under Cameras
- [ ] Kinect LED is GREEN (not red)
- [ ] `test_kinect_v1.py` runs without errors
- [ ] Can start scanner: `python kinect_scanner.py`
- [ ] Can capture photos: type `c`
- [ ] Photos saved to `data/captured/`
- [ ] `manifest.json` created
- [ ] Scanner can quit cleanly: type `q`
- [ ] External USB storage working (if needed)

**If ALL items checked**: ✓ **SETUP COMPLETE - READY FOR SCANNING**

---

## Quick Reference Commands

```powershell
# Check Python version
python --version

# Check installed packages
pip list

# Install dependencies
pip install -r requirements_kinect_scanner.txt

# Run hardware test
python test_kinect_v1.py

# Start scanner - Option 1 (Batch)
run_kinect_scanner.bat

# Start scanner - Option 2 (PowerShell)
.\run_kinect_scanner.ps1

# Start scanner - Option 3 (Direct)
python kinect_scanner.py

# Update specific package
pip install --upgrade opencv-python
```

---

## Support Resources

| Document | Location | Purpose |
|----------|----------|---------|
| Setup Guide | `docs/KINECT_TARGET_PC_SETUP.md` | Complete Windows 11 setup |
| API Reference | `docs/API_REFERENCE.md` | Python API documentation |
| Integration | `docs/KINECT_V1_INTEGRATION.md` | Technical details |
| Troubleshooting | `KINECT_V1_LIBUSBK_TROUBLESHOOTING.md` | Advanced troubleshooting |
| Quick Start | `KINECT_V1_QUICK_START.md` | Quick reference |

---

## Success Criteria

Your setup is **COMPLETE** when:

1. ✓ All Phase 1 system software installed
2. ✓ All Phase 2 JScaner files downloaded and dependencies installed
3. ✓ Phase 3 hardware testing passes
4. ✓ Phase 4 scanner starts and captures images
5. ✓ Images successfully saved to `data/captured/`
6. ✓ Manifest files created
7. ✓ Can successfully quit and restart scanner

---

## Support Contact

If setup fails:

1. Review this checklist step-by-step
2. Check troubleshooting section
3. Review documentation files
4. Verify hardware is functional
5. Contact technical support with:
   - Output from `python test_kinect_v1.py`
   - Output from `python kinect_scanner.py`
   - Your Windows version
   - Your Python version

---

**Setup Date**: _______________  
**Completed By**: _______________  
**Status**: ☐ Complete | ☐ Partial | ☐ Incomplete

**Notes**: _____________________________________________________________________________

---

**Last Updated**: December 29, 2025  
**Document Version**: 1.0
