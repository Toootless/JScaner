"""
Fallback 3D reconstruction implementation using alternative libraries
for Python 3.14 compatibility (Open3D not available)
"""

import numpy as np
try:
    import trimesh
    HAS_TRIMESH = True
except ImportError:
    HAS_TRIMESH = False

try:
    import pymeshlab
    HAS_PYMESHLAB = True
except ImportError:
    HAS_PYMESHLAB = False

from scipy.spatial.distance import pdist
from scipy.spatial import KDTree, ConvexHull
from sklearn.cluster import DBSCAN
import cv2
from typing import Tuple, List, Optional

class Point3DReconstruction:
    """Alternative 3D reconstruction using triangulation and mesh generation"""
    
    def __init__(self):
        self.has_trimesh = HAS_TRIMESH
        self.has_pymeshlab = HAS_PYMESHLAB
        self.points_3d = None
        self.colors = None
    
    @property
    def points(self):
        """Compatibility property for Open3D interface"""
        return self.points_3d if self.points_3d is not None else np.array([])
        
    def triangulate_points_stereo(self, 
                                points1: np.ndarray, 
                                points2: np.ndarray,
                                camera_matrix1: np.ndarray,
                                camera_matrix2: np.ndarray,
                                R: np.ndarray,
                                t: np.ndarray) -> np.ndarray:
        """
        Triangulate 3D points from stereo correspondences
        """
        # Create projection matrices
        P1 = camera_matrix1 @ np.hstack([np.eye(3), np.zeros((3, 1))])
        P2 = camera_matrix2 @ np.hstack([R, t.reshape(-1, 1)])
        
        # Triangulate points
        points_4d = cv2.triangulatePoints(P1, P2, points1.T, points2.T)
        
        # Convert from homogeneous to 3D coordinates
        points_3d = (points_4d[:3] / points_4d[3]).T
        
        return points_3d
    
    def triangulate_from_multiple_views(self,
                                      image_points: List[np.ndarray],
                                      camera_matrices: List[np.ndarray],
                                      poses: List[Tuple[np.ndarray, np.ndarray]]) -> np.ndarray:
        """
        Triangulate points from multiple camera views
        """
        if len(image_points) < 2:
            raise ValueError("Need at least 2 views for triangulation")
        
        # Use first two views for basic triangulation
        points1 = image_points[0].astype(np.float32)
        points2 = image_points[1].astype(np.float32)
        
        R1, t1 = poses[0]
        R2, t2 = poses[1]
        
        # Relative pose
        R_rel = R2 @ R1.T
        t_rel = t2 - R_rel @ t1
        
        points_3d = self.triangulate_points_stereo(
            points1, points2, 
            camera_matrices[0], camera_matrices[1],
            R_rel, t_rel
        )
        
        return points_3d
    
    def filter_outlier_points(self, points: np.ndarray, 
                            nb_neighbors: int = 20,
                            std_ratio: float = 2.0) -> np.ndarray:
        """
        Filter outlier points using statistical analysis
        """
        if len(points) < nb_neighbors:
            return points
        
        # Build KD-tree for neighbor search
        tree = KDTree(points)
        
        # Calculate distances to neighbors for each point
        distances_list = []
        for point in points:
            distances, _ = tree.query(point, k=nb_neighbors + 1)  # +1 to exclude self
            mean_dist = np.mean(distances[1:])  # Exclude distance to self (0)
            distances_list.append(mean_dist)
        
        distances_array = np.array(distances_list)
        mean_distance = np.mean(distances_array)
        std_distance = np.std(distances_array)
        
        # Filter points based on statistical threshold
        threshold = mean_distance + std_ratio * std_distance
        inlier_mask = distances_array < threshold
        
        return points[inlier_mask]
    
    def create_point_cloud(self, points: np.ndarray, colors: Optional[np.ndarray] = None):
        """
        Store point cloud data
        """
        self.points_3d = points
        self.colors = colors
        
        print(f"Point cloud created with {len(points)} points")
        
        if colors is not None:
            print(f"Colors assigned to {len(colors)} points")
    
    def estimate_normals(self, points: np.ndarray, k_neighbors: int = 30) -> np.ndarray:
        """
        Estimate surface normals for points
        """
        if len(points) < k_neighbors:
            k_neighbors = len(points) - 1
        
        tree = KDTree(points)
        normals = np.zeros_like(points)
        
        for i, point in enumerate(points):
            # Find k nearest neighbors
            _, indices = tree.query(point, k=k_neighbors)
            neighbors = points[indices]
            
            # Compute covariance matrix
            centered = neighbors - np.mean(neighbors, axis=0)
            cov_matrix = np.cov(centered.T)
            
            # Normal is the eigenvector with smallest eigenvalue
            eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
            normal = eigenvectors[:, np.argmin(eigenvalues)]
            normals[i] = normal
        
        return normals
    
    def create_mesh_poisson(self, points: np.ndarray, 
                          normals: Optional[np.ndarray] = None,
                          depth: int = 9) -> Optional[object]:
        """
        Create mesh using Poisson surface reconstruction (if PyMeshLab available)
        """
        if not self.has_pymeshlab:
            print("PyMeshLab not available for Poisson reconstruction")
            return None
        
        try:
            # Create MeshSet
            ms = pymeshlab.MeshSet()
            
            # Add point cloud
            if normals is None:
                normals = self.estimate_normals(points)
            
            # Create mesh from points and normals
            ms.add_mesh(pymeshlab.Mesh(vertex_matrix=points, v_normals_matrix=normals))
            
            # Apply Poisson surface reconstruction
            ms.generate_surface_reconstruction_screened_poisson(depth=depth)
            
            return ms.current_mesh()
            
        except Exception as e:
            print(f"Poisson reconstruction failed: {e}")
            return None
    
    def create_mesh_alpha_shape(self, points: np.ndarray, alpha: float = 0.1) -> Optional[object]:
        """
        Create mesh using alpha shapes (if Trimesh available)
        """
        if not self.has_trimesh:
            print("Trimesh not available for alpha shape reconstruction")
            return None
        
        try:
            # Create alpha shape mesh
            mesh = trimesh.Trimesh(vertices=points)
            alpha_mesh = mesh.convex_hull  # Simplified - use convex hull
            
            return alpha_mesh
            
        except Exception as e:
            print(f"Alpha shape reconstruction failed: {e}")
            return None
    
    def save_point_cloud_ply(self, filename: str, points: np.ndarray, 
                           colors: Optional[np.ndarray] = None):
        """
        Save point cloud to PLY format
        """
        with open(filename, 'w') as f:
            # PLY header
            f.write("ply\n")
            f.write("format ascii 1.0\n")
            f.write(f"element vertex {len(points)}\n")
            f.write("property float x\n")
            f.write("property float y\n")
            f.write("property float z\n")
            
            if colors is not None:
                f.write("property uchar red\n")
                f.write("property uchar green\n")
                f.write("property uchar blue\n")
            
            f.write("end_header\n")
            
            # Write vertices
            for i, point in enumerate(points):
                if colors is not None:
                    color = colors[i]
                    f.write(f"{point[0]} {point[1]} {point[2]} {int(color[0])} {int(color[1])} {int(color[2])}\n")
                else:
                    f.write(f"{point[0]} {point[1]} {point[2]}\n")
        
        print(f"Point cloud saved to {filename}")
    
    def save_mesh_ply(self, filename: str, vertices: np.ndarray, 
                     faces: np.ndarray, colors: Optional[np.ndarray] = None):
        """
        Save mesh to PLY format
        """
        with open(filename, 'w') as f:
            # PLY header
            f.write("ply\n")
            f.write("format ascii 1.0\n")
            f.write(f"element vertex {len(vertices)}\n")
            f.write("property float x\n")
            f.write("property float y\n")
            f.write("property float z\n")
            
            if colors is not None:
                f.write("property uchar red\n")
                f.write("property uchar green\n")
                f.write("property uchar blue\n")
            
            f.write(f"element face {len(faces)}\n")
            f.write("property list uchar int vertex_indices\n")
            f.write("end_header\n")
            
            # Write vertices
            for i, vertex in enumerate(vertices):
                if colors is not None:
                    color = colors[i]
                    f.write(f"{vertex[0]} {vertex[1]} {vertex[2]} {int(color[0])} {int(color[1])} {int(color[2])}\n")
                else:
                    f.write(f"{vertex[0]} {vertex[1]} {vertex[2]}\n")
            
            # Write faces
            for face in faces:
                f.write(f"3 {face[0]} {face[1]} {face[2]}\n")
        
        print(f"Mesh saved to {filename}")

def create_reconstruction_engine():
    """Factory function to create reconstruction engine"""
    return Point3DReconstruction()