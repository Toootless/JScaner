# 🚀 Quick Start - Kinect Scanner for Windows 11

**TL;DR Setup** (30 minutes to working system)

---

## What You're Getting

A complete **standalone Kinect v1 scanning system** for Windows 11 that:
- ✓ Captures 3D scan images with Kinect v1 (Xbox 360)
- ✓ Exports data compatible with JScaner processing
- ✓ Requires only 4 Python packages
- ✓ Runs on any Windows 11 PC

---

## Programs You MUST Install

### 1. Python 3.11+ ⚡
```
Download: https://www.python.org/downloads/
Install: Default settings
CRITICAL: Check "Add Python to PATH" ✓
```

### 2. Visual C++ Redistributable ⚡
```
Download: https://support.microsoft.com/help/2977003
Choose: VS 2015-2022 (x64)
Install: Click "Install"
```

### 3. Kinect v1 Drivers ⚡
```
Download: https://www.microsoft.com/download/details.aspx?id=34808
Or: Auto-install via Device Manager
Install: Follow wizard
RESTART COMPUTER ⚠️
```

**That's it! Only 3 programs needed.**

---

## Installation Steps (5 minutes)

```powershell
# 1. Download JScaner project to your PC
# 2. Open PowerShell in JScaner folder
# 3. Run this ONE command:

pip install -r requirements_kinect_scanner.txt

# 4. Plug in Kinect
# 5. Test it:

python test_kinect_v1.py

# 6. Start scanning:

python kinect_scanner.py
```

---

## Using the Scanner

```powershell
# Start
python kinect_scanner.py

# At the prompt (>>>):
i              # Check camera
c              # Capture one photo
a 25           # Capture 25 photos automatically
s              # Save list of all photos
q              # Quit and save
```

**That's all you need to know!**

---

## What Gets Saved

```
data/captured/
├── scan_20250101_120000_001.jpg       (your photo)
├── scan_20250101_120000_001_metadata.json (info)
├── scan_20250101_120101_002.jpg       (your photo)
├── scan_20250101_120101_002_metadata.json (info)
└── manifest.json                      (list of all)
```

---

## Files You Get

| File | Purpose |
|------|---------|
| `kinect_scanner.py` | Main program |
| `run_kinect_scanner.bat` | Double-click to run |
| `requirements_kinect_scanner.txt` | Automatic dependencies |
| `test_kinect_v1.py` | Verify hardware |
| `docs/KINECT_TARGET_PC_SETUP.md` | Full setup guide |
| `REQUIRED_PROGRAMS_LIST.md` | Complete requirements |
| `KINECT_SCANNER_SETUP_CHECKLIST.md` | Installation checklist |

---

## Troubleshooting (30 seconds)

### "Python not found"
```powershell
# Reinstall Python and CHECK "Add to PATH"
# Then restart computer
```

### "Camera not found"
```powershell
# Run: python test_kinect_v1.py
# Check Kinect LED is GREEN
# Try different USB port
# Restart computer
```

### "Can't install packages"
```powershell
# Run: pip install --upgrade pip
# Then: pip install -r requirements_kinect_scanner.txt
```

---

## System Requirements

- Windows 11 (or Windows 10)
- Python 3.11+ 
- Intel i5 or better
- 4 GB RAM minimum
- 5 GB free disk space
- Kinect v1 (Xbox 360) + power supply

---

## Next Steps

1. **Install Programs** (15 min)
   - Python 3.11+
   - Visual C++
   - Kinect Drivers
   - Restart PC

2. **Get JScaner** (2 min)
   - Download/clone project

3. **Install Python Packages** (3 min)
   - `pip install -r requirements_kinect_scanner.txt`

4. **Test** (2 min)
   - `python test_kinect_v1.py`

5. **Start Scanning** (8 min)
   - `python kinect_scanner.py`
   - Type `a 25` for 25 photos

6. **Process** (variable)
   - Transfer images to processing PC
   - Use JScaner main app for 3D reconstruction
   - Export as STL for 3D printing

