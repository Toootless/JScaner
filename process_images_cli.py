#!/usr/bin/env python3
"""
JScaner - CLI Image Processing and 3D Reconstruction

This command-line tool processes captured images for 3D reconstruction.
"""

import sys
import os
import json
import glob
import cv2
import numpy as np

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.grid_calibration import GridDetector
from core.reconstruction import StereoReconstructor
from core.stl_export import STLExporter

class ImageProcessor:
    """Process captured images for 3D reconstruction."""
    
    def __init__(self, captured_dir):
        """Initialize processor."""
        self.captured_dir = captured_dir
        self.images = []
        self.metadata = []
        self.grid_detector = GridDetector()
        self.reconstructor = StereoReconstructor()
        self.stl_exporter = STLExporter()
        self.calibration_data = None
        
    def load_images(self):
        """Load all images and metadata."""
        jpg_files = sorted(glob.glob(os.path.join(self.captured_dir, "*.jpg")))
        
        print(f"\n📁 Loading images from: {self.captured_dir}")
        print(f"Found {len(jpg_files)} image files\n")
        
        for jpg_file in jpg_files:
            try:
                img = cv2.imread(jpg_file)
                if img is not None:
                    self.images.append(img)
                    
                    # Load metadata
                    json_file = jpg_file.replace('.jpg', '.json')
                    metadata = {}
                    if os.path.exists(json_file):
                        try:
                            with open(json_file, 'r') as f:
                                metadata = json.load(f)
                        except:
                            pass
                    
                    self.metadata.append(metadata)
                    print(f"✓ {os.path.basename(jpg_file)}")
                    
            except Exception as e:
                print(f"✗ Failed to load {jpg_file}: {e}")
        
        print(f"\n✓ Loaded {len(self.images)} images")
        return len(self.images) > 0
    
    def load_calibration(self, cal_file="cal.json"):
        """Load existing calibration file."""
        cal_path = os.path.join(self.captured_dir, "..", cal_file)
        
        if not os.path.exists(cal_path):
            print(f"✗ Calibration file not found: {cal_path}")
            return False
        
        print(f"\n📋 Loading calibration from {os.path.basename(cal_path)}...")
        try:
            with open(cal_path, 'r') as f:
                self.calibration_data = json.load(f)
            
            self.reconstructor.load_calibration(self.calibration_data)
            print(f"✓ Calibration loaded successfully")
            return True
            
        except Exception as e:
            print(f"✗ Failed to load calibration: {e}")
            return False
    
    def calibrate(self, grid_size=10.0, grid_cols=9, grid_rows=6):
        """Calibrate camera using grid detection."""
        print(f"\n🔧 Calibrating camera...")
        print(f"Grid: {grid_cols}x{grid_rows}, Size: {grid_size}mm")
        
        try:
            self.grid_detector = GridDetector((grid_size, grid_size))
            self.calibration_data = self.grid_detector.calibrate_camera(
                self.images, (grid_cols, grid_rows)
            )
            
            if self.calibration_data:
                error = self.calibration_data.get('reprojection_error', 0)
                print(f"✓ Calibration successful (error: {error:.3f})")
                self.reconstructor.load_calibration(self.calibration_data)
                return True
            else:
                print("✗ Calibration failed")
                return False
                
        except Exception as e:
            print(f"✗ Calibration error: {e}")
            return False
    
    def reconstruct_3d(self):
        """Perform 3D reconstruction."""
        if not self.images:
            print("✗ No images loaded")
            return False
        
        if not self.calibration_data:
            print("✗ Camera not calibrated")
            return False
        
        print("\n🎯 Performing 3D reconstruction...")
        try:
            self.point_cloud = self.reconstructor.reconstruct_from_images(self.images)
            
            if self.point_cloud:
                if hasattr(self.point_cloud, 'points'):
                    point_count = len(self.point_cloud.points)
                elif hasattr(self.point_cloud, 'points_3d') and self.point_cloud.points_3d is not None:
                    point_count = len(self.point_cloud.points_3d)
                else:
                    point_count = 0
                
                print(f"✓ Reconstruction complete ({point_count} points)")
                return True
            else:
                print("✗ Reconstruction failed")
                return False
                
        except Exception as e:
            print(f"✗ Reconstruction error: {e}")
            return False
    
    def export_stl(self, output_file="output.stl", scale=1.0):
        """Export point cloud to STL file."""
        if not hasattr(self, 'point_cloud') or self.point_cloud is None:
            print("✗ No point cloud to export")
            return False
        
        print(f"\n💾 Exporting STL to {output_file}...")
        try:
            # For Open3D point clouds, create a mesh first
            try:
                import open3d as o3d
                if hasattr(self.point_cloud, 'points'):
                    # Compute normals for the point cloud
                    self.point_cloud.estimate_normals()
                    
                    # Create mesh from point cloud using Poisson reconstruction
                    print("  Creating mesh from point cloud...")
                    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
                        self.point_cloud, depth=8
                    )
                    
                    # Save mesh
                    o3d.io.write_triangle_mesh(output_file, mesh)
                    print(f"✓ STL exported successfully ({len(mesh.vertices)} vertices)")
                    return True
            except ImportError:
                pass
            
            # Fallback: use trimesh if available
            success = self.stl_exporter.export_point_cloud_to_stl(
                self.point_cloud, output_file, scale_factor=scale
            )
            
            if success:
                print(f"✓ STL exported successfully")
                return True
            else:
                print("✗ Export failed")
                return False
                
        except Exception as e:
            print(f"✗ Export error: {e}")
            return False
    
    def print_summary(self):
        """Print processing summary."""
        print(f"\n{'='*60}")
        print(f"📊 JSCANER - IMAGE PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f"Total images: {len(self.images)}")
        print(f"Calibration: {'✓' if self.calibration_data else '✗'}")
        print(f"Point cloud: {'✓' if hasattr(self, 'point_cloud') else '✗'}")
        
        if self.metadata and self.metadata[0]:
            meta = self.metadata[0]
            print(f"\nCamera Info:")
            print(f"  Camera: {meta.get('camera', 'Unknown')}")
            res = meta.get('resolution', {})
            print(f"  Resolution: {res.get('width', '?')}x{res.get('height', '?')}")
            print(f"  Format: {meta.get('format', 'Unknown')}")
        
        print(f"{'='*60}\n")


def main():
    """Main CLI workflow."""
    try:
        # Setup
        base_dir = os.path.dirname(__file__)
        captured_dir = os.path.join(base_dir, 'captured')
        
        if not os.path.exists(captured_dir):
            print(f"✗ Error: Captured directory not found: {captured_dir}")
            return 1
        
        # Initialize processor
        processor = ImageProcessor(captured_dir)
        
        # Load images
        if not processor.load_images():
            print("✗ Failed to load images")
            return 1
        
        # Try to load existing calibration
        if not processor.load_calibration():
            print("✗ Could not load calibration - trying to calibrate from images...")
            if not processor.calibrate():
                print("⚠ Calibration failed - attempting reconstruction anyway...")
        
        # Reconstruct
        if not processor.reconstruct_3d():
            print("✗ Reconstruction failed")
            return 1
        
        # Export STL
        output_stl = os.path.join(base_dir, "reconstruction_output.stl")
        if not processor.export_stl(output_stl):
            print("✗ Export failed")
            return 1
        
        # Summary
        processor.print_summary()
        print(f"✓ Complete workflow finished successfully!")
        print(f"Output file: {output_stl}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
