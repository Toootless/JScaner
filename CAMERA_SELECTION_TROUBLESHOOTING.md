# Kinect Scanner - Camera Selection Troubleshooting

## Quick Diagnosis

### "I'm using the wrong camera (system webcam instead of Kinect)"

**Root Cause**: Camera 0 (default) is usually the system's default webcam

**Fast Fix**:
1. Launch GUI (it will show wrong camera)
2. Click dropdown at top
3. Try **Camera 1** (most common for second device)
4. Watch preview - does it look like a Kinect? (No fisheye, 640x480)
5. If yes → you found it! If no → try Camera 2, 3, etc.

### Quick ID Test

Look for:
- ✓ **Kinect v1**: Rectangular feed, 640×480, no distortion
- ✗ **System webcam**: Often round/wide-angle, may be different resolution

---

## Step-by-Step Camera Identification

### Step 1: Find All Cameras

```
1. Open kinect_scanner_gui.bat
2. Wait for app to load
3. Look at dropdown showing cameras
4. Count how many options there are
```

**Example result**: 3 cameras available (Camera 0, 1, 3)

### Step 2: Test Each Camera

```
1. Click dropdown
2. Select Camera 0
   - Watch preview for 3 seconds
   - Note characteristics (appearance, resolution)
3. Click dropdown again
4. Select Camera 1
   - Watch preview for 3 seconds
   - Different from Camera 0?
5. Try Camera 2, 3, etc. same way
```

### Step 3: Identify Your Kinect

| Camera | Typical Use | How to Identify |
|--------|------------|-----------------|
| Camera 0 | System webcam | Built-in, wide angle, often rounded |
| Camera 1+ | USB devices | Can be Kinect, USB webcam, other |
| Kinect v1 | Scanning | Rectangular 640×480, clean image |

---

## Common Scenarios & Solutions

### Scenario 1: Desktop with Webcam + Kinect

**Situation**:
```
PC Components:
- Built-in: Webcam (Camera 0)
- USB: Kinect v1 (Camera ?)
- Goal: Use Kinect, not webcam
```

**Solution**:
```
1. Launch GUI → sees Camera 0 (built-in)
2. Click dropdown
3. Look for Camera 1, 2, or 3
4. Try each one in preview
5. Watch for Kinect characteristics:
   - Rectangular, no fisheye
   - 640×480 resolution
   - Clean, clear image
6. That's your Kinect!
```

**Expected result**: Camera 1 or 2 is usually Kinect

### Scenario 2: Laptop with Webcam + Kinect

**Situation**:
```
Laptop:
- Built-in: HD Webcam (Camera 0)
- USB: Kinect v1 (Camera ?)
- Goal: Switch from built-in to Kinect
```

**Solution**:
```
Same as Scenario 1
- Built-in laptop webcam = Camera 0
- Kinect v1 = Camera 1, 2, or 3
- Click dropdown to find it
```

### Scenario 3: Multiple USB Cameras

**Situation**:
```
System:
- Camera 0: Built-in
- Camera 1: USB HD Webcam
- Camera 2: USB IR Camera
- Camera 3: Kinect v1
```

**Solution**:
```
1. Test each in preview
2. Kinect = rectangular, 640×480
3. USB HD = usually 1080p or similar
4. IR Camera = likely grayscale or unusual
5. Try resolution first:
   - 640×480? → Likely Kinect
   - Other? → Try next
```

---

## Diagnosis: Cannot Find Kinect

### Problem: Kinect Not Appearing in Dropdown

**Test 1**: Check USB Connection
```
1. Unplug Kinect from USB
2. Wait 5 seconds
3. In app, click "🔄 Refresh"
4. Nothing changes (expected)
5. Plug Kinect back in
6. Click "🔄 Refresh" again
7. Should appear!
```

