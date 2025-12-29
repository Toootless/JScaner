#!/usr/bin/env python3
"""
JScaner Kinect Scanner - Standalone Kinect v1 Capture & Export Program

This is a simplified, portable version of JScaner designed to run on a separate laptop
with a Kinect v1 (Xbox 360) camera. It captures images and exports them in a format
compatible with the main JScaner application for processing.

Usage:
    python kinect_scanner.py

Features:
    - Live Kinect v1 camera preview
    - Grid calibration support
    - Batch image capture
    - Automatic export to JScaner-compatible format
    - Minimal dependencies
"""

import sys
import os
import cv2
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Configure paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "captured"
CALIBRATION_FILE = BASE_DIR / "data" / "last_calibration.json"

# Ensure data directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
(BASE_DIR / "data").mkdir(parents=True, exist_ok=True)


class KinectScanner:
    """Kinect v1 Scanner - Captures and exports 3D scan images."""
    
    def __init__(self, camera_id: int = 0, output_dir: Optional[Path] = None):
        """
        Initialize the Kinect scanner.
        
        Args:
            camera_id: OpenCV device ID for the camera (default 0)
            output_dir: Directory for captured images (default: data/captured/)
        """
        self.camera_id = camera_id
        self.output_dir = Path(output_dir) if output_dir else DATA_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.cap = None
        self.is_running = False
        self.calibration = self._load_calibration()
        self.frame_count = 0
        self.captured_images: List[Dict[str, str]] = []
        
        print(f"[KinectScanner] Initializing with camera ID: {camera_id}")
        print(f"[KinectScanner] Output directory: {self.output_dir}")
    
    def _load_calibration(self) -> Optional[Dict]:
        """Load calibration data if available."""
        if CALIBRATION_FILE.exists():
            try:
                with open(CALIBRATION_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARNING] Could not load calibration: {e}")
        return None
    
    def connect(self) -> bool:
        """
        Connect to Kinect camera.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"[KinectScanner] Connecting to camera ID {self.camera_id}...")
            self.cap = cv2.VideoCapture(self.camera_id)
            
            if not self.cap.isOpened():
                print("[ERROR] Could not open camera")
                return False
            
            # Set camera properties for better quality
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
            
            # Test frame capture
            ret, frame = self.cap.read()
            if not ret or frame is None:
                print("[ERROR] Could not capture test frame")
                return False
            
            print(f"[SUCCESS] Connected to camera {self.camera_id}")
            print(f"[INFO] Frame size: {frame.shape[1]}x{frame.shape[0]}")
            self.is_running = True
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from camera."""
        if self.cap:
            self.cap.release()
            self.is_running = False
            print("[KinectScanner] Camera disconnected")
    
    def capture_frame(self, frame_name: Optional[str] = None) -> Optional[Tuple[str, str]]:
        """
        Capture a single frame and save it.
        
        Args:
            frame_name: Custom name for the frame (optional)
            
        Returns:
            Tuple of (frame_path, metadata_path) if successful, None otherwise
        """
        if not self.is_running or self.cap is None:
            print("[ERROR] Camera not connected")
            return None
        
        try:
            ret, frame = self.cap.read()
            if not ret or frame is None:
                print("[ERROR] Failed to capture frame")
                return None
            
            self.frame_count += 1
            
            # Generate filename
            if frame_name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                frame_name = f"scan_{timestamp}_{self.frame_count:03d}"
            else:
                frame_name = frame_name.replace(" ", "_")
            
            # Save image
            image_path = self.output_dir / f"{frame_name}.jpg"
            cv2.imwrite(str(image_path), frame)
            
            # Save metadata
            metadata = {
                "filename": image_path.name,
                "timestamp": datetime.now().isoformat(),
                "camera_id": self.camera_id,
                "frame_size": [frame.shape[1], frame.shape[0]],
                "calibration": self.calibration is not None
            }
            
            metadata_path = self.output_dir / f"{frame_name}_metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            self.captured_images.append({
                "image": str(image_path),
                "metadata": str(metadata_path)
            })
            
            print(f"[CAPTURED] {frame_name}.jpg ({image_path.stat().st_size // 1024} KB)")
            return (str(image_path), str(metadata_path))
            
        except Exception as e:
            print(f"[ERROR] Failed to capture frame: {e}")
            return None
    
    def auto_capture_sequence(self, count: int = 20, interval: float = 0.5) -> List[Tuple[str, str]]:
        """
        Capture a sequence of frames automatically.
        
        Args:
            count: Number of frames to capture
            interval: Delay between captures in seconds
            
        Returns:
            List of captured image paths
        """
        if not self.is_running:
            print("[ERROR] Camera not connected")
            return []
        
        results = []
        print(f"\n[SEQUENCE] Starting auto-capture of {count} frames...")
        print("[SEQUENCE] Frames will be captured every {:.1f} seconds".format(interval))
        
        for i in range(count):
            result = self.capture_frame(f"auto_sequence_{i+1:02d}")
            if result:
                results.append(result)
                remaining = count - i - 1
                if remaining > 0:
                    print(f"[SEQUENCE] {remaining} frames remaining...")
                    time.sleep(interval)
        
        print(f"[SEQUENCE] Completed: {len(results)} frames captured\n")
        return results
    
    def get_camera_info(self) -> Dict:
        """Get camera information and properties."""
        if not self.cap:
            return {"status": "not_connected"}
        
        try:
            return {
                "device_id": self.camera_id,
                "width": int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height": int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "fps": self.cap.get(cv2.CAP_PROP_FPS),
                "focus": self.cap.get(cv2.CAP_PROP_AUTOFOCUS),
                "is_connected": self.is_running
            }
        except Exception as e:
            return {"error": str(e)}
    
    def export_manifest(self) -> str:
        """
        Export a manifest file listing all captured images.
        
        Returns:
            Path to manifest file
        """
        manifest = {
            "timestamp": datetime.now().isoformat(),
            "total_captures": len(self.captured_images),
            "output_directory": str(self.output_dir),
            "images": self.captured_images,
            "camera_info": self.get_camera_info(),
            "calibration_available": self.calibration is not None
        }
        
        manifest_path = self.output_dir / "manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"[MANIFEST] Exported to {manifest_path}")
        return str(manifest_path)
    
    def get_captured_count(self) -> int:
        """Get number of captured images."""
        return len(self.captured_images)