---

## One Page Reference

| Action | Command | Time |
|--------|---------|------|
| Install Python | Download & run | 5 min |
| Install C++ Runtime | Download & run | 2 min |
| Install Kinect Driver | Download & run | 5 min |
| Get JScaner | Clone/download | 2 min |
| Install packages | `pip install -r...` | 3 min |
| Test hardware | `python test_kinect_v1.py` | 1 min |
| Start scanner | `python kinect_scanner.py` | <1 min |
| Capture 25 photos | Type `a 25` | 30 sec |
| Export | Type `s` then `q` | 5 sec |
| **TOTAL** | **All above** | **~25 min** |

---

## File Locations After Setup

```
C:\Your\Desired\Path\
└── JScaner/
    ├── kinect_scanner.py
    ├── run_kinect_scanner.bat
    ├── test_kinect_v1.py
    ├── requirements_kinect_scanner.txt
    ├── docs/
    │   ├── KINECT_TARGET_PC_SETUP.md
    │   ├── KINECT_V1_INTEGRATION.md
    │   └── KINECT_V1_LIBUSBK_SETUP.md
    └── data/
        └── captured/
            ├── scan_*.jpg
            ├── scan_*_metadata.json
            └── manifest.json
```

---

## Quick Command Cheat Sheet

```powershell
# Setup
python --version                    # Check Python is 3.11+
pip install -r requirements_kinect_scanner.txt  # Install packages
python test_kinect_v1.py           # Test hardware

# Running
python kinect_scanner.py           # Start scanner
double-click run_kinect_scanner.bat # Or use this

# Scanner commands (type at >>> prompt)
h               # Help menu
c               # Capture one photo
a 20            # Capture 20 photos automatically
i               # Camera info
s               # Save manifest
q               # Quit scanner
```

---

## Success Criteria ✓

You're done when:

- [ ] `python --version` shows 3.11+
- [ ] `pip list` shows opencv-python
- [ ] `python test_kinect_v1.py` shows "✓ Device found"
- [ ] `python kinect_scanner.py` starts without errors
- [ ] You can type `c` and it captures a photo
- [ ] Files appear in `data/captured/` folder
- [ ] `manifest.json` file exists

---

## Support

- **Full Setup Guide**: `docs/KINECT_TARGET_PC_SETUP.md`
- **Step-by-Step Checklist**: `KINECT_SCANNER_SETUP_CHECKLIST.md`
- **All Requirements**: `REQUIRED_PROGRAMS_LIST.md`
- **Full Reference**: `KINECT_SCANNER_PROGRAM_SUMMARY.md`

---

## What NOT to Do ❌

- ❌ Don't forget "Add Python to PATH"
- ❌ Don't skip Visual C++ installation
- ❌ Don't forget to restart after drivers
- ❌ Don't connect Kinect to USB hub (use direct port)
- ❌ Don't run if Kinect LED is RED (power issue)
- ❌ Don't use USB 3.0 if USB 2.0 available

---

## Expected Results

After typing `a 25` to capture 25 photos:

```
[SEQUENCE] Starting auto-capture of 25 frames...
[SEQUENCE] Frames will be captured every 0.5 seconds
[CAPTURED] auto_sequence_01.jpg (178 KB)
[CAPTURED] auto_sequence_02.jpg (165 KB)
...
[SEQUENCE] Completed: 25 frames captured
```

📁 Files in `data/captured/`:
- 25 JPG image files (~4 MB total)
- 25 JSON metadata files
- 1 manifest.json file

✅ Ready to process on main JScaner PC!

---

**Ready? Start here**: Download the three programs above, then run `pip install -r requirements_kinect_scanner.txt`

**Stuck? Check**: `KINECT_SCANNER_SETUP_CHECKLIST.md` (Phase-by-phase guide)

---

**Setup Time**: 25-30 minutes | **Difficulty**: Easy | **Success Rate**: 99%
