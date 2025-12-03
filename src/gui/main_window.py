"""
Main GUI Application Window

Provides user interface for the 3D Object Scanner application.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import os
import json

# Import core modules
from core.image_capture import ImageCapture
from core.grid_calibration import GridDetector
from core.reconstruction import StereoReconstructor
from core.stl_export import STLExporter

class MainApplication:
    """Main application window for JScaner."""
    
    def __init__(self):
        """Initialize the main application."""
        self.root = tk.Tk()
        self.root.title("JScaner")
        self.root.geometry("1000x700")
        
        # Core components
        self.image_capture = ImageCapture()
        self.grid_detector = GridDetector()
        self.reconstructor = StereoReconstructor()
        self.stl_exporter = STLExporter()
        
        # Application state
        self.captured_images = []
        self.calibration_data = None
        self.current_frame = None
        self.is_camera_active = False
        self.point_cloud = None
        self.current_photo = None  # Keep reference to current photo
        
        # Data directories
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        self.captured_dir = os.path.join(self.data_dir, 'captured')
        self.calibration_file = os.path.join(self.data_dir, 'last_calibration.json')
        
        # Ensure directories exist
        os.makedirs(self.captured_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Setup UI
        self.create_widgets()
        self.setup_layout()
        
        # Auto-load last calibration
        self.auto_load_calibration()
        
        # Auto-start Kinect on startup (prefer Kinect over webcam)
        self.root.after(500, self.auto_start_kinect)
        
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        
        # Tab 1: Camera and Capture
        self.capture_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.capture_frame, text="Capture")
        
        # Tab 2: Calibration
        self.calibration_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.calibration_frame, text="Calibration")
        
        # Tab 3: Reconstruction
        self.reconstruction_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.reconstruction_frame, text="3D Reconstruction")
        
        # Tab 4: Export
        self.export_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.export_frame, text="Export STL")
        
        # Create widgets for each tab
        self.create_capture_widgets()
        self.create_calibration_widgets()
        self.create_reconstruction_widgets()
        self.create_export_widgets()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, anchor=tk.W)
    
    def create_capture_widgets(self):
        """Create widgets for the capture tab."""
        # Camera selection frame (NEW)
        camera_select_frame = ttk.LabelFrame(self.capture_frame, text="Camera Selection")
        camera_select_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        ttk.Label(camera_select_frame, text="Select Camera:").pack(side=tk.LEFT, padx=5, pady=5)
        
        self.camera_var = tk.StringVar(value="kinect")
        ttk.Radiobutton(camera_select_frame, text="📷 Logitech Webcam", variable=self.camera_var, 
                       value="webcam", command=self.on_camera_selection_changed).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(camera_select_frame, text="🎮 Xbox Kinect v1", variable=self.camera_var, 
                       value="kinect", command=self.on_camera_selection_changed).pack(side=tk.LEFT, padx=5)
        
        # Camera preview frame
        camera_frame = ttk.LabelFrame(self.capture_frame, text="Camera Preview")
        camera_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        self.camera_label = ttk.Label(camera_frame, text="Camera not initialized")
        self.camera_label.pack(padx=10, pady=10)
        
        # Control buttons
        control_frame = ttk.LabelFrame(self.capture_frame, text="Controls")
        control_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        ttk.Button(control_frame, text="Start Camera", 
                  command=self.start_camera).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Stop Camera", 
                  command=self.stop_camera).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Capture Image", 
                  command=self.capture_single_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Load Images", 
                  command=self.load_external_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Clear Images", 
                  command=self.clear_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Show Save Location", 
                  command=self.show_save_location).pack(side=tk.LEFT, padx=5)
        
        # Captured images list
        images_frame = ttk.LabelFrame(self.capture_frame, text="Captured Images")
        images_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        
        self.images_listbox = tk.Listbox(images_frame, height=10)
        self.images_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configure grid weights
        self.capture_frame.columnconfigure(0, weight=2)
        self.capture_frame.columnconfigure(1, weight=1)
        self.capture_frame.rowconfigure(1, weight=1)
    
    def create_calibration_widgets(self):
        """Create widgets for the calibration tab."""
        # Grid settings
        settings_frame = ttk.LabelFrame(self.calibration_frame, text="Grid Settings")
        settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ttk.Label(settings_frame, text="Grid Square Size (mm):").grid(row=0, column=0, padx=5, pady=5)
        self.grid_size_var = tk.StringVar(value="10.0")
        ttk.Entry(settings_frame, textvariable=self.grid_size_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(settings_frame, text="Grid Pattern (cols x rows):").grid(row=1, column=0, padx=5, pady=5)
        self.grid_cols_var = tk.StringVar(value="9")
        self.grid_rows_var = tk.StringVar(value="6")
        ttk.Entry(settings_frame, textvariable=self.grid_cols_var, width=5).grid(row=1, column=1, padx=2, pady=5)
        ttk.Label(settings_frame, text="x").grid(row=1, column=2, padx=2, pady=5)
        ttk.Entry(settings_frame, textvariable=self.grid_rows_var, width=5).grid(row=1, column=3, padx=2, pady=5)
        
        # Calibration controls
        calib_frame = ttk.LabelFrame(self.calibration_frame, text="Calibration")
        calib_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        ttk.Button(calib_frame, text="Calibrate Camera", 
                  command=self.calibrate_camera).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(calib_frame, text="Analyze Grid Patterns", 
                  command=self.analyze_grid_patterns).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(calib_frame, text="Load Calibration", 
                  command=self.load_calibration).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(calib_frame, text="Save Calibration", 
                  command=self.save_calibration).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Calibration status
        self.calib_status_var = tk.StringVar()
        self.calib_status_var.set("Not calibrated")
        ttk.Label(self.calibration_frame, textvariable=self.calib_status_var).grid(row=2, column=0, padx=10, pady=10)
    
    def create_reconstruction_widgets(self):
        """Create widgets for the reconstruction tab."""
        # Reconstruction controls
        recon_frame = ttk.LabelFrame(self.reconstruction_frame, text="3D Reconstruction")
        recon_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ttk.Button(recon_frame, text="Reconstruct 3D Model", 
                  command=self.reconstruct_3d).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(recon_frame, text="View Point Cloud", 
                  command=self.view_point_cloud).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Reconstruction parameters
        params_frame = ttk.LabelFrame(self.reconstruction_frame, text="Parameters")
        params_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        ttk.Label(params_frame, text="Feature Matching Threshold:").grid(row=0, column=0, padx=5, pady=5)
        self.match_threshold_var = tk.StringVar(value="0.7")
        ttk.Entry(params_frame, textvariable=self.match_threshold_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        
        # Progress and status
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.reconstruction_frame, variable=self.progress_var)
        self.progress_bar.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.recon_status_var = tk.StringVar()
        self.recon_status_var.set("No reconstruction performed")
        ttk.Label(self.reconstruction_frame, textvariable=self.recon_status_var).grid(row=3, column=0, padx=10, pady=5)
    
    def create_export_widgets(self):
        """Create widgets for the export tab."""
        # Export controls
        export_controls = ttk.LabelFrame(self.export_frame, text="Export Settings")
        export_controls.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ttk.Label(export_controls, text="Scale Factor:").grid(row=0, column=0, padx=5, pady=5)
        self.scale_var = tk.StringVar(value="1.0")
        ttk.Entry(export_controls, textvariable=self.scale_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(export_controls, text="Target Size (mm):").grid(row=1, column=0, padx=5, pady=5)
        self.target_size_var = tk.StringVar(value="50.0")
        ttk.Entry(export_controls, textvariable=self.target_size_var, width=10).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(export_controls, text="Export STL", 
                  command=self.export_stl).grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        
        # Export status
        self.export_status_var = tk.StringVar()
        self.export_status_var.set("No model to export")
        ttk.Label(self.export_frame, textvariable=self.export_status_var).grid(row=1, column=0, padx=10, pady=10)
    
    def setup_layout(self):
        """Setup the main layout."""
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Configure main grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def auto_start_kinect(self):
        """Automatically start Kinect v1 on application startup."""
        print("Auto-starting Kinect v1...")
        self.camera_var.set("kinect")
        self.start_camera()
    
    def on_camera_selection_changed(self):
        """Handle camera selection change."""
        selected = self.camera_var.get()
        was_active = self.is_camera_active
        
        if was_active:
            self.stop_camera()
        
        use_kinect = (selected == "kinect")
        success = self.image_capture.switch_camera(use_kinect)
        
        if success:
            camera_name = "Xbox Kinect v1" if use_kinect else "Logitech Webcam"
            self.status_var.set(f"📷 Camera switched to {camera_name}")
            if was_active:
                self.start_camera()
        else:
            camera_name = "Xbox Kinect v1" if use_kinect else "Logitech Webcam"
            self.status_var.set(f"⚠ Failed to switch to {camera_name}")
            messagebox.showwarning("Camera Switch Failed", 
                f"Could not switch to {camera_name}.\n\n"
                "Make sure the camera is connected and not in use by another application.")
    
    def start_camera(self):
        """Start camera preview."""
        # Run diagnostics first
        self.image_capture.diagnose_camera_issues()
        
        # Ensure camera is set to the selected one
        selected = self.camera_var.get()
        use_kinect = (selected == "kinect")
        
        # If camera type doesn't match selection, switch it
        if use_kinect and not self.image_capture.kinect_active:
            if not self.image_capture.switch_camera(use_kinect):
                self.status_var.set("⚠ Kinect not available, using webcam")
        elif not use_kinect and self.image_capture.kinect_active:
            if not self.image_capture.switch_camera(use_kinect):
                self.status_var.set("⚠ Failed to switch to webcam")
        
        # Initialize camera
        if self.image_capture.initialize_camera():
            self.is_camera_active = True
            self.update_camera_preview()
            
            # Show camera type
            camera_type = self.image_capture.get_camera_type()
            self.status_var.set(f"Camera started - {camera_type}")
            
            # Check if using Kinect
            if camera_type == "Kinect v1":
                self.status_var.set("✓ Kinect v1 activated - RGB enabled!")
            # Check if C920 compatible
            elif hasattr(self.image_capture, 'get_camera_info'):
                camera_info = self.image_capture.get_camera_info()
                if camera_info.get('is_c920_compatible'):
                    self.status_var.set("Camera started - C920 optimized")
                    self.image_capture.optimize_for_3d_scanning()
        else:
            self.status_var.set("Camera failed to start - check diagnostics")
            messagebox.showerror("Camera Error", 
                "Failed to initialize camera.\n\n"
                "Check the terminal output for diagnostics.\n\n"
                "Common fixes:\n"
                "• Close other camera apps (Skype, Teams, etc.)\n"
                "• Unplug and reconnect camera\n"
                "• Try Windows Camera app first")
    
    def stop_camera(self):
        """Stop camera preview."""
        self.is_camera_active = False
        self.image_capture.release()
        self.camera_label.config(image="", text="Camera stopped")
        self.status_var.set("Camera stopped")
    
    def update_camera_preview(self):
        """Update camera preview in GUI."""
        if self.is_camera_active:
            frame = self.image_capture.get_frame()
            if frame is not None:
                # Resize frame for display
                display_frame = cv2.resize(frame, (640, 480))
                display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
                
                # Convert to PhotoImage
                image = Image.fromarray(display_frame)
                photo = ImageTk.PhotoImage(image)
                
                self.camera_label.config(image=photo, text="")
                self.current_photo = photo  # Keep a reference
                
                self.current_frame = frame
            
            # Schedule next update
            self.root.after(50, self.update_camera_preview)
    
    def capture_single_image(self):
        """Capture a single image with optional custom naming."""
        if self.current_frame is None:
            messagebox.showwarning("Warning", "No camera frame available. Make sure camera is started.")
            return
        
        # Capture the frame immediately
        captured_frame = self.current_frame.copy()
        
        # Ask if user wants to name the file
        name_dialog = tk.Toplevel(self.root)
        name_dialog.title("Name Image")
        name_dialog.geometry("400x180")
        name_dialog.transient(self.root)
        name_dialog.grab_set()
        
        tk.Label(name_dialog, text="Enter custom name (or leave blank for auto-naming):", 
                font=("Arial", 9)).pack(pady=10)
        
        name_entry = tk.Entry(name_dialog, width=40)
        name_entry.pack(pady=5)
        name_entry.focus()
        
        def save_image():
            custom_name = name_entry.get().strip()
            
            # Generate filename
            if custom_name:
                filename = f"{custom_name}.png"
            else:
                filename = f"image_{len(self.captured_images)+1:03d}.png"
            
            # Save to disk
            filepath = os.path.join(self.captured_dir, filename)
            success = cv2.imwrite(filepath, captured_frame)
            
            if success:
                # Store image with metadata
                img_data = {
                    'image': captured_frame,
                    'source': 'camera',
                    'filepath': filepath,
                    'purpose': 'processing'
                }
                self.captured_images.append(img_data)
                
                # Update UI
                self.images_listbox.insert(tk.END, filename)
                self.status_var.set(f"Saved: {filename} ({len(self.captured_images)} images)")
            else:
                messagebox.showerror("Error", f"Failed to save image to {filepath}")
            
            name_dialog.destroy()
        
        def cancel():
            name_dialog.destroy()
        
        btn_frame = tk.Frame(name_dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Save", command=save_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=cancel).pack(side=tk.LEFT, padx=5)
        
        # Allow Enter key to save
        name_entry.bind('<Return>', lambda e: save_image())
        name_entry.bind('<Escape>', lambda e: cancel())
    
    def clear_images(self):
        """Clear all captured images."""
        self.captured_images.clear()
        self.images_listbox.delete(0, tk.END)
        self.status_var.set("Images cleared")
    
    def calibrate_camera(self):
        """Perform camera calibration using captured images."""
        if len(self.captured_images) < 3:
            messagebox.showwarning("Warning", "Need at least 3 images for calibration")
            return
        
        try:
            # Get grid parameters
            grid_size = float(self.grid_size_var.get())
            grid_cols = int(self.grid_cols_var.get())
            grid_rows = int(self.grid_rows_var.get())
            
            self.grid_detector = GridDetector((grid_size, grid_size))
            
            # Extract images from metadata structure
            images = []
            for item in self.captured_images:
                if isinstance(item, dict) and 'image' in item:
                    images.append(item['image'])
                else:
                    images.append(item)
            
            # Perform calibration
            self.status_var.set("Calibrating camera...")
            self.calibration_data = self.grid_detector.calibrate_camera(
                images, (grid_cols, grid_rows)
            )
            
            # Load calibration into reconstructor
            self.reconstructor.load_calibration(self.calibration_data)
            
            self.calib_status_var.set(f"Calibrated (error: {self.calibration_data['reprojection_error']:.2f})")
            self.status_var.set("Camera calibration completed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Calibration failed: {e}")
            self.status_var.set("Calibration failed")
    
    def analyze_grid_patterns(self):
        """Analyze captured images to find possible grid patterns."""
        if not self.captured_images:
            messagebox.showwarning("Warning", "No captured images to analyze")
            return
        
        try:
            # Extract first image from metadata structure
            first_item = self.captured_images[0]
            first_image = first_item['image'] if isinstance(first_item, dict) and 'image' in first_item else first_item
            
            # Analyze the first image
            patterns = self.grid_detector.analyze_grid_patterns(first_image)
            
            if patterns:
                pattern_text = "\n".join([f"- {p[0]}x{p[1]} inner corners" for p in patterns])
                message = f"Detected grid patterns in first image:\n\n{pattern_text}\n\nTry using one of these patterns for calibration."
                messagebox.showinfo("Grid Pattern Analysis", message)
                
                # Auto-set the first detected pattern
                if patterns:
                    self.grid_cols_var.set(str(patterns[0][0]))
                    self.grid_rows_var.set(str(patterns[0][1]))
            else:
                messagebox.showwarning("No Grid Patterns Found", 
                    "No standard checkerboard patterns detected.\n\n"
                    "Make sure your images contain:\n"
                    "- Clear black and white checkerboard pattern\n"
                    "- Good contrast and lighting\n"
                    "- Grid is flat and not distorted\n"
                    "- Grid takes up a significant portion of the image")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Pattern analysis failed: {e}")
    
    def load_calibration(self):
        """Load calibration data from file."""
        filename = filedialog.askopenfilename(
            title="Load Calibration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.calibration_data = self.grid_detector.load_calibration(filename)
                self.reconstructor.load_calibration(self.calibration_data)
                self.calib_status_var.set("Calibration loaded")
                self.status_var.set("Calibration data loaded")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load calibration: {e}")
    
    def save_calibration(self):
        """Save calibration data to file."""
        if self.calibration_data is None:
            messagebox.showwarning("Warning", "No calibration data to save")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save Calibration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile="calibration.json"
        )
        
        if filename:
            try:
                self.grid_detector.save_calibration(self.calibration_data, filename)
                
                # Also save as last calibration for auto-load
                self.grid_detector.save_calibration(self.calibration_data, self.calibration_file)
                
                self.status_var.set("Calibration data saved")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save calibration: {e}")
    
    def reconstruct_3d(self):
        """Perform 3D reconstruction."""
        if len(self.captured_images) < 2:
            messagebox.showwarning("Warning", "Need at least 2 images for reconstruction")
            return
        
        if self.calibration_data is None:
            messagebox.showwarning("Warning", "Camera calibration required")
            return
        
        def reconstruction_thread():
            try:
                self.recon_status_var.set("Reconstructing...")
                self.progress_var.set(0)
                
                # Extract images from metadata structure
                images = []
                for item in self.captured_images:
                    if isinstance(item, dict) and 'image' in item:
                        images.append(item['image'])
                    else:
                        images.append(item)
                
                # Perform reconstruction
                self.point_cloud = self.reconstructor.reconstruct_from_images(images)
                
                # Get point count (handle both Open3D and fallback)
                if hasattr(self.point_cloud, 'points'):
                    point_count = len(self.point_cloud.points)
                elif hasattr(self.point_cloud, 'points_3d') and self.point_cloud.points_3d is not None:
                    point_count = len(self.point_cloud.points_3d)
                else:
                    point_count = 0
                
                self.progress_var.set(100)
                self.recon_status_var.set(f"Reconstruction complete ({point_count} points)")
                self.status_var.set("3D reconstruction completed")
                
            except Exception as e:
                self.recon_status_var.set(f"Reconstruction failed: {e}")
                self.status_var.set("Reconstruction failed")
        
        # Run reconstruction in separate thread
        threading.Thread(target=reconstruction_thread, daemon=True).start()
    
    def view_point_cloud(self):
        """Display point cloud in 3D viewer."""
        if hasattr(self, 'point_cloud'):
            try:
                # Try Open3D visualization if available
                try:
                    import open3d as o3d
                    if hasattr(self.point_cloud, 'points') and hasattr(o3d.geometry, 'PointCloud'):
                        o3d.visualization.draw_geometries([self.point_cloud])
                        return
                except ImportError:
                    pass
                
                # Fallback: Use matplotlib for 3D visualization
                import matplotlib.pyplot as plt
                from mpl_toolkits.mplot3d import Axes3D
                
                # Get points from either Open3D or fallback format
                if hasattr(self.point_cloud, 'points'):
                    points = self.point_cloud.points
                elif hasattr(self.point_cloud, 'points_3d'):
                    points = self.point_cloud.points_3d
                else:
                    messagebox.showerror("Error", "Unknown point cloud format")
                    return
                
                if points is None or len(points) == 0:
                    messagebox.showwarning("Warning", "Point cloud is empty")
                    return
                
                # Create 3D plot
                fig = plt.figure(figsize=(10, 8))
                ax = fig.add_subplot(111, projection='3d')
                
                # Plot points
                ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
                          c=points[:, 2], cmap='viridis', marker='.', s=1)
                
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.set_title(f'Point Cloud ({len(points)} points)')
                
                plt.show()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to display point cloud: {e}")
        else:
            messagebox.showwarning("Warning", "No point cloud available")
    
    def export_stl(self):
        """Export 3D model to STL file."""
        if not hasattr(self, 'point_cloud'):
            messagebox.showwarning("Warning", "No 3D model available for export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export STL",
            defaultextension=".stl",
            filetypes=[("STL files", "*.stl"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                scale_factor = float(self.scale_var.get())
                
                success = self.stl_exporter.export_point_cloud_to_stl(
                    self.point_cloud, filename, scale_factor=scale_factor
                )
                
                if success:
                    self.export_status_var.set("STL exported successfully")
                    self.status_var.set(f"STL exported to {os.path.basename(filename)}")
                else:
                    self.export_status_var.set("Export failed")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")
                self.export_status_var.set("Export failed")
    
    def run(self):
        """Start the application."""
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start main loop
        self.root.mainloop()
    
    def on_closing(self):
        """Handle application closing."""
        self.stop_camera()
        self.root.destroy()
    
    def auto_load_calibration(self):
        """Automatically load the last saved calibration on startup."""
        # Check for cal.json in root directory first (legacy location)
        root_cal = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'cal.json')
        
        calibration_path = None
        if os.path.exists(root_cal):
            calibration_path = root_cal
        elif os.path.exists(self.calibration_file):
            calibration_path = self.calibration_file
        
        if calibration_path:
            try:
                with open(calibration_path, 'r') as f:
                    self.calibration_data = json.load(f)
                
                # Load calibration into reconstructor
                if self.calibration_data:
                    self.reconstructor.load_calibration(self.calibration_data)
                
                self.calib_status_var.set(f"Calibration loaded (error: {self.calibration_data.get('reprojection_error', 'N/A'):.2f})")
                self.status_var.set(f"Calibration auto-loaded from {os.path.basename(calibration_path)}")
            except Exception as e:
                self.status_var.set(f"Failed to auto-load calibration: {e}")
    
    def load_external_images(self):
        """Load images from external source with purpose selection."""
        filepaths = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if not filepaths:
            return
        
        # Ask purpose
        purpose_dialog = tk.Toplevel(self.root)
        purpose_dialog.title("Select Purpose")
        purpose_dialog.geometry("300x150")
        purpose_dialog.transient(self.root)
        purpose_dialog.grab_set()
        
        selected_purpose = tk.StringVar(value="processing")
        
        tk.Label(purpose_dialog, text="What are these images for?", 
                font=("Arial", 10, "bold")).pack(pady=10)
        
        tk.Radiobutton(purpose_dialog, text="3D Reconstruction (Processing)", 
                      variable=selected_purpose, value="processing").pack(anchor=tk.W, padx=20)
        tk.Radiobutton(purpose_dialog, text="Camera Calibration", 
                      variable=selected_purpose, value="calibration").pack(anchor=tk.W, padx=20)
        
        def confirm_purpose():
            purpose = selected_purpose.get()
            purpose_dialog.destroy()
            
            # Load images
            loaded_count = 0
            for filepath in filepaths:
                try:
                    img = cv2.imread(filepath)
                    if img is not None:
                        # Store with metadata
                        img_data = {
                            'image': img,
                            'source': 'external',
                            'original_path': filepath,
                            'purpose': purpose
                        }
                        self.captured_images.append(img_data)
                        
                        # Add to listbox with indicator
                        filename = os.path.basename(filepath)
                        self.images_listbox.insert(tk.END, f"[EXT] {filename}")
                        loaded_count += 1
                except Exception as e:
                    print(f"Failed to load {filepath}: {e}")
            
            self.status_var.set(f"Loaded {loaded_count} images for {purpose}")
        
        ttk.Button(purpose_dialog, text="Confirm", command=confirm_purpose).pack(pady=10)
        
        purpose_dialog.wait_window()
    
    def show_save_location(self):
        """Show the location where captured images are saved."""
        location_dialog = tk.Toplevel(self.root)
        location_dialog.title("Image Save Location")
        location_dialog.geometry("600x200")
        location_dialog.transient(self.root)
        
        tk.Label(location_dialog, text="Captured images are saved in:", 
                font=("Arial", 10, "bold")).pack(pady=10)
        
        # Display path
        path_frame = tk.Frame(location_dialog)
        path_frame.pack(fill=tk.X, padx=20, pady=5)
        
        path_text = tk.Text(path_frame, height=2, wrap=tk.WORD)
        path_text.pack(fill=tk.X)
        path_text.insert("1.0", self.captured_dir)
        path_text.config(state=tk.DISABLED)
        
        # Buttons
        btn_frame = tk.Frame(location_dialog)
        btn_frame.pack(pady=10)
        
        def open_folder():
            if os.path.exists(self.captured_dir):
                os.startfile(self.captured_dir)
        
        def copy_path():
            self.root.clipboard_clear()
            self.root.clipboard_append(self.captured_dir)
            self.status_var.set("Path copied to clipboard")
        
        ttk.Button(btn_frame, text="Open Folder", command=open_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Copy Path", command=copy_path).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=location_dialog.destroy).pack(side=tk.LEFT, padx=5)