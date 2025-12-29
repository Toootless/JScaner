# Kinect v1 Scanner - READ THIS FIRST

**Welcome!** This is a complete Kinect v1 (Xbox 360) scanning system for Windows 11.

---

## ⚡ TL;DR - 25 Minutes to Scanning

```
1. Install: Python 3.11+ (check "Add to PATH")
2. Install: Visual C++ Redistributable
3. Install: Kinect Drivers
4. Restart computer
5. Run: pip install -r requirements_kinect_scanner.txt
6. Run: python kinect_scanner.py
7. Type: a 25 (capture 25 photos)
8. Done! Photos in data/captured/
```

---

## 📚 Which Document Should I Read?

### 🟢 I want to START NOW (5 minutes)
**Read**: [QUICK_START_KINECT_SCANNER.md](QUICK_START_KINECT_SCANNER.md)

### 🟡 I need detailed SETUP instructions (30 minutes)
**Read**: [KINECT_SCANNER_SETUP_CHECKLIST.md](KINECT_SCANNER_SETUP_CHECKLIST.md)

### 🔵 I need to know what PROGRAMS to download (10 minutes)
**Read**: [REQUIRED_PROGRAMS_LIST.md](REQUIRED_PROGRAMS_LIST.md)

### 🟣 I want to understand EVERYTHING (60 minutes)
**Read**: [KINECT_SCANNER_PROGRAM_SUMMARY.md](KINECT_SCANNER_PROGRAM_SUMMARY.md)

### ⚫ I need HELP NAVIGATING these docs
**Read**: [KINECT_SCANNER_DOCUMENTATION_INDEX.md](KINECT_SCANNER_DOCUMENTATION_INDEX.md)

---

## 🎯 3 Programs You Need

| Program | Get From | Size | Install |
|---------|----------|------|---------|
| **Python 3.11+** | https://www.python.org/downloads | 25 MB | ✓ Add to PATH |
| **Visual C++ 2015-2022** | https://support.microsoft.com/help/2977003 | 20 MB | ✓ Click Install |
| **Kinect Drivers** | https://www.microsoft.com/download/details.aspx?id=34808 | 30 MB | ✓ Restart after |

**Then**: `pip install -r requirements_kinect_scanner.txt`

---

## 🎬 First Run

```powershell
# Navigate to this folder
cd C:\path\to\JScaner

# Start scanner
python kinect_scanner.py

# At the >>> prompt, try:
h              # Show help
i              # Camera info
c              # Capture one photo
a 10           # Capture 10 photos
s              # Save list
q              # Quit
```

---

## 📁 What's Included

```
📦 Files Ready to Use:
├── kinect_scanner.py           ← Main program
├── run_kinect_scanner.bat      ← Click to run (Windows)
├── test_kinect_v1.py           ← Test hardware
└── requirements_kinect_scanner.txt ← Dependencies

📚 Documentation:
├── QUICK_START_KINECT_SCANNER.md       ← Start here!
├── REQUIRED_PROGRAMS_LIST.md           ← Download list
├── KINECT_SCANNER_SETUP_CHECKLIST.md   ← Step-by-step
├── docs/KINECT_TARGET_PC_SETUP.md      ← Detailed guide
├── KINECT_SCANNER_PROGRAM_SUMMARY.md   ← Full reference
└── KINECT_SCANNER_DOCUMENTATION_INDEX.md ← Navigation
```

---

## ✅ What This Program Does

✅ Captures images from Kinect v1 (Xbox 360)  
✅ Saves images as JPEG files  
✅ Tracks metadata for each image  
✅ Creates manifest of all captures  
✅ Exports data for JScaner processing  
✅ 640x480 resolution at 30 FPS  
✅ Batch capture mode (20+ images per session)  

---

## 🆘 Something Not Working?

### Kinect not found
1. Check Device Manager for "Kinect"
2. Verify USB cable connected
3. Check LED is GREEN (not red)
4. Try different USB port
5. Restart computer
6. Reinstall drivers

### Python errors
1. Check: `python --version` (must be 3.11+)
2. Try: `pip install --upgrade opencv-python`
3. Or: `pip install -r requirements_kinect_scanner.txt --force-reinstall`

