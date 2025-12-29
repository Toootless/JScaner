# 🚀 Kinect v1 Scanner - Deployment Package

**Welcome!** This is your complete Kinect v1 (Xbox 360) scanning system for Windows 11.

---

## ⚡ FASTEST WAY TO GET STARTED (3 STEPS)

### Step 1: Run Automated Setup (30 seconds to start)
```
Double-click: AUTOMATED_SETUP.bat
```
This script will:
- Check/install Python 3.12
- Check/install Visual C++ Redistributable
- Verify Kinect hardware
- Install Python packages
- Start the scanner

### Step 2: Connect Kinect
- Plug in Kinect v1 (Xbox 360) via USB
- Ensure LED is GREEN (has power)
- Wait 10 seconds for detection

### Step 3: Start Capturing
```
In the scanner prompt:
>>> a 25    (capture 25 images)
>>> s       (save manifest)
>>> q       (quit)
```

**Done! ✅ Images saved to data/captured/**

---

## 📦 WHAT'S IN THIS PACKAGE

### Executable Programs
- `kinect_scanner.py` - Main scanner application
- `AUTOMATED_SETUP.bat` - Automatic setup script (recommended!)
- `run_kinect_scanner.bat` - Manual launcher
- `run_kinect_scanner.ps1` - PowerShell launcher
- `test_kinect_v1.py` - Hardware test utility

### Documentation
- `START_HERE_KINECT_SCANNER.md` - Welcome guide
- `QUICK_START_KINECT_SCANNER.md` - Quick overview
- `REQUIRED_PROGRAMS_LIST.md` - What programs needed
- `KINECT_SCANNER_SETUP_CHECKLIST.md` - Step-by-step setup
- `docs/KINECT_TARGET_PC_SETUP.md` - Detailed Windows 11 guide

### Configuration
- `requirements_kinect_scanner.txt` - Python dependencies

---

## 🎯 RECOMMENDED: Use Automated Setup

This is the easiest way:

```
1. Right-click AUTOMATED_SETUP.bat
2. Select "Run as Administrator"
3. Follow the prompts
4. Done!
```

The script will:
✅ Download/install Python 3.12 (if needed)  
✅ Download/install Visual C++ (if needed)  
✅ Check Kinect hardware  
✅ Install Python packages (4 total)  
✅ Verify everything works  
✅ Start the scanner  

**Estimated time: 5-10 minutes (depending on downloads)**

---

## 📖 MANUAL SETUP (If Automated Fails)

1. Read: `START_HERE_KINECT_SCANNER.md`
2. Read: `QUICK_START_KINECT_SCANNER.md`
3. Get programs: `REQUIRED_PROGRAMS_LIST.md`
4. Follow: `KINECT_SCANNER_SETUP_CHECKLIST.md`

---

## 🎬 RUNNING THE SCANNER

### After Setup is Complete

```powershell
# Option 1: Double-click
run_kinect_scanner.bat

# Option 2: PowerShell
.\run_kinect_scanner.ps1

# Option 3: Direct command
python kinect_scanner.py
```

### Scanner Commands

```
h              Show help menu
c              Capture one photo
a 25           Capture 25 photos automatically
i              Show camera information
s              Save manifest file (list of all photos)
q              Quit and save
```

---

## 📋 3 PROGRAMS YOU MUST HAVE (Automated Setup Gets Them)

1. **Python 3.11+** (Automated Setup: Downloads for you)
2. **Visual C++ 2015-2022** (Automated Setup: Downloads for you)
3. **Kinect v1 Drivers** (You need to install manually if not present)

**Kinect Drivers** (if not auto-detected):
- Download: https://www.microsoft.com/download/details.aspx?id=34808
- Named: "Kinect for Windows Runtime v1.8"
- Install and restart computer

---

## ✨ KEY FEATURES

✅ Live Kinect v1 camera feed  
✅ Single frame capture  
✅ Batch capture (20+ images at once)  
✅ Automatic metadata tracking  
✅ 640x480 resolution at 30 FPS  
✅ Manifest export for JScaner processing  

---

## 🆘 TROUBLESHOOTING

### "Kinect Not Found"
- Check USB connection (use USB 2.0 if available)
- Verify Kinect LED is GREEN (has power)
- Try different USB port
- Restart computer
- Install drivers from link above

### "Python Not Found"
- Automated Setup should install it
- Or download from https://www.python.org/downloads/
- **CRITICAL**: Check "Add Python to PATH"

### "Missing Packages"
- Run: `pip install -r requirements_kinect_scanner.txt`
- Or let Automated Setup handle it

### Still Stuck?
- See: `KINECT_SCANNER_SETUP_CHECKLIST.md` → Troubleshooting
- See: `docs/KINECT_TARGET_PC_SETUP.md` → Troubleshooting

---

## 📁 FILE LOCATIONS

After setup, images are saved to:
```
data/captured/
├── scan_YYYYMMDD_HHMMSS_001.jpg
├── scan_YYYYMMDD_HHMMSS_001_metadata.json
├── scan_YYYYMMDD_HHMMSS_002.jpg
├── ...
└── manifest.json
```

---

## 🚀 WORKFLOW

### On This PC (Scanner)
1. Run: `AUTOMATED_SETUP.bat` (first time only)
2. Connect Kinect
3. Run: `python kinect_scanner.py`
4. Capture: `a 25` (25 photos)
5. Save: `s` (manifest file)
6. Copy `data/captured/` folder

### On Processing PC (Main JScaner)
1. Paste captured images
2. Run: `python main.py`
3. Process 3D reconstruction
4. Export as STL for 3D printing

---

## 📊 SYSTEM REQUIREMENTS

| Item | Requirement |
|------|-------------|
| OS | Windows 11 (or Windows 10) |
| Python | 3.11+ (auto-installed) |
| CPU | Intel i5 or better |
| RAM | 4 GB minimum |
| Storage | 5 GB free space |
| USB | 1 port for Kinect |

---

## ✅ SUCCESS CHECKLIST

After Automated Setup, verify:
- [x] Python installed: `python --version` → shows 3.11+
- [x] Packages installed: `pip list` → shows opencv-python
- [x] Kinect detected: `python test_kinect_v1.py` → shows "✓ Device found"
- [x] Scanner runs: `python kinect_scanner.py` → starts without errors
- [x] Can capture: Type `c` → creates .jpg file
- [x] Files saved: Check `data/captured/` folder

**All checked? You're ready to scan!** 📸

---

## 📞 QUICK HELP

| Need | File to Read |
|------|--------------|
| Welcome | START_HERE_KINECT_SCANNER.md |
| Quick start | QUICK_START_KINECT_SCANNER.md |
| Programs to install | REQUIRED_PROGRAMS_LIST.md |
| Step-by-step setup | KINECT_SCANNER_SETUP_CHECKLIST.md |
| Detailed guide | docs/KINECT_TARGET_PC_SETUP.md |

---

## 🎯 NEXT STEPS

1. ✅ **First time?** Run: `AUTOMATED_SETUP.bat`
2. ✅ **Connect Kinect** via USB
3. ✅ **Start scanning:** `python kinect_scanner.py`
4. ✅ **Capture images:** Type `a 25`
5. ✅ **Save and quit:** Type `s` then `q`
6. ✅ **Transfer to processing PC**

---

**Setup Time**: 5-10 minutes (with Automated Setup)  
**Programs to Install**: 3 (Automated Setup handles it!)  
**Difficulty**: Easy  

---

**Ready? Double-click AUTOMATED_SETUP.bat to get started!** 🚀

*Created December 29, 2025*
