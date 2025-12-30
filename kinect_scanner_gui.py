#!/usr/bin/env python3
"""
JScaner Kinect Scanner GUI - Enhanced Multi-Camera Version

Professional interface with multiple camera support:
- Auto-detect available cameras
- Camera selection dropdown
- Live preview window
- Single image capture
- Batch capture with configurable settings
- Real-time statistics
- Manifest export

Usage:
    python kinect_scanner_gui.py

Requirements:
    - opencv-python
    - numpy
    - Pillow
    - tkinter (built-in with Python)
"""

import sys
import os
import cv2
import json
import time
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from tkinter import Tk, Frame, Button, Label, Entry, StringVar, Scale, HORIZONTAL, VERTICAL, messagebox, filedialog, OptionMenu
from tkinter import TOP, LEFT, RIGHT, BOTTOM, CENTER, X, Y, BOTH, END
from PIL import Image, ImageTk
import tkinter as tk

# Configure paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "captured"
CALIBRATION_FILE = BASE_DIR / "data" / "last_calibration.json"

# Ensure data directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
(BASE_DIR / "data").mkdir(parents=True, exist_ok=True)


class CameraDetector:
    """Detect and enumerate available cameras."""
    
    @staticmethod
    def get_available_cameras() -> Dict[int, str]:
        """
        Detect all available cameras on the system including Kinect v1.
        
        Returns:
            Dict with camera_id/name as key and camera_name as value
        """
        available_cameras = {}
        
        # Check for Kinect v1 via .NET SDK
        try:
            sys.path.insert(0, str(BASE_DIR / "src" / "core"))
            from kinect_v1_dotnet import KinectV1Camera
            
            # Try to initialize Kinect
            kinect_test = KinectV1Camera()
            if kinect_test.initialize():
                available_cameras["kinect_v1"] = "Kinect v1 (640x480 @ 30fps via .NET SDK)"
                kinect_test.release()
        except Exception as e:
            # Kinect not available, skip silently
            pass
        
        # Try standard cameras 0-9
        for camera_id in range(10):
            cap = cv2.VideoCapture(camera_id)
            if cap.isOpened():
                # Get camera properties
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                
                # Try to get camera name from backend
                backend_id = int(cap.get(cv2.CAP_PROP_BACKEND))
                backend_name = CameraDetector._get_backend_name(backend_id)
                
                # Create descriptive name
                if camera_id == 0:
                    camera_name = f"Camera {camera_id} (Default Webcam) - {width}x{height} @ {fps}fps"
                else:
                    camera_name = f"Camera {camera_id} ({backend_name}) - {width}x{height} @ {fps}fps"
                
                available_cameras[camera_id] = camera_name
                cap.release()
        
        return available_cameras
    
    @staticmethod
    def _get_backend_name(backend_id: int) -> str:
        """Get human-readable backend name."""
        backends = {
            0: "VfW",
            100: "V4L",
            200: "VfW",
            300: "DirectShow",
            400: "VfW",
            500: "VfW",
            600: "IEEE1394",
            700: "PVAPI",
            800: "OpenNI",
            900: "OpenNI_ASUS",
            1000: "Android",
            1100: "XIAPI",
            1200: "AVFoundation",
            1300: "Giganetix",
            1400: "Msmf",
            1500: "WinRT",
            1600: "Intelperc",
        }
        return backends.get(backend_id, "Unknown")