### Still stuck?
1. See: [KINECT_SCANNER_SETUP_CHECKLIST.md](KINECT_SCANNER_SETUP_CHECKLIST.md) Troubleshooting
2. Or: [docs/KINECT_TARGET_PC_SETUP.md](docs/KINECT_TARGET_PC_SETUP.md) Troubleshooting

---

## 🚀 Quick Reference

```powershell
# Check system ready
python --version          # Should be 3.11+
pip list                  # Should show opencv-python

# Test hardware
python test_kinect_v1.py  # Should show ✓ Device found

# Run scanner
python kinect_scanner.py  # Should start without errors

# In scanner (>>> prompt):
h     - Help
c     - Capture one photo
a 25  - Capture 25 photos
i     - Camera info
s     - Save manifest
q     - Quit
```

---

## 💾 Where Images Are Saved

After capturing, find your images here:
```
data/captured/
├── scan_20250101_120000_001.jpg
├── scan_20250101_120000_001_metadata.json
├── scan_20250101_120101_002.jpg
├── ...
└── manifest.json
```

---

## 🎓 Learning Path

**Beginner** (Just want to use it)
1. Read: QUICK_START_KINECT_SCANNER.md
2. Install programs (3 of them)
3. Run: python kinect_scanner.py
4. Done!

**Intermediate** (Want to understand)
1. Read: KINECT_SCANNER_SETUP_CHECKLIST.md
2. Follow all 5 phases
3. Read: KINECT_SCANNER_PROGRAM_SUMMARY.md
4. Ready for production

**Advanced** (Want deep knowledge)
1. Read all documentation
2. Study: docs/KINECT_V1_INTEGRATION.md
3. Review: kinect_scanner.py source code
4. Customize for your needs

---

## 📊 Specifications

| Feature | Spec |
|---------|------|
| Camera | Kinect v1 (Xbox 360) |
| Resolution | 640x480 RGB |
| Frame Rate | Up to 30 FPS |
| OS | Windows 11 (Windows 10 OK) |
| Python | 3.11+ |
| Setup Time | 25-30 minutes |
| Disk Space | 5 GB minimum |
| RAM | 4 GB minimum |

---

## 🎯 What Happens After Scanning?

1. **Capture Phase**: Use this program to capture 20-30 images
2. **Transfer Phase**: Copy `data/captured/` folder to processing PC
3. **Processing Phase**: Load images in main JScaner GUI
4. **Export Phase**: Generate STL files for 3D printing

---

## 📞 Quick Support

**Q: Python not found?**
A: Reinstall Python with "Add to PATH" checked. Restart.

**Q: Kinect won't start?**
A: LED should be GREEN. Check USB cable. Try different port.

**Q: Can't install packages?**
A: Run: `pip install --upgrade pip`
Then: `pip install -r requirements_kinect_scanner.txt`

**Q: More help?**
A: See [KINECT_SCANNER_SETUP_CHECKLIST.md](KINECT_SCANNER_SETUP_CHECKLIST.md)

---

## 🏁 Start Here

1. **Pick your speed**:
   - Fast: [QUICK_START_KINECT_SCANNER.md](QUICK_START_KINECT_SCANNER.md)
   - Thorough: [KINECT_SCANNER_SETUP_CHECKLIST.md](KINECT_SCANNER_SETUP_CHECKLIST.md)
   - Complete: [KINECT_SCANNER_PROGRAM_SUMMARY.md](KINECT_SCANNER_PROGRAM_SUMMARY.md)

2. **Get the 3 programs**: [REQUIRED_PROGRAMS_LIST.md](REQUIRED_PROGRAMS_LIST.md)

3. **Follow the guide** for your speed level

4. **Start scanning!** 🎉

---

## ✨ Key Features

- 🎬 Live Kinect camera preview
- 📸 Single and batch capture modes
- 📊 Automatic metadata tracking
- 📁 Organized file management
- 📋 Manifest export for processing
- 🔧 Easy troubleshooting
- 📚 Comprehensive documentation
- 🚀 Production ready

---

## Version Info

- **Program**: JScaner Kinect v1 Scanner v1.0
- **Created**: December 29, 2025
- **Status**: Production Ready ✅
- **Support**: Full documentation included

---

**Ready? Start with [QUICK_START_KINECT_SCANNER.md](QUICK_START_KINECT_SCANNER.md)**

*25 minutes from now, you'll be scanning! 📸*
