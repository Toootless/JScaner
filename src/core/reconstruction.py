"""
3D Reconstruction Module

Implements algorithms for reconstructing 3D point clouds and meshes from multiple images.
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional, Dict
import scipy.spatial.distance as distance

# Try to import Open3D, fall back to alternative implementation
try:
    import open3d as o3d
    HAS_OPEN3D = True
    print("Open3D available for 3D reconstruction")
except ImportError:
    HAS_OPEN3D = False
    print("Open3D not available, using fallback reconstruction methods")
    from .reconstruction_fallback import create_reconstruction_engine

class StereoReconstructor:
    """Handles 3D reconstruction from stereo image pairs."""
    
    def __init__(self):
        """Initialize stereo reconstruction parameters."""
        self.calibration_data = None
        
    def load_calibration(self, calibration: Dict):
        """Load camera calibration data."""
        # Convert lists to numpy arrays if needed
        if calibration:
            self.calibration_data = {
                'camera_matrix': np.array(calibration['camera_matrix'], dtype=np.float64),
                'distortion_coefficients': np.array(calibration['distortion_coefficients'], dtype=np.float64).reshape(-1),
                'reprojection_error': calibration.get('reprojection_error', 0),
                'image_size': calibration.get('image_size', [1920, 1080]),
                'grid_size_mm': calibration.get('grid_size_mm', [55.0, 55.0])
            }
        else:
            self.calibration_data = calibration
    
    def detect_features(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect keypoints and descriptors in image using SIFT.
        
        Args:
            image: Input image
            
        Returns:
            Tuple of (keypoints, descriptors)
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Initialize SIFT detector
        sift = cv2.SIFT_create()
        
        # Detect keypoints and compute descriptors
        keypoints, descriptors = sift.detectAndCompute(gray, None)
        
        return keypoints, descriptors
    
    def match_features(self, desc1: np.ndarray, desc2: np.ndarray, 
                      ratio_threshold: float = 0.7) -> List[cv2.DMatch]:
        """
        Match features between two images using FLANN matcher.
        
        Args:
            desc1: Descriptors from first image
            desc2: Descriptors from second image
            ratio_threshold: Lowe's ratio test threshold
            
        Returns:
            List of good matches
        """
        # FLANN parameters
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        
        # Initialize FLANN matcher
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        
        # Find matches
        matches = flann.knnMatch(desc1, desc2, k=2)
        
        # Apply Lowe's ratio test
        good_matches = []
        for match_pair in matches:
            if len(match_pair) == 2:
                m, n = match_pair
                if m.distance < ratio_threshold * n.distance:
                    good_matches.append(m)
        
        return good_matches
    
    def estimate_pose(self, kp1: List, kp2: List, matches: List[cv2.DMatch]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Estimate relative pose between two camera views.
        
        Args:
            kp1: Keypoints from first image
            kp2: Keypoints from second image
            matches: Feature matches between images
            
        Returns:
            Tuple of (rotation_matrix, translation_vector)
        """
        if self.calibration_data is None:
            raise ValueError("Camera calibration data not loaded")
        
        # Extract matched point coordinates
        pts1 = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        pts2 = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        
        # Find essential matrix
        camera_matrix = np.array(self.calibration_data['camera_matrix'], dtype=np.float64)
        dist_coeffs = np.array(self.calibration_data['distortion_coefficients'], dtype=np.float64).reshape(-1)
        
        # Extract focal length and principal point
        focal = camera_matrix[0, 0]
        pp = (camera_matrix[0, 2], camera_matrix[1, 2])
        
        E, mask = cv2.findEssentialMat(pts1, pts2, 
                                       focal=focal, 
                                       pp=pp,
                                       method=cv2.RANSAC, 
                                       prob=0.999, 
                                       threshold=1.0)
        
        # Recover pose from essential matrix
        _, R, t, mask = cv2.recoverPose(E, pts1, pts2, camera_matrix)
        
        return R, t
    
    def triangulate_points(self, kp1: List, kp2: List, matches: List[cv2.DMatch], 
                          R: np.ndarray, t: np.ndarray) -> np.ndarray:
        """
        Triangulate 3D points from matched features.
        
        Args:
            kp1: Keypoints from first image
            kp2: Keypoints from second image
            matches: Feature matches
            R: Rotation matrix between views
            t: Translation vector between views
            
        Returns:
            3D points array
        """
        if self.calibration_data is None:
            raise ValueError("Camera calibration data not loaded")
        
        camera_matrix = self.calibration_data['camera_matrix']
        
        # Create projection matrices
        P1 = camera_matrix @ np.hstack([np.eye(3), np.zeros((3, 1))])
        P2 = camera_matrix @ np.hstack([R, t])
        
        # Extract matched points
        pts1 = np.float32([kp1[m.queryIdx].pt for m in matches]).T
        pts2 = np.float32([kp2[m.trainIdx].pt for m in matches]).T
        
        # Triangulate points
        points_4d = cv2.triangulatePoints(P1, P2, pts1, pts2)
        
        # Convert from homogeneous to 3D coordinates
        points_3d = points_4d[:3] / points_4d[3]
        
        return points_3d.T
    
    def reconstruct_from_images(self, images: List[np.ndarray]) -> Optional['o3d.geometry.PointCloud']:
        """
        Reconstruct 3D point cloud from multiple images.
        
        Args:
            images: List of input images
            
        Returns:
            Open3D point cloud if available, or None
        """
        if not HAS_OPEN3D:
            print("Open3D not available for reconstruction")
            return None
            
        if len(images) < 2:
            raise ValueError("Need at least 2 images for reconstruction")
        
        all_points = []
        
        # Process pairs of consecutive images
        for i in range(len(images) - 1):
            img1, img2 = images[i], images[i + 1]
            
            # Detect features
            kp1, desc1 = self.detect_features(img1)
            kp2, desc2 = self.detect_features(img2)
            
            if desc1 is None or desc2 is None:
                continue
            
            # Match features
            matches = self.match_features(desc1, desc2)
            
            if len(matches) < 50:  # Need sufficient matches
                continue
            
            # Estimate pose
            R, t = self.estimate_pose(kp1, kp2, matches)
            
            # Triangulate points
            points_3d = self.triangulate_points(kp1, kp2, matches, R, t)
            
            # Filter out points that are too far or too close
            distances = np.linalg.norm(points_3d, axis=1)
            valid_mask = (distances > 0.1) & (distances < 10.0)  # Adjust based on object size
            
            if np.any(valid_mask):
                all_points.append(points_3d[valid_mask])
        
        if not all_points:
            raise ValueError("Failed to reconstruct any 3D points")
        
        # Combine all points
        combined_points = np.vstack(all_points)
        
        if HAS_OPEN3D:
            # Create Open3D point cloud
            point_cloud = o3d.geometry.PointCloud()
            point_cloud.points = o3d.utility.Vector3dVector(combined_points)
            
            # Remove outliers
            point_cloud, _ = point_cloud.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
        else:
            # Use fallback implementation
            reconstruction_engine = create_reconstruction_engine()
            filtered_points = reconstruction_engine.filter_outlier_points(combined_points)
            reconstruction_engine.create_point_cloud(filtered_points)
            point_cloud = reconstruction_engine
        
        return point_cloud
    
    def generate_mesh(self, point_cloud: object, 
                     method: str = "poisson") -> Optional[object]:
        """
        Generate mesh from point cloud.
        
        Args:
            point_cloud: Input point cloud (Open3D or fallback)
            method: Reconstruction method ("poisson" or "alpha_shape")
            
        Returns:
            Triangle mesh or None if failed
        """
        if HAS_OPEN3D and hasattr(point_cloud, 'estimate_normals'):
            # Open3D point cloud
            point_cloud.estimate_normals()
            point_cloud.orient_normals_consistent_tangent_plane(100)
            
            if method == "poisson":
                # Poisson surface reconstruction
                mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
                    point_cloud, depth=9
                )
            elif method == "alpha_shape":
                # Alpha shape reconstruction
                alpha = 0.03  # Adjust based on point cloud density
                mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(
                    point_cloud, alpha
                )
            else:
                raise ValueError("Unknown mesh reconstruction method")
            
            # Clean up mesh
            mesh.remove_degenerate_triangles()
            mesh.remove_duplicated_triangles()
            mesh.remove_duplicated_vertices()
            mesh.remove_non_manifold_edges()
            
            return mesh
        else:
            # Fallback implementation
            if hasattr(point_cloud, 'points_3d') and point_cloud.points_3d is not None:
                if method == "poisson":
                    return point_cloud.create_mesh_poisson(point_cloud.points_3d)
                elif method == "alpha_shape":
                    return point_cloud.create_mesh_alpha_shape(point_cloud.points_3d)
            
            return None