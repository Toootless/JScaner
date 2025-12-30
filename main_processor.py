#!/usr/bin/env python3
"""
JScaner - Image Processing and 3D Reconstruction

This application processes captured images and metadata files to reconstruct 3D objects.
"""

import sys
import os
import json
import glob
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Check for Open3D availability
try:
    import open3d
    print("✓ Open3D available - full 3D reconstruction features enabled")
except ImportError:
    print("⚠ Open3D not available - using fallback reconstruction methods")

from gui.main_window import MainApplication

class ImageDataProcessor:
    """Process captured images and metadata files."""
    
    def __init__(self, captured_dir):
        """Initialize processor with captured images directory."""
        self.captured_dir = captured_dir
        self.images = []
        self.metadata = []
        self.load_images_and_metadata()
    
    def load_images_and_metadata(self):
        """Load all images and corresponding metadata files."""
        # Get all JPG files
        jpg_files = sorted(glob.glob(os.path.join(self.captured_dir, "*.jpg")))
        
        print(f"\n📁 Loading images from: {self.captured_dir}")
        print(f"Found {len(jpg_files)} image files\n")
        
        for jpg_file in jpg_files:
            # Find corresponding JSON metadata
            json_file = jpg_file.replace('.jpg', '.json')
            
            if os.path.exists(json_file):
                try:
                    with open(json_file, 'r') as f:
                        metadata = json.load(f)
                    
                    self.images.append(jpg_file)
                    self.metadata.append(metadata)
                    
                    print(f"✓ Loaded: {os.path.basename(jpg_file)}")
                    print(f"  └─ Metadata: {metadata.get('camera', 'Unknown')} "
                          f"@ {metadata.get('resolution', {}).get('width', '?')}x"
                          f"{metadata.get('resolution', {}).get('height', '?')}")
                except json.JSONDecodeError:
                    print(f"⚠ Invalid JSON: {os.path.basename(json_file)}")
            else:
                print(f"⚠ No metadata for: {os.path.basename(jpg_file)}")
    
    def get_summary(self):
        """Get summary of loaded data."""
        return {
            "total_images": len(self.images),
            "images": self.images,
            "metadata": self.metadata,
            "captured_dir": self.captured_dir
        }
    
    def print_summary(self):
        """Print summary of loaded data."""
        print(f"\n{'='*60}")
        print(f"📊 IMAGE PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f"Total images loaded: {len(self.images)}")
        print(f"Total metadata entries: {len(self.metadata)}")
        print(f"Images directory: {self.captured_dir}")
        
        if self.images:
            print(f"\n📷 Camera Configuration:")
            if self.metadata:
                meta = self.metadata[0]
                print(f"   Camera: {meta.get('camera', 'Unknown')}")
                res = meta.get('resolution', {})
                print(f"   Resolution: {res.get('width', '?')}x{res.get('height', '?')}")
                print(f"   Format: {meta.get('format', 'Unknown')}")
        
        print(f"\n✓ Ready for 3D reconstruction!")
        print(f"{'='*60}\n")


def main():
    """Launch the JScaner application with image processing."""
    try:
        # Get captured directory
        base_dir = os.path.dirname(__file__)
        captured_dir = os.path.join(base_dir, 'captured')
        
        # Check if captured directory exists
        if not os.path.exists(captured_dir):
            print(f"Error: Captured directory not found: {captured_dir}")
            sys.exit(1)
        
        # Load and process images
        processor = ImageDataProcessor(captured_dir)
        processor.print_summary()
        
        # Launch GUI with loaded images
        app = MainApplication()
        
        # Pre-load the captured images and metadata into the application
        summary = processor.get_summary()
        app.load_processed_images(summary)
        
        app.run()
        
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
