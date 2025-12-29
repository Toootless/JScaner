# Target PC Programs & Requirements List

**For Windows 11 Kinect Scanner System**  
**Date: December 29, 2025**

---

## Complete Software Requirements List

This document provides a single, definitive list of ALL programs and packages needed to run the Kinect v1 Scanner on a Windows 11 target PC.

---

## Installation Priority Order

### ⚠️ CRITICAL - Must Install First

| Program | Version | Download Link | Purpose |
|---------|---------|---------------|---------|
| **Python** | 3.11 or higher | https://www.python.org/downloads/ | Runtime environment |
| **Visual C++ Redistributable** | 2015-2022 | https://support.microsoft.com/help/2977003 | Library support |
| **Kinect v1 Drivers** | Latest | https://www.microsoft.com/download/details.aspx?id=34808 | Hardware driver |

**Installation Steps**:
1. Install Python (check "Add to PATH")
2. Install Visual C++
3. Install Kinect Drivers
4. **Restart Computer**

---

## Python Packages (Automatically Installed)

These are installed automatically when you run:
```powershell
pip install -r requirements_kinect_scanner.txt
```

| Package | Version | Size | Purpose |
|---------|---------|------|---------|
| opencv-python | 4.8.0+ | ~30 MB | Camera capture |
| numpy | 1.24.0+ | ~10 MB | Numerical processing |
| Pillow | 10.0.0+ | ~2 MB | Image formats |
| tqdm | 4.65.0+ | <1 MB | Progress bars |

**Total Python Package Size**: ~50 MB

---

## Optional Programs (Recommended But Not Required)

| Program | Version | Download Link | Purpose |
|---------|---------|---------------|---------|
| **Git for Windows** | Latest | https://git-scm.com/download/win | Clone project |
| **Visual Studio Code** | Latest | https://code.visualstudio.com/ | Edit files |
| **7-Zip** | Latest | https://www.7-zip.org/ | Extract archives |

**Use Case**:
- Git: If cloning from GitHub repository
- VS Code: For editing configuration files
- 7-Zip: For extracting downloaded files

---

## Storage Requirements

### Minimum Space
- Python 3.11: ~100 MB
- Kinect Drivers: ~200 MB
- Visual C++: ~500 MB
- Python Packages: ~50 MB
- **Project Files**: ~10 MB
- **For Captures**: Variable (25 MB per 100 images)

**Total Minimum**: 5 GB free space recommended

### Recommended Space
- All above: 1 GB for software
- **Capture Storage**: 20 GB minimum for capturing
- **Backups**: 20 GB external storage

**Total Recommended**: 50+ GB total storage, 20+ GB free

---

## Internet Bandwidth

| Component | Size | Speed Impact |
|-----------|------|--------------|
| Python installer | 25 MB | ~5 minutes at 1 Mbps |
| Visual C++ | 20 MB | ~4 minutes at 1 Mbps |
| Kinect drivers | 30 MB | ~6 minutes at 1 Mbps |
| Python packages (pip) | 50 MB | ~10 minutes at 1 Mbps |
| Project files (git clone) | 10 MB | ~2 minutes at 1 Mbps |

**Total Download**: ~135 MB  
**Total Time** (1 Mbps): ~30 minutes

---

## Hardware Requirements

### CPU (Processor)
- **Minimum**: Intel i5 (8th Gen) or AMD Ryzen 5 2600
- **Recommended**: Intel i7 (10th Gen+) or AMD Ryzen 7 3000+
- **Performance Need**: 2+ cores minimum, 4+ cores recommended

### RAM (Memory)
- **Minimum**: 4 GB
- **Recommended**: 8 GB
- **Performance Note**: Scanning only uses 200-400 MB

### Storage
- **Minimum**: 5 GB free space
- **Recommended**: 20 GB free space
- **Type**: HDD acceptable, SSD better for speed

### USB Ports
- **Required**: 1x USB 2.0 or 3.0 port
- **Recommendation**: Use USB 2.0 for better Kinect stability
- **Note**: Direct connection (no hubs)

