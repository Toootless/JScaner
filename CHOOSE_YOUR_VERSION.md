# Kinect Scanner - GUI vs CLI Comparison

## Quick Choice Guide

### 👍 Choose **GUI Version** if you:
- Want visual feedback
- Prefer clicking buttons to typing commands
- Are not technical
- Want live camera preview
- Like real-time progress indicators
- Need intuitive interface

### 👍 Choose **CLI Version** if you:
- Want scripting/automation
- Prefer command-line
- Are technical user
- Need batch processing scripts
- Want lightweight interface
- Like text-based feedback

---

## Both Versions Available

### GUI Version
```
Launch: run_kinect_scanner_gui.bat
What you see: Window with live preview + buttons
```

### CLI Version
```
Launch: run_kinect_scanner.bat
What you see: Text menu with commands
```

---

## Feature Comparison

| Feature | GUI | CLI |
|---------|-----|-----|
| **Live Preview** | ✓ Real-time video | ✓ Text display |
| **Single Capture** | Button click | `c` command |
| **Batch Capture** | Button + settings | `a` command |
| **Interface** | Windows GUI | Text menu |
| **Dependencies** | 4 packages | 4 packages |
| **File Size** | ~17 KB | ~13 KB |
| **Learning Curve** | Easy (5 minutes) | Medium (15 minutes) |
| **Speed** | Fast | Fast |
| **Automation** | ✓ Batch mode | ✓ Full scripting |
| **Mobile Touch** | ✓ Touch friendly | ✗ Not touch friendly |

---

## Typical Workflows

### Workflow 1: One-Off Scan
```
GUI: Open → Wait → Click Button → Done
CLI: Open → Wait → Type 'c' → Done
(GUI is slightly easier)
```

### Workflow 2: 360° Product Scan (12 images)
```
GUI:
  1. Set Count = 12
  2. Set Interval = 1.0
  3. Click Start
  4. Rotate object 12 times
  5. Done

CLI:
  1. Type 'a' for auto-capture
  2. Enter 12 for count
  3. Enter 1.0 for interval
  4. Rotate object 12 times
  5. Done

(Similar effort, GUI is more visual)
```

### Workflow 3: Rapid Continuous Capture
```
GUI:
  1. Set Count = 100
  2. Set Interval = 0.2
  3. Click Start
  4. Watch progress
  5. Stop when done

CLI:
  1. Type 'a'
  2. Enter 100
  3. Enter 0.2
  4. Type 's' to stop
  5. Done

(CLI is faster for power users)
```

### Workflow 4: Automated Nightly Batch
```
GUI: Not ideal - requires manual interaction

CLI: Perfect with script:
  python -c "
  from kinect_scanner import KinectScanner
  scanner = KinectScanner()
  scanner.connect()
  scanner.auto_capture_sequence(50, 0.5)
  scanner.export_manifest()
  "
  (Can schedule this in Windows Task Scheduler)
```

---

## Installation (Both Versions)

Both versions use the **same** launcher files:

### GUI
- `run_kinect_scanner_gui.bat`
- `run_kinect_scanner_gui.ps1`
- `kinect_scanner_gui.py`

### CLI
- `run_kinect_scanner.bat`
- `run_kinect_scanner.ps1`
- `kinect_scanner.py`

**AUTOMATED_SETUP.bat installs both automatically!**

---

## Starting Out (Recommendation)

### If you're **completely new**:
```
Start with: GUI Version
Reason: Visual feedback helps learning
Time: Open → 5 minutes
```

### If you're **comfortable with terminal**:
```
Try: CLI Version
Reason: More direct, scriptable
Time: Open → 3 minutes
```

### Ideal: **Try both!**
```
GUI for learning + interactive
CLI for production + automation
```

---

## File Organization