**Test 2**: Check Device Manager
```
Windows + Pause
→ Device Manager
→ Look for:
  - "Kinect"
  - "Xbox 360 Camera" or similar
  - Any unknown devices?
```

**Test 3**: Check Drivers
```
If Kinect not in Device Manager:
1. Download Kinect v1 drivers
2. Run installation
3. Restart computer
4. Try GUI again
```

### Problem: Kinect Appears But Preview Freezes

**Test**: Camera Lock Issue
```
1. Close GUI
2. Close any other camera apps (Skype, Discord, etc.)
3. Reopen GUI
4. Try camera selection again
```

**If still freezes**:
```
1. It might be camera initialization delay
2. Wait full 10 seconds after selection
3. If preview eventually shows → camera works!
```

---

## Resolution by Operating System

### Windows 10/11 - Kinect Selection

**Expected camera order**:
```
Camera 0: Built-in or first USB device detected
Camera 1: Next device
Camera 2: Kinect usually here
Camera 3+: Additional devices
```

**Note**: Windows USB detection order isn't guaranteed; try all cameras.

### Checking USB Port Assignment

```PowerShell
# PowerShell command to list devices:
Get-PnpDevice -Class USB | Select-Object Name

# Look for Kinect or Camera entries
```

---

## Creating a Camera Reference Log

### Document Your Setup

**Recommended**: Create text file with camera mappings

```
MyPC_CameraLog.txt:

Camera 0: Built-in Webcam (NOT USED)
  - Description: Dell Integrated Webcam
  - Resolution: 1280x720
  - Note: Too wide-angle for scanning

Camera 1: USB Generic Webcam
  - Description: Generic USB Device
  - Resolution: 800x600
  - Note: Testing only

Camera 2: [EMPTY - Not available]

Camera 3: Kinect v1 ✓ USE THIS ONE
  - Description: Xbox 360 Kinect Camera
  - Resolution: 640x480
  - Backend: DirectShow
  - Note: BEST FOR SCANNING
```

**Usage**: Save this for future reference!

---

## Advanced: Check Which Camera Before Opening

### PowerShell Script to List Cameras

```powershell
# save as: list_cameras.ps1

import cv2

print("Scanning for available cameras...")
print("Please wait...\n")

for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Camera {i}: {int(width)}x{int(height)} @ {int(fps)}fps")
        cap.release()

print("\nDone! Use the camera number in dropdown.")
```

---

## Quick Reference: Camera By Numbers

### Standard PC Setup

```
Most likely Kinect: Camera 1 or 2
Test order: 1 → 2 → 3 → 0
```

### Laptop Setup

```
Most likely Kinect: Camera 1 or 2
Test order: 1 → 2 → 3
(Avoid Camera 0 - built-in)
```

### Multi-USB Setup

```
Most likely Kinect: Camera 2 or 3
Test order: 2 → 3 → 1
(Depends on USB port connection order)
```

---

## Not Working? Next Steps

1. **Document the problem**:
   - How many cameras appear?
   - Which looks like Kinect?
   - What error message?

2. **Check prerequisites**:
   - Is Kinect powered? (LED on back?)
   - Is Kinect USB connected?
   - Are drivers installed?

3. **Verify in Device Manager**:
   - Windows + Pause → Device Manager
   - Look for Kinect or Camera entries
   - Any yellow exclamation marks?

4. **Run diagnostic**:
   - Run `test_kinect_v1.py`
   - It will scan for Kinect specifically
   - Reports which camera it is

---

## Success Indicators

✓ **You found your Kinect when**:
- Preview shows rectangular, undistorted image
- Resolution shows 640×480
- No lag or freezing in live feed
- Can capture images successfully

✓ **Next step**: Use that camera number consistently

---

**Need more help?** See:
- `MULTI_CAMERA_GUIDE.md` - General multi-camera features
- `KINECT_SETUP.md` - Kinect v1 driver setup
- `test_kinect_v1.py` - Hardware diagnostic tool
