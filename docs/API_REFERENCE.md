# JScaner - Development API Reference

## Core Classes and Methods

### ImageCapture Class
```python
class ImageCapture:
    def __init__(self, camera_id: int = 0)
    def diagnose_camera_issues() -> None
    def initialize_camera() -> bool
    def get_frame() -> Optional[np.ndarray]
    def capture_image(save_path: Optional[str] = None) -> Optional[np.ndarray]
    def capture_sequence(num_images: int, delay_seconds: float = 2.0, 
                        save_directory: Optional[str] = None) -> List[np.ndarray]
    def preview_camera(window_name: str = "Camera Preview") -> List[np.ndarray]
    def get_camera_info() -> dict
    def detect_c920() -> bool
    def optimize_for_3d_scanning() -> None
    def is_camera_truly_active() -> bool
    def release() -> None
```

### GridDetector Class
```python
class GridDetector:
    def __init__(self, grid_size_mm: Tuple[float, float] = (10.0, 10.0))
    def detect_grid(image: np.ndarray, grid_pattern: Tuple[int, int] = (9, 6)) -> Optional[np.ndarray]
    def generate_3d_points(grid_pattern: Tuple[int, int]) -> np.ndarray
    def calibrate_camera(images: List[np.ndarray], grid_pattern: Tuple[int, int] = (9, 6)) -> Dict
    def save_calibration(calibration: Dict, filename: str) -> None
    def load_calibration(filename: str) -> Dict
```

### StereoReconstructor Class
```python
class StereoReconstructor:
    def __init__()
    def load_calibration(calibration: Dict) -> None
    def detect_features(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]
    def match_features(desc1: np.ndarray, desc2: np.ndarray, 
                      ratio_threshold: float = 0.7) -> List[cv2.DMatch]
    def estimate_pose(kp1: List, kp2: List, matches: List[cv2.DMatch]) -> Tuple[np.ndarray, np.ndarray]
    def triangulate_points(kp1: List, kp2: List, matches: List[cv2.DMatch], 
                          R: np.ndarray, t: np.ndarray) -> np.ndarray
    def reconstruct_from_images(images: List[np.ndarray]) -> object  # Open3D or fallback
    def generate_mesh(point_cloud: object, 
                     method: str = "poisson") -> Optional[object]  # Open3D or fallback
```

### Point3DReconstruction Class (Fallback)
```python
class Point3DReconstruction:
    def __init__()
    def triangulate_points_stereo(points1: np.ndarray, points2: np.ndarray,
                                camera_matrix1: np.ndarray, camera_matrix2: np.ndarray,
                                R: np.ndarray, t: np.ndarray) -> np.ndarray
    def triangulate_from_multiple_views(image_points: List[np.ndarray],
                                      camera_matrices: List[np.ndarray],
                                      poses: List[Tuple[np.ndarray, np.ndarray]]) -> np.ndarray
    def filter_outlier_points(points: np.ndarray, nb_neighbors: int = 20,
                            std_ratio: float = 2.0) -> np.ndarray
    def create_point_cloud(points: np.ndarray, colors: Optional[np.ndarray] = None)
    def estimate_normals(points: np.ndarray, k_neighbors: int = 30) -> np.ndarray
    def create_mesh_poisson(points: np.ndarray, normals: Optional[np.ndarray] = None,
                          depth: int = 9) -> Optional[object]
    def create_mesh_alpha_shape(points: np.ndarray, alpha: float = 0.1) -> Optional[object]
    def save_point_cloud_ply(filename: str, points: np.ndarray, 
                           colors: Optional[np.ndarray] = None)
    def save_mesh_ply(filename: str, vertices: np.ndarray, 
                     faces: np.ndarray, colors: Optional[np.ndarray] = None)
```

### STLExporter Class (Enhanced with Fallback Support)
```python
class STLExporter:
    def __init__()
    def export_mesh_to_stl(mesh: object,  # Open3D or fallback mesh
                          filename: str, scale_factor: float = 1.0,
                          ascii_format: bool = False) -> bool
    def export_point_cloud(points: np.ndarray, filename: str, 
                          colors: Optional[np.ndarray] = None,
                          format: str = "ply") -> bool
    def validate_mesh(mesh: object) -> bool
    def get_mesh_info(mesh: object) -> dict
    
    # Fallback methods (when Open3D unavailable)
    def _export_fallback_mesh(mesh: object, filename: str, 
                             scale_factor: float, ascii_format: bool) -> bool
    def _export_xyz(points: np.ndarray, filename: str) -> bool
```