```
Project/
├── 🎨 GUI VERSION
│   ├── kinect_scanner_gui.py                (Application)
│   ├── run_kinect_scanner_gui.bat           (Launcher)
│   ├── run_kinect_scanner_gui.ps1           (Alt launcher)
│   ├── KINECT_SCANNER_GUI_GUIDE.md          (Full docs)
│   ├── KINECT_SCANNER_GUI_QUICK_START.md    (Quick start)
│   ├── GUI_VERSION_SUMMARY.md               (Summary)
│   └── GUI_VISUAL_REFERENCE.md              (UI guide)
│
├── 💻 CLI VERSION
│   ├── kinect_scanner.py                    (Application)
│   ├── run_kinect_scanner.bat               (Launcher)
│   ├── run_kinect_scanner.ps1               (Alt launcher)
│   ├── QUICK_START_KINECT_SCANNER.md        (Quick start)
│   └── KINECT_SCANNER_SETUP_CHECKLIST.md    (Setup guide)
│
├── ⚙️  SHARED
│   ├── test_kinect_v1.py                    (Hardware test)
│   ├── requirements_kinect_scanner.txt      (Dependencies)
│   ├── AUTOMATED_SETUP.bat                  (Full install)
│   └── data/captured/                       (Image storage)
```

---

## First Time Setup

### Step 1: Download & Extract
```
Kinect_Scanner_Deployment.zip → Extract to folder
```

### Step 2: Run Setup
```
Double-click: AUTOMATED_SETUP.bat
Wait: ~5-10 minutes
Result: Everything installed automatically
```

### Step 3: Choose Your Version
```
Option A: run_kinect_scanner_gui.bat      (Visual/Easy)
Option B: run_kinect_scanner.bat          (Text/Power)
```

### Step 4: Start Capturing!

---

## Video Tutorials (Recommended)

*To be created:*
- [ ] GUI Version - 3 minute tour
- [ ] CLI Version - 3 minute tour
- [ ] 360° Product Scan - 5 minute tutorial
- [ ] Batch Processing - 5 minute guide

---

## Troubleshooting by Version

### GUI Issues
- **Preview not showing**: Wait 3 sec, restart app
- **Can't click buttons**: Camera still initializing
- **Button disabled**: Batch operation in progress

### CLI Issues
- **Commands not working**: Check menu (press 'h')
- **No status output**: Normal - press any key for menu
- **Batch not starting**: Check count/interval values

---

## Advanced Usage

### Power Users: Auto-Deploy Both Versions
```batch
:: Install both automatically
AUTOMATED_SETUP.bat

:: Create shortcuts for both
mklink "GUI Scanner.lnk" run_kinect_scanner_gui.bat
mklink "CLI Scanner.lnk" run_kinect_scanner.bat

:: Both ready to use!
```

### Developers: Custom Scripts
```python
# Use CLI version for scripting
from kinect_scanner import KinectScanner

scanner = KinectScanner()
scanner.connect()
scanner.auto_capture_sequence(20, 0.5)  # 20 images, 0.5s apart
scanner.export_manifest()
```

---

## Migration Path

If you already have **CLI Version**:

1. Keep existing `kinect_scanner.py`
2. Add new `kinect_scanner_gui.py`
3. Add new launchers
4. Both work side-by-side

**No conflicts!** Both versions use same data folder.

---

## Support & Help

### GUI Questions?
→ See `KINECT_SCANNER_GUI_QUICK_START.md`
→ See `KINECT_SCANNER_GUI_GUIDE.md`

### CLI Questions?
→ See `QUICK_START_KINECT_SCANNER.md`
→ See `KINECT_SCANNER_SETUP_CHECKLIST.md`

### Hardware Issues?
→ Run `test_kinect_v1.py`
→ See `KINECT_SETUP.md`

---

## Summary

| Need | Solution |
|------|----------|
| First time? | Start with GUI |
| Like buttons? | Use GUI |
| Like commands? | Use CLI |
| Need both? | Install both! |
| Want automation? | Use CLI |
| Want visual? | Use GUI |
| Production use? | Try both, pick favorite |

---

**Version**: 2.0 (Both GUI + CLI)
**Status**: Production Ready ✓
**Date**: December 2025

Choose your version and start scanning!