class KinectScannerGUI:
    """Enhanced Kinect Scanner with GUI and multi-camera support."""
    
    def __init__(self, root: Tk, camera_id: int = 0, output_dir: Optional[Path] = None):
        """Initialize the GUI scanner."""
        self.root = root
        self.root.title("Kinect v1 Scanner - Image Collection Tool (Multi-Camera)")
        self.root.geometry("1200x850")
        self.root.resizable(True, True)
        
        self.camera_id = camera_id
        self.output_dir = Path(output_dir) if output_dir else DATA_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Detect available cameras
        self.available_cameras = CameraDetector.get_available_cameras()
        
        # Camera
        self.cap = None
        self.is_running = False
        self.preview_active = False
        
        # Capture state
        self.captured_count = 0
        self.batch_count = 0
        self.batch_interval = 1.0
        self.is_batch_capturing = False
        self.calibration = self._load_calibration()
        
        # UI Variables
        self.status_var = StringVar(value="Ready")
        self.capture_count_var = StringVar(value="0")
        self.batch_size_var = StringVar(value="10")
        self.camera_var = StringVar(value=str(camera_id))
        
        # Build GUI
        self._build_gui()
        self._connect_camera()
        
        # Start preview thread
        self.preview_thread = threading.Thread(target=self._preview_loop, daemon=True)
        self.preview_thread.start()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _build_gui(self):
        """Build the GUI layout."""
        # Main container
        main_frame = Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Top: Camera Selection
        camera_select_frame = Frame(main_frame, bg="lightgray", relief="sunken", padx=10, pady=8)
        camera_select_frame.pack(fill=X, side=TOP, padx=5, pady=(0, 5))
        
        Label(camera_select_frame, text="📷 Camera Selection:", font=("Arial", 10, "bold"), bg="lightgray").pack(side=LEFT, padx=5)
        
        # Camera dropdown
        if self.available_cameras:
            camera_options = [f"{cam_id}: {name}" for cam_id, name in self.available_cameras.items()]
            self.camera_dropdown = OptionMenu(
                camera_select_frame,
                self.camera_var,
                *[str(cam_id) for cam_id in self.available_cameras.keys()],
                command=self._on_camera_changed
            )
            self.camera_dropdown.pack(side=LEFT, padx=5)
            
            # Update camera_var display text
            self.camera_var.set(str(self.camera_id))
            
            # Show current camera info
            if self.camera_id in self.available_cameras:
                camera_info_label = Label(
                    camera_select_frame,
                    text=f"Current: {self.available_cameras[self.camera_id]}",
                    font=("Arial", 9),
                    bg="lightgray",
                    fg="darkblue"
                )
                camera_info_label.pack(side=LEFT, padx=5)
                self.camera_info_label = camera_info_label
        else:
            Label(camera_select_frame, text="❌ No cameras detected!", font=("Arial", 10), bg="lightgray", fg="red").pack(side=LEFT, padx=5)
        
        # Refresh cameras button
        refresh_button = Button(
            camera_select_frame,
            text="🔄 Refresh",
            command=self._refresh_cameras,
            font=("Arial", 9),
            bg="#FF9800",
            fg="white",
            padx=10
        )
        refresh_button.pack(side=RIGHT, padx=5)
        
        # Preview section
        preview_frame = Frame(main_frame, bg="black", highlightthickness=2, highlightbackground="gray")
        preview_frame.pack(fill=BOTH, expand=True, side=TOP, padx=5, pady=5)
        
        self.preview_label = Label(preview_frame, bg="black", text="Initializing camera...")
        self.preview_label.pack(fill=BOTH, expand=True)
        
        # Bottom: Controls section
        control_frame = Frame(main_frame)
        control_frame.pack(fill=X, side=BOTTOM, padx=5, pady=5)
        
        # Left panel: Capture controls
        left_panel = Frame(control_frame)
        left_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        
        # Title
        title_label = Label(left_panel, text="IMAGE COLLECTION", font=("Arial", 12, "bold"))
        title_label.pack(anchor="w", pady=5)
        
        # Single capture
        single_frame = Frame(left_panel)
        single_frame.pack(fill=X, pady=5)
        
        single_button = Button(
            single_frame,
            text="📷 Capture Single Image",
            command=self._capture_single,
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=10,
            height=2
        )
        single_button.pack(fill=X)
        
        # Batch capture
        batch_title = Label(left_panel, text="Batch Capture", font=("Arial", 10, "bold"))
        batch_title.pack(anchor="w", pady=(15, 5))
        
        batch_config_frame = Frame(left_panel)
        batch_config_frame.pack(fill=X, pady=5)
        
        Label(batch_config_frame, text="Count:").pack(side=LEFT, padx=5)
        batch_count_entry = Entry(batch_config_frame, textvariable=self.batch_size_var, width=5)
        batch_count_entry.pack(side=LEFT, padx=5)
        
        Label(batch_config_frame, text="Interval (sec):").pack(side=LEFT, padx=5)
        interval_var = StringVar(value="1.0")
        interval_entry = Entry(batch_config_frame, textvariable=interval_var, width=5)
        interval_entry.pack(side=LEFT, padx=5)
        self.interval_var = interval_var
        
        batch_button = Button(
            left_panel,
            text="🔄 Start Batch Capture",
            command=self._start_batch_capture,
            font=("Arial", 10, "bold"),
            bg="#2196F3",
            fg="white",
            padx=15,
            pady=8
        )
        batch_button.pack(fill=X, pady=5)
        self.batch_button = batch_button
        
        stop_batch_button = Button(
            left_panel,
            text="⏹ Stop Batch",
            command=self._stop_batch_capture,
            font=("Arial", 10, "bold"),
            bg="#f44336",
            fg="white",
            padx=15,
            pady=8,
            state="disabled"
        )
        stop_batch_button.pack(fill=X, pady=5)
        self.stop_batch_button = stop_batch_button
        
        # Middle panel: Status and stats
        middle_panel = Frame(control_frame)
        middle_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=5)
        
        title_label2 = Label(middle_panel, text="STATUS & STATS", font=("Arial", 12, "bold"))
        title_label2.pack(anchor="w", pady=5)
        
        status_frame = Frame(middle_panel)
        status_frame.pack(fill=X, pady=5)
        Label(status_frame, text="Status:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        status_display = Label(status_frame, textvariable=self.status_var, font=("Arial", 10), fg="green")
        status_display.pack(side=LEFT, padx=5)
        
        count_frame = Frame(middle_panel)
        count_frame.pack(fill=X, pady=5)
        Label(count_frame, text="Images Captured:", font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        count_display = Label(count_frame, textvariable=self.capture_count_var, font=("Arial", 10, "bold"), fg="blue")
        count_display.pack(side=LEFT, padx=5)
        
        # Right panel: Utility buttons
        right_panel = Frame(control_frame)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
        
        title_label3 = Label(right_panel, text="UTILITIES", font=("Arial", 12, "bold"))
        title_label3.pack(anchor="w", pady=5)
        
        open_folder_button = Button(
            right_panel,
            text="📁 Open Capture Folder",
            command=self._open_capture_folder,
            font=("Arial", 10, "bold"),
            bg="#FF9800",
            fg="white",
            padx=10,
            pady=8
        )
        open_folder_button.pack(fill=X, pady=5)
        
        export_button = Button(
            right_panel,
            text="💾 Export Manifest",
            command=self._export_manifest,
            font=("Arial", 10, "bold"),
            bg="#9C27B0",
            fg="white",
            padx=10,
            pady=8
        )
        export_button.pack(fill=X, pady=5)
    
    def _load_calibration(self) -> Optional[Dict]:
        """Load calibration data if available."""
        if CALIBRATION_FILE.exists():
            try:
                with open(CALIBRATION_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self._update_status(f"Calibration load failed: {e}")
        return None
    
    def _refresh_cameras(self):
        """Refresh available cameras list and update dropdown."""
        self._update_status("Scanning for cameras...")
        
        # Release current camera
        was_running = self.is_running
        if self.cap:
            self.is_running = False
            self.cap.release()
            self.cap = None
        
        # Re-scan cameras
        self.available_cameras = CameraDetector.get_available_cameras()
        
        if self.available_cameras:
            self._update_status(f"Found {len(self.available_cameras)} camera(s)")
            
            # Rebuild the dropdown menu
            if hasattr(self, 'camera_dropdown'):
                menu = self.camera_dropdown["menu"]
                menu.delete(0, "end")
                
                # Add new camera options
                for cam_id in self.available_cameras.keys():
                    menu.add_command(
                        label=f"{cam_id}: {self.available_cameras[cam_id]}",
                        command=lambda value=str(cam_id): self._on_camera_changed(value)
                    )
                
                # Select first camera if current not available
                if self.camera_id not in self.available_cameras:
                    first_cam = list(self.available_cameras.keys())[0]
                    self.camera_id = first_cam
                    self.camera_var.set(str(first_cam))
            
            # Reconnect if was running
            if was_running:
                self._connect_camera()
        else:
            self._update_status("ERROR: No cameras found")
            messagebox.showerror("No Cameras", "No camera devices detected on this system")
    
    def _on_camera_changed(self, new_camera_id: str):
        """Handle camera selection change from dropdown."""
        self._change_camera(new_camera_id)
    
    def _change_camera(self, new_camera_id: str):
        """Change active camera."""
        try:
            # Handle both integer camera IDs and string IDs (like "kinect_v1")
            if new_camera_id.isdigit():
                new_id = int(new_camera_id)
            else:
                new_id = new_camera_id
            
            if new_id != self.camera_id:
                self._update_status(f"Switching to camera {new_id}...")
                self.camera_id = new_id
                self.is_running = False
                
                # Close old camera
                if self.cap:
                    self.cap.release()
                    self.cap = None
                
                # Small delay
                time.sleep(0.5)
                
                # Connect new camera
                self._connect_camera()
                
                # Update display
                if hasattr(self, 'camera_info_label') and new_id in self.available_cameras:
                    self.camera_info_label.config(text=f"Current: {self.available_cameras[new_id]}")
        except ValueError:
            self._update_status("Invalid camera selection")
    
    def _connect_camera(self) -> bool:
        """Connect to camera (supports both standard cameras and Kinect v1)."""
        try:
            self._update_status(f"Connecting to camera {self.camera_id}...")
            
            # Check if this is Kinect v1
            if self.camera_id == "kinect_v1":
                sys.path.insert(0, str(BASE_DIR / "src" / "core"))
                from kinect_v1_dotnet import KinectV1Camera
                
                self.cap = KinectV1Camera()
                if not self.cap.initialize():
                    self._update_status("ERROR: Could not initialize Kinect v1")
                    messagebox.showerror("Kinect Error", "Failed to initialize Kinect v1\n\nMake sure:\n- Kinect is plugged in and powered\n- No other apps are using Kinect\n- Kinect SDK v1.8 is installed")
                    return False
            else:
                # Standard OpenCV camera
                self.cap = cv2.VideoCapture(self.camera_id)
                
                if not self.cap.isOpened():
                    self._update_status(f"ERROR: Could not open camera {self.camera_id}")
                    messagebox.showerror("Camera Error", f"Failed to open camera {self.camera_id}\n\nTry selecting a different camera or run 'Refresh'")
                    return False
                
                # Set camera properties
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
                self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            
            # Test frame
            ret, frame = self.cap.read()
            if not ret or frame is None:
                self._update_status(f"ERROR: Could not capture test frame from camera {self.camera_id}")
                return False
            
            self.is_running = True
            camera_name = self.available_cameras.get(self.camera_id, f"Camera {self.camera_id}")
            self._update_status(f"✓ Camera connected: {camera_name.split('-')[0]}")
            return True
        except Exception as e:
            self._update_status(f"Connection error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _preview_loop(self):
        """Continuously update preview."""
        while True:
            if self.is_running and self.cap and self.cap.isOpened():
                ret, frame = self.cap.read()
                
                if ret and frame is not None:
                    # Resize for display
                    display_frame = cv2.resize(frame, (640, 480))
                    
                    # Add info overlay
                    cv2.putText(
                        display_frame,
                        f"Captured: {self.captured_count}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )
                    
                    if self.is_batch_capturing:
                        cv2.putText(
                            display_frame,
                            f"Batch: {self.batch_count}",
                            (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 165, 255),
                            2
                        )
                    
                    # Convert for tkinter
                    frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(frame_rgb)
                    photo = ImageTk.PhotoImage(pil_image)
                    
                    self.preview_label.config(image=photo)
                    self.preview_label.image = photo
                    self.preview_active = True
            
            time.sleep(0.033)  # ~30 FPS
    
    def _capture_single(self):
        """Capture a single image."""
        if not self.is_running or not self.cap:
            messagebox.showerror("Error", "Camera not connected")
            return
        
        try:
            ret, frame = self.cap.read()
            if not ret or frame is None:
                messagebox.showerror("Error", "Failed to capture frame")
                return
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.captured_count += 1
            seq_num = str(self.captured_count).zfill(3)
            filename = f"scan_{timestamp}_{seq_num}.jpg"
            filepath = self.output_dir / filename
            
            # Save image
            cv2.imwrite(str(filepath), frame)
            
            # Save metadata
            metadata = {
                "filename": filename,
                "timestamp": timestamp,
                "sequence": self.captured_count,
                "camera": self.available_cameras.get(self.camera_id, str(self.camera_id)),
                "resolution": {
                    "width": frame.shape[1],
                    "height": frame.shape[0]
                },
                "format": "BGR"
            }
            
            metadata_file = filepath.with_suffix('.json').name.replace('.jpg', '_metadata.json')
            metadata_path = self.output_dir / metadata_file
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.capture_count_var.set(str(self.captured_count))
            self._update_status(f"✓ Captured: {filename}")
            
        except Exception as e:
            messagebox.showerror("Capture Error", str(e))
            self._update_status(f"Capture failed: {e}")
    
    def _start_batch_capture(self):
        """Start batch capture."""
        try:
            count = int(self.batch_size_var.get())
            interval = float(self.interval_var.get())
            
            if count <= 0:
                messagebox.showerror("Error", "Count must be > 0")
                return
            
            self.batch_count = 0
            self.is_batch_capturing = True
            self.batch_button.config(state="disabled")
            self.stop_batch_button.config(state="normal")
            self._update_status(f"Starting batch: {count} images")
            
            # Run batch in thread
            batch_thread = threading.Thread(
                target=self._batch_capture_worker,
                args=(count, interval),
                daemon=True
            )
            batch_thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid count or interval")
    
    def _batch_capture_worker(self, count: int, interval: float):
        """Worker thread for batch capture."""
        try:
            for i in range(count):
                if not self.is_batch_capturing:
                    break
                
                ret, frame = self.cap.read()
                if ret and frame is not None:
                    # Generate filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    self.captured_count += 1
                    seq_num = str(self.captured_count).zfill(3)
                    filename = f"scan_{timestamp}_{seq_num}.jpg"
                    filepath = self.output_dir / filename
                    
                    # Save image
                    cv2.imwrite(str(filepath), frame)
                    
                    # Save metadata
                    metadata = {
                        "filename": filename,
                        "timestamp": timestamp,
                        "sequence": self.captured_count,
                        "batch_index": i + 1,
                        "batch_total": count,
                        "camera": self.available_cameras.get(self.camera_id, str(self.camera_id)),
                        "resolution": {
                            "width": frame.shape[1],
                            "height": frame.shape[0]
                        },
                        "format": "BGR"
                    }
                    
                    metadata_file = filepath.with_suffix('.json').name.replace('.jpg', '_metadata.json')
                    metadata_path = self.output_dir / metadata_file
                    with open(metadata_path, 'w') as f:
                        json.dump(metadata, f, indent=2)
                    
                    self.batch_count = i + 1
                    self.capture_count_var.set(str(self.captured_count))
                    self._update_status(f"Batch: {i+1}/{count}")
                
                time.sleep(interval)
            
            if self.is_batch_capturing:
                self._update_status(f"✓ Batch complete: {count} images")
            else:
                self._update_status("Batch stopped by user")
        
        except Exception as e:
            self._update_status(f"Batch error: {e}")
        
        finally:
            self.is_batch_capturing = False
            self.batch_button.config(state="normal")
            self.stop_batch_button.config(state="disabled")
    
    def _stop_batch_capture(self):
        """Stop batch capture."""
        self.is_batch_capturing = False
        self._update_status("Batch capture stopped")
    
    def _export_manifest(self):
        """Export manifest of captured images."""
        try:
            images = list(self.output_dir.glob("scan_*.jpg"))
            
            if not images:
                messagebox.showinfo("Info", "No images captured yet")
                return
            
            manifest = {
                "export_time": datetime.now().isoformat(),
                "total_images": len(images),
                "output_directory": str(self.output_dir),
                "camera_id": self.camera_id,
                "camera_name": self.available_cameras.get(self.camera_id, f"Camera {self.camera_id}"),
                "images": []
            }
            
            for img_path in sorted(images):
                manifest["images"].append({
                    "filename": img_path.name,
                    "size_bytes": img_path.stat().st_size,
                    "created": datetime.fromtimestamp(img_path.stat().st_ctime).isoformat()
                })
            
            # Save manifest
            manifest_path = self.output_dir / "manifest.json"
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            messagebox.showinfo("Success", f"Manifest exported:\n{manifest_path}\n\nTotal images: {len(images)}")
            self._update_status(f"✓ Manifest exported ({len(images)} images)")
        
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
    
    def _open_capture_folder(self):
        """Open capture folder in explorer."""
        try:
            import subprocess
            subprocess.Popen(f'explorer "{self.output_dir}"')
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder: {e}")
    
    def _update_status(self, message: str):
        """Update status display."""
        self.status_var.set(message)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def _on_close(self):
        """Handle window close."""
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()


def main():
    """Main entry point."""
    root = Tk()
    app = KinectScannerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
