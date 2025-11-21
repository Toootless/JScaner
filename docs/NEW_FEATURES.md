# JScaner New Features

## Overview
This document describes the three new features added to enhance the JScaner workflow.

## 1. Auto-Load Last Calibration

### Description
JScaner now automatically loads the last saved calibration when the application starts. This eliminates the need to manually load calibration data every time you restart the program.

### How It Works
- When you save a calibration, it's automatically stored in `data/last_calibration.json`
- On startup, JScaner checks for this file and loads it automatically
- The calibration status display shows "Calibration loaded from last session"
- Status bar confirms: "Last calibration auto-loaded successfully"

### Location
- Calibration file: `data/last_calibration.json`
- Auto-loaded during application initialization

### Benefits
- Faster workflow - no need to manually reload calibration
- Consistent results across sessions
- Reduced setup time for repeated scans

---

## 2. Load External Images

### Description
Import images from external sources with a choice of purpose: for 3D reconstruction processing or for camera calibration.

### How to Use
1. Click **"Load Images"** button in the Capture tab
2. Select one or more image files from the file dialog
3. Choose the purpose in the popup dialog:
   - **3D Reconstruction (Processing)**: Images will be used for creating 3D models
   - **Camera Calibration**: Images will be used to calibrate the camera

### Supported Formats
- PNG (.png)
- JPEG (.jpg, .jpeg)
- Bitmap (.bmp)
- TIFF (.tiff)

### Image Display
- External images are prefixed with **[EXT]** in the image list
- Shows the original filename for easy identification
- Count displayed in status bar: "Loaded X images for [purpose]"

### Use Cases
- Import pre-captured checkerboard images for calibration
- Load high-quality images captured with external cameras
- Batch process existing image sets
- Use images from other scanning sessions

---

## 3. Show Save Location & Custom Naming

### Description
View the directory where captured images are saved and optionally provide custom names for each image.

### Custom Naming (Capture)
When you click **"Capture Image"**:
1. A naming dialog appears
2. Enter a custom name (optional) or leave blank for auto-naming
3. Auto-naming format: `image_001.png`, `image_002.png`, etc.
4. Custom naming: `[your_name].png`

### Save Location Display
Click **"Show Save Location"** button to:
- View the full path to the captured images directory
- **Open Folder**: Opens the directory in Windows Explorer
- **Copy Path**: Copies the path to clipboard
- **Close**: Closes the dialog

### Default Save Location
```
data/captured/
```

### File Storage Structure
```
3dscaning/
├── data/
│   ├── captured/          # All captured images
│   │   ├── image_001.png
│   │   ├── image_002.png
│   │   ├── custom_name.png
│   │   └── ...
│   └── last_calibration.json  # Auto-loaded calibration
```

### Benefits
- Easy access to captured images for backup or external processing
- Custom naming for better organization
- Quick path copying for documentation or sharing
- Direct folder access for file management

---

## Image Metadata Structure

Each captured or imported image now includes metadata:

```python
{
    'image': numpy_array,        # The actual image data
    'source': 'camera' | 'external',  # Where image came from
    'filepath': 'path/to/file',  # Saved location (camera only)
    'original_path': 'path',     # Original location (external only)
    'purpose': 'processing' | 'calibration'  # Intended use
}
```

This metadata enables:
- Tracking image sources
- Differentiating between capture types
- Maintaining file references
- Purpose-specific processing

---

## Technical Notes

### Directory Creation
The application automatically creates required directories:
- `data/` - Main data directory
- `data/captured/` - Captured images storage
- `data/last_calibration.json` - Auto-saved calibration

### Compatibility
- Works with existing image capture functionality
- Backward compatible with older calibration files
- Handles both simple image arrays and metadata structures
- Supports multiple image formats

### Error Handling
- Missing calibration file on startup: silently continues without error
- Invalid external images: skipped with console message
- Empty naming dialog: uses auto-generated names
- Invalid save locations: creates directories automatically

---

## Usage Examples

### Example 1: Quick Scanning Workflow
1. Start JScaner → last calibration auto-loads
2. Capture images with custom names
3. Perform 3D reconstruction
4. Export STL

### Example 2: Using External Calibration Images
1. Click "Load Images"
2. Select checkerboard photos
3. Choose "Camera Calibration"
4. Run calibration
5. Calibration auto-saved for next session

### Example 3: Batch Processing
1. Click "Load Images"
2. Select multiple object photos
3. Choose "3D Reconstruction (Processing)"
4. Perform reconstruction
5. Export results

### Example 4: Organizing Captures
1. Before capturing, plan naming scheme
2. Capture with custom names: "object_top", "object_side", etc.
3. Click "Show Save Location"
4. Open folder to verify all images captured
5. Backup captured images for safekeeping

---

## Future Enhancements

Potential improvements for consideration:
- Image preview before importing
- Batch renaming of captured images
- Export image metadata to JSON
- Image filtering by purpose
- Automatic backup to external location
- Image quality assessment before processing

---

## Support

For issues or questions about these features, refer to:
- Main documentation: `README.md`
- API reference: `docs/API_REFERENCE.md`
- Project summary: `PROJECT_SUMMARY.md`