### Display
- **Minimum**: 1024x768
- **Recommended**: 1920x1080 or higher
- **Purpose**: Scanning uses terminal only, display just for monitoring

### Network
- **Internet**: Required only for initial setup/downloads
- **During Scanning**: Not required
- **For Transfer**: Optional (can use USB drive)

---

## Kinect v1 Hardware Specifications

### Physical Requirements
- **Device**: Xbox 360 Kinect (also called Kinect v1)
- **Connection**: USB Type-A
- **Power**: External power supply (included with device)
- **Cable Length**: 1.5 meters USB cable + separate power

### Specifications
- **Resolution**: 640x480 RGB
- **Frame Rate**: 30 FPS
- **Color Depth**: 8-bit RGB (24-bit)
- **Autofocus**: Yes (important for grid detection)
- **Field of View**: 58° horizontal, 45° vertical

### Required Accessories
- [ ] Kinect v1 unit
- [ ] USB cable (Type A to proprietary connector)
- [ ] Power supply (100-240V, typically 5V 2A)
- [ ] Wall outlet or power strip

---

## Windows 11 Specific Requirements

| Component | Version | Status |
|-----------|---------|--------|
| OS | Windows 11 (any edition) | ✓ Required |
| Build | Latest (recommended) | ✓ Recommended |
| Architecture | x64 (64-bit) | ✓ Required |
| Drivers | Latest Windows Updates | ✓ Recommended |

**Verify Windows Version**:
```powershell
winver  # Run this to check your version
```

**Update Windows**:
```
Settings → Update & Security → Windows Update → Check for updates
```

---

## Python Version Support Matrix

| Python Version | Scanner | Full JScaner | Status |
|----------------|---------|--------------|--------|
| 3.11 | ✓ | ✓ | Fully Supported |
| 3.12 | ✓ | ✓ | Fully Supported |
| 3.13 | ✓ | ✓ | Fully Supported |
| 3.14 | ✓ | ✓ | Supported |
| 3.10 | ✗ | ✓ | Not Supported |

**Recommendation**: Use Python 3.12 for best compatibility

---

## Driver Requirements Detail

### Kinect v1 Drivers

**Option 1: Official Microsoft (Recommended)**
- Name: "Kinect for Windows Runtime v1.8"
- Source: Microsoft Download Center
- Size: ~30 MB
- Installation Time: 5 minutes
- Restart Required: Yes

**Option 2: Windows Auto-Driver (Fallback)**
- Method: Device Manager → Update Driver
- Time: 10-15 minutes
- Restart Required: Yes
- Reliability: Good for basic operation

**Option 3: LibUSBK (Advanced)**
- Use if Options 1-2 fail
- Requires vcpkg installation
- See: docs/KINECT_V1_LIBUSBK_SETUP.md
- Complex setup - avoid if possible

### Visual C++ Redistributable

**Version**: Visual Studio 2015-2022 Redistributable  
**Architecture**: x64 (for 64-bit Windows)  
**Size**: ~20 MB  
**Installation Time**: 2 minutes  
**Restart Required**: Yes (usually)

---

## Complete Installation Command Reference

### Windows PowerShell Commands (Copy & Paste)

```powershell
# Step 1: Verify Python
python --version

# Step 2: Verify pip
pip --version

# Step 3: Install requirements
pip install -r requirements_kinect_scanner.txt

# Step 4: Verify installation
pip list

# Step 5: Test hardware
python test_kinect_v1.py

# Step 6: Start scanner
python kinect_scanner.py
```

---

## Pre-Installation Checklist

Before beginning installation, verify you have:

**Hardware**
- [ ] Windows 11 PC ready
- [ ] Administrator account access
- [ ] Kinect v1 device
- [ ] Kinect power supply
- [ ] Available USB port
- [ ] Internet connection