### GPU Acceleration Class
```python
class GPUAccelerator:
    def __init__()
    def is_available() -> bool
    def get_device_info() -> dict
    def process_image_gpu(image: np.ndarray, operation: str) -> np.ndarray
    def harris_corners_gpu(image: np.ndarray, k: float = 0.04, 
                          threshold: float = 0.01) -> np.ndarray
    def gaussian_blur_gpu(image: np.ndarray, sigma: float) -> np.ndarray
    def memory_info() -> dict
```

## Configuration Examples

### Camera Initialization
```python
from src.core.image_capture import ImageCapture

# Initialize camera
camera = ImageCapture()
if camera.initialize_camera():
    print("Camera ready")
    
    # Optimize for scanning
    camera.optimize_for_3d_scanning()
    
    # Capture sequence
    images = camera.capture_sequence(num_images=8, delay_seconds=3.0)
    
    camera.release()
```

### Calibration Workflow
```python
from src.core.grid_calibration import GridDetector

# Setup calibration
detector = GridDetector(grid_size_mm=(10.0, 10.0))

# Perform calibration
calibration_data = detector.calibrate_camera(images, grid_pattern=(9, 6))

# Save for future use
detector.save_calibration(calibration_data, "calibration.json")
```

### 3D Reconstruction
```python
from src.core.reconstruction import StereoReconstructor

# Setup reconstructor
reconstructor = StereoReconstructor()
reconstructor.load_calibration(calibration_data)

# Reconstruct 3D model
point_cloud = reconstructor.reconstruct_from_images(captured_images)
mesh = reconstructor.generate_mesh(point_cloud, method="poisson")
```

### STL Export
```python
from src.core.stl_export import STLExporter

# Setup exporter
exporter = STLExporter()

# Optimize and export
optimized_mesh = exporter.optimize_mesh_for_printing(mesh, target_triangle_count=50000)
scaled_mesh = exporter.scale_to_print_size(optimized_mesh, target_size_mm=50.0)

# Export STL
success = exporter.export_mesh_to_stl(scaled_mesh, "output.stl")

# Validate result
is_valid, info = exporter.validate_stl_file("output.stl")
```

## Error Handling Patterns

### Camera Diagnostics
```python
# Run diagnostics
camera.diagnose_camera_issues()

# Check camera status
if not camera.is_camera_truly_active():
    print("Camera not properly activated")
    
# Get detailed info
info = camera.get_camera_info()
print(f"Resolution: {info['width']}x{info['height']}")
print(f"C920 Compatible: {info['is_c920_compatible']}")
```

### Calibration Validation
```python
# Check calibration quality
reprojection_error = calibration_data['reprojection_error']
if reprojection_error > 1.0:
    print("Warning: High calibration error")

# Verify sufficient calibration images
if len(calibration_images) < 5:
    print("Need more calibration images for accuracy")
```

### Mesh Quality Assessment
```python
# Validate mesh before export
is_valid, mesh_info = exporter.validate_stl_file("output.stl")

if not is_valid:
    print("Mesh validation failed")
else:
    print(f"Mesh volume: {mesh_info['volume']} cubic units")
    print(f"Surface area: {mesh_info['surface_area']}")
    print(f"Vertices: {mesh_info['vertices']}")
    print(f"Faces: {mesh_info['faces']}")
```

## Performance Optimization

### Memory Management
```python
# Clear large objects when done
del captured_images
del point_cloud
import gc
gc.collect()
```

### Processing Efficiency
```python
# Reduce point cloud size for faster processing
point_cloud = point_cloud.voxel_down_sample(voxel_size=0.01)

# Simplify mesh for printing
simplified_mesh = exporter.optimize_mesh_for_printing(
    mesh, target_triangle_count=20000
)
```

## Integration Examples

### Batch Processing
```python
import os
from pathlib import Path

def process_image_directory(image_dir: str, output_dir: str):
    """Process all images in directory for 3D reconstruction."""
    
    # Load calibration
    detector = GridDetector()
    calibration = detector.load_calibration("calibration.json")
    
    # Setup reconstructor
    reconstructor = StereoReconstructor()
    reconstructor.load_calibration(calibration)
    
    # Process images
    image_files = list(Path(image_dir).glob("*.jpg"))
    images = [cv2.imread(str(f)) for f in image_files]
    
    # Reconstruct
    point_cloud = reconstructor.reconstruct_from_images(images)
    mesh = reconstructor.generate_mesh(point_cloud)
    
    # Export
    exporter = STLExporter()
    output_path = os.path.join(output_dir, "reconstruction.stl")
    exporter.export_mesh_to_stl(mesh, output_path)
```

### Custom Grid Patterns
```python
# Define custom calibration grid
custom_detector = GridDetector(grid_size_mm=(5.0, 5.0))  # 5mm squares

# Use different pattern size
calibration = custom_detector.calibrate_camera(
    images, grid_pattern=(11, 8)  # 11x8 instead of 9x6
)
```