# 🎯 Transfer Project to Target PC - Quick Guide

**Purpose**: Move JScaner Kinect Scanner project to your image capture PC

---

## ✅ What You Need

- **USB Drive** (8GB+) OR cloud storage link
- **Target PC** with Windows 10/11 and USB ports
- **~15 minutes** for transfer + setup

---

## 📦 Option 1: Using ZIP File (Fastest)

### Send to Target PC:
1. Copy `Kinect_Scanner_Deployment.zip` to USB or email
2. On target PC, extract the ZIP file
3. Open extracted folder
4. Double-click `AUTOMATED_SETUP.bat` (Run as Admin)
5. Wait ~10 minutes for auto-setup
6. Scanner launches automatically!

**File size**: ~30 KB (compressed)

---

## 📂 Option 2: Using Full Project Folder

### Send to Target PC:
1. Copy entire `3dscaning` folder to USB drive
2. On target PC, paste in desired location
3. Open PowerShell in the folder
4. Run:
   ```powershell
   pip install -r requirements_kinect_scanner.txt
   python kinect_scanner_gui.py
   ```

**Folder size**: ~2 GB (with git history) or ~500 MB (without .git)

---

## 📍 How to Reduce Transfer Size

### To send only essentials (~50 MB):
Delete these BEFORE transferring:
- `.git/` folder (repo history)
- `captured/` folder (old scans)
- `debug_grid_detection_*.jpg` files
- `data/` folder (example data)
- All `.md` files except: `README.md`, `START_HERE_KINECT_SCANNER.md`

---

## 🚀 For Development Work (Full Source Code)

If target PC needs to modify source code:
1. Send full project folder (option 2)
2. Include all files in `src/` directory
3. Include `.github/` for documentation standards
4. Include all test files from `tests/`

---

## 💻 What Target PC Needs Installed First

### Before running scanner:
1. **Python 3.11+** - https://www.python.org/downloads/
2. **Visual C++ 2015-2022** - https://support.microsoft.com/help/2977003
3. **Kinect v1 Drivers** - Use: `REQUIRED_PROGRAMS_LIST.md`

*Note: `AUTOMATED_SETUP.bat` will handle this if files aren't found*

---

## ✅ Verification Checklist

On target PC after setup:
- [ ] Python installed: `python --version`
- [ ] Kinect detected: `python test_kinect_v1.py`
- [ ] GUI launches: `python kinect_scanner_gui.py`
- [ ] Camera preview shows live feed

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Kinect not found" | Run `test_kinect_v1.py`, check USB connection |
| "Python not found" | Run `AUTOMATED_SETUP.bat` or install Python manually |
| GUI won't launch | Verify: `python -m tkinter` |

**For more help**: See `KINECT_SCANNER_SETUP_CHECKLIST.md`