**Access**
- [ ] Can access download websites
- [ ] Can install software (Admin rights)
- [ ] Can restart computer if needed
- [ ] 30 minutes of uninterrupted time

**Files**
- [ ] Know where to download files
- [ ] Know where to save project
- [ ] Have storage space available

---

## Bandwidth & Storage Summary Table

| Download | Size | Time (1 Mbps) |
|----------|------|---------------|
| Python installer | 25 MB | 3 min |
| Visual C++ | 20 MB | 2.5 min |
| Kinect drivers | 30 MB | 4 min |
| OpenCV (pip) | 30 MB | 4 min |
| NumPy (pip) | 10 MB | 1.3 min |
| Other packages (pip) | 10 MB | 1.3 min |
| Project files | 10 MB | 1.3 min |
| **TOTAL** | **135 MB** | **~17 min** |

**Note**: Times vary by internet speed. 10 Mbps connection = ~1.7 minutes total.

---

## Programs Needed - Quick Reference

### Essential (Installation Order)

1. **Python 3.11+**
   - Get from: python.org
   - Install to: Default location
   - Action: Add to PATH

2. **Visual C++ 2015-2022 Redistributable**
   - Get from: microsoft.com
   - Install to: Default location
   - Restart: Required

3. **Kinect v1 Drivers**
   - Get from: microsoft.com (or Device Manager)
   - Install to: System drivers
   - Restart: Required

### Automatic (via pip)

```powershell
pip install -r requirements_kinect_scanner.txt
```

Installs:
- opencv-python
- numpy
- Pillow
- tqdm

### Optional

- Git (for cloning project)
- Visual Studio Code (for editing)
- 7-Zip (for file extraction)

---

## Troubleshooting Programs

If installation fails, you may need:

| Symptom | Solution | Program |
|---------|----------|---------|
| "Python not found" | Add Python to PATH | Python installer |
| Missing DLL files | Install Visual C++ | Visual C++ installer |
| Camera not recognized | Reinstall drivers | Kinect drivers |
| pip not working | Reinstall Python | Python installer |
| Can't extract files | Install 7-Zip | 7-Zip |

---

## System Cleanup After Setup

**After successful setup**, you can delete:
- [ ] Python installer (.exe file)
- [ ] Visual C++ installer (.exe file)
- [ ] Kinect driver installer (.exe file)
- [ ] Downloaded .zip files

**Keep**: Project folder and virtual environment

---

## Support Resources

| Issue | Document |
|-------|----------|
| Can't install Python | docs/KINECT_TARGET_PC_SETUP.md → Phase 1 |
| Driver problems | docs/KINECT_V1_LIBUSBK_SETUP.md |
| Package installation fails | KINECT_SCANNER_SETUP_CHECKLIST.md → Troubleshooting |
| Hardware not detected | KINECT_V1_QUICK_START.md |

---

## Final Verification

After installation, verify:

```powershell
# Check Python
python --version           # Should show 3.11+

# Check packages
pip list                   # Should show opencv, numpy, etc

# Check Kinect
python test_kinect_v1.py   # Should show device found

# Check Scanner
python kinect_scanner.py   # Should start successfully
```

---

## Complete Programs & Requirements Summary

**TOTAL PROGRAMS NEEDED**: 3 Essential + 4 Python Packages (automatic)

**TOTAL DOWNLOAD SIZE**: ~135 MB  
**TOTAL INSTALL TIME**: 20-30 minutes  
**TOTAL STORAGE NEEDED**: 5 GB minimum  
**RESTART REQUIRED**: Yes (after drivers)

---

## One-Liner Summary

**Install**: Python 3.11+ → Visual C++ 2015-2022 → Kinect Drivers → `pip install -r requirements_kinect_scanner.txt` → Done!

---

**Next Step**: Follow KINECT_SCANNER_SETUP_CHECKLIST.md for step-by-step installation

---

**Document Version**: 1.0  
**Last Updated**: December 29, 2025  
**Target OS**: Windows 11 (Windows 10 also works)