def print_banner():
    """Print application banner."""
    print("\n" + "="*60)
    print("  JScaner - Kinect v1 Scanner")
    print("  Standalone Image Capture & Export")
    print("="*60 + "\n")


def print_help():
    """Print help menu."""
    print("\nKINECT SCANNER COMMANDS:")
    print("  c <name>   - Capture single frame (optional: custom name)")
    print("  a <count>  - Auto-capture sequence (default: 20 frames)")
    print("  i          - Show camera info")
    print("  s          - Save manifest file")
    print("  q          - Quit")
    print("")


def find_available_cameras(max_index: int = 5) -> List[int]:
    """Find available camera indices."""
    available = []
    for idx in range(max_index):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                available.append(idx)
    return available


def main():
    """Main application loop."""
    print_banner()
    
    # Find available cameras
    print("[STARTUP] Scanning for available cameras...")
    available_cameras = find_available_cameras()
    
    if not available_cameras:
        print("[ERROR] No cameras found!")
        print("[INFO] Please check:")
        print("       - Kinect v1 is connected via USB")
        print("       - Drivers are installed")
        print("       - Device is not in use by another program")
        sys.exit(1)
    
    print(f"[INFO] Found {len(available_cameras)} camera(s): {available_cameras}")
    
    # Select camera
    camera_id = 0
    if len(available_cameras) > 1:
        print("\nMultiple cameras detected. Using camera 0 (change with --camera argument)")
    
    # Initialize scanner
    scanner = KinectScanner(camera_id=camera_id)
    
    if not scanner.connect():
        print("[ERROR] Failed to initialize scanner")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("  Scanner ready! Type 'h' for help or 'q' to quit")
    print("="*60 + "\n")
    
    try:
        while True:
            command = input(">>> ").strip().lower()
            
            if not command:
                continue
            
            parts = command.split(maxsplit=1)
            cmd = parts[0]
            arg = parts[1] if len(parts) > 1 else None
            
            if cmd == 'h':
                print_help()
            
            elif cmd == 'c':
                print(f"[CAPTURE] Taking photo...")
                result = scanner.capture_frame(frame_name=arg)
                if result:
                    print(f"[SUCCESS] Captured {scanner.get_captured_count()} total")
            
            elif cmd == 'a':
                count = int(arg) if arg and arg.isdigit() else 20
                scanner.auto_capture_sequence(count=count)
            
            elif cmd == 'i':
                info = scanner.get_camera_info()
                print("\nCAMERA INFORMATION:")
                for key, value in info.items():
                    print(f"  {key}: {value}")
                print()
            
            elif cmd == 's':
                scanner.export_manifest()
                print(f"[INFO] {scanner.get_captured_count()} images ready for processing\n")
            
            elif cmd == 'q':
                print("\n[SHUTDOWN] Saving manifest and exiting...")
                if scanner.captured_images:
                    scanner.export_manifest()
                scanner.disconnect()
                print("[DONE] Goodbye!\n")
                break
            
            else:
                print("[INFO] Unknown command. Type 'h' for help.")
    
    except KeyboardInterrupt:
        print("\n\n[SHUTDOWN] Interrupted by user...")
        if scanner.captured_images:
            scanner.export_manifest()
        scanner.disconnect()
        print("[DONE] Scanner closed.\n")
    
    except Exception as e:
        print(f"\n[ERROR] {e}")
        scanner.disconnect()
        sys.exit(1)


if __name__ == "__main__":
    main()
