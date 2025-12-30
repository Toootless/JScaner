# Kinect Not Detected - Quick Fix Guide

## Problem
The Kinect scanner program only detects your laptop webcam, not the Kinect.

## Diagnosis
✓ Kinect SDK v1.8 is installed  
✓ Kinect shows in Device Manager  
✗ Some Kinect devices show "Unknown" status  
✗ Kinect camera not accessible to applications  

## Solution

### STEP 1: Run Driver Fix (Automated)

Right-click `fix_kinect_drivers.ps1` → **Run as Administrator**

This will:
- Check Kinect device status
- Reset problematic devices
- Update drivers
- Report results

### STEP 2: Verify Fix

After running the fix script, test detection:

```powershell
python find_kinect_camera.py
```

**Expected result**: Should show 2 cameras
- Camera 0: Laptop webcam (640x480)
- Camera 1: Kinect camera (640x480 or higher)

### STEP 3: Update Scanner Configuration

If Kinect is detected as Camera 1, update the program:

**For GUI version** (`kinect_scanner_gui.py`):
- The GUI should auto-detect and show both cameras in the dropdown
- Select "Camera 1" from the dropdown menu

**For command-line version** (`kinect_scanner.py`):
Edit line ~44:
```python
# Change from:
camera_id = 0

# To:
camera_id = 1  # or whatever index find_kinect_camera.py reported
```

---

## If Automated Fix Doesn't Work

### Manual Fix Option 1: Driver Reinstall

1. **Open Device Manager** (Win+X → Device Manager)
2. Expand "Kinect for Windows"
3. For each device with yellow ⚠ or showing "Unknown":
   - Right-click → **Uninstall device**
   - ✓ Check "Delete the driver software for this device"
   - Click **Uninstall**
4. **Unplug Kinect USB cable**
5. **Restart computer**
6. **Plug in Kinect** - Windows should auto-install drivers
7. Run `python find_kinect_camera.py` again

### Manual Fix Option 2: Reinstall SDK

If driver reinstall doesn't work:

1. **Uninstall Kinect SDK**:
   - Settings → Apps → Kinect for Windows SDK v1.8 → Uninstall
2. **Restart computer**
3. **Download and reinstall** Kinect SDK v1.8:
   - https://www.microsoft.com/en-us/download/details.aspx?id=40278
4. **Plug in Kinect** after installation completes
5. Test with `python find_kinect_camera.py`

### Manual Fix Option 3: Try Different USB Port

- **Unplug Kinect** from current USB port
- **Try different USB port** (preferably USB 2.0 or powered USB 3.0)
- **Avoid USB hubs** - plug directly into computer
- Some laptops have power issues with Kinect on certain ports

---

## Verification Checklist

After applying fixes, verify:

- [ ] `python find_kinect_camera.py` shows multiple cameras
- [ ] Device Manager shows all Kinect devices with "OK" status
- [ ] Running `kinect_scanner_gui.py` shows Kinect in camera dropdown
- [ ] Preview window shows Kinect feed (not laptop webcam)

---

## Still Not Working?

### Check Power
Kinect v1 needs:
- USB data connection (to laptop)
- **External power adapter** (should be plugged in and LED lit)
- If LED on Kinect is off → check power adapter

### Check Conflicts
- Close Skype, Teams, or any app that might use cameras
- Only one app can access Kinect at a time

### Alternative: Use Laptop Webcam
If Kinect issues persist, the scanner works fine with laptop webcam:
- Just use Camera 0 (default)
- Lower quality but functional for testing

---

## Files Created
- `fix_kinect_drivers.ps1` - Automated driver repair (run as admin)
- `find_kinect_camera.py` - Camera detection diagnostic tool
- `KINECT_NOT_DETECTED.md` - This guide

## Related Documentation
- `KINECT_V1_QUICK_START.md` - Original setup guide
- `KINECT_V1_LIBUSBK_TROUBLESHOOTING.md` - Advanced troubleshooting
- `KINECT_SETUP.md` - Kinect v2 setup (different device)
