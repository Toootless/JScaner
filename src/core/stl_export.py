"""
STL Export Module with Open3D fallback support

Handles conversion and export of 3D meshes to STL format for 3D printing.
"""

import numpy as np
from typing import Optional, Tuple, Union
import os

# Try to import Open3D, fall back to alternative implementation
try:
    import open3d as o3d
    HAS_OPEN3D = True
except ImportError:
    HAS_OPEN3D = False

# Try to import trimesh as alternative
try:
    import trimesh
    HAS_TRIMESH = True
except ImportError:
    HAS_TRIMESH = False

# Import fallback functions
from .stl_fallback import write_stl_manual, extract_mesh_data, write_point_cloud_ply

class STLExporter:
    """Handles export of 3D meshes to STL format with Open3D fallback support."""
    
    def __init__(self):
        """Initialize STL exporter."""
        self.has_open3d = HAS_OPEN3D
        self.has_trimesh = HAS_TRIMESH
    
    def export_mesh_to_stl(self, mesh: object, 
                          filename: str, 
                          scale_factor: float = 1.0,
                          ascii_format: bool = False) -> bool:
        """
        Export mesh to STL file.
        
        Args:
            mesh: Mesh object (Open3D, fallback, or other format)
            filename: Output STL filename
            scale_factor: Scale factor for the mesh (default 1.0)
            ascii_format: Use ASCII format instead of binary
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            # Ensure filename has .stl extension
            if not filename.lower().endswith('.stl'):
                filename += '.stl'
            
            if self.has_open3d and hasattr(mesh, 'vertices') and hasattr(mesh, 'triangles'):
                # Open3D mesh
                return self._export_open3d_mesh(mesh, filename, scale_factor)
            else:
                # Fallback: extract mesh data and write manually
                return self._export_fallback_mesh(mesh, filename, scale_factor, ascii_format)
                
        except Exception as e:
            print(f"Error exporting mesh to STL: {e}")
            return False
    
    def _export_open3d_mesh(self, mesh, filename: str, scale_factor: float) -> bool:
        """Export Open3D mesh using native functionality"""
        if scale_factor != 1.0:
            mesh = mesh.scale(scale_factor, center=mesh.get_center())
        
        success = o3d.io.write_triangle_mesh(filename, mesh)
        
        if success:
            print(f"Mesh exported to: {filename}")
            return True
        else:
            print(f"Failed to export mesh with Open3D")
            return False
    
    def _export_fallback_mesh(self, mesh, filename: str, scale_factor: float, ascii_format: bool) -> bool:
        """Export mesh using fallback methods"""
        mesh_data = extract_mesh_data(mesh)
        if mesh_data is None:
            print("Could not extract mesh data for export")
            return False
        
        vertices, faces = mesh_data
        
        # Apply scale factor
        if scale_factor != 1.0:
            vertices = vertices * scale_factor
        
        success = write_stl_manual(vertices, faces, filename, ascii_format)
        return success
    
    def export_point_cloud_to_stl(self, point_cloud: object, 
                                  filename: str, 
                                  reconstruction_method: str = "poisson",
                                  scale_factor: float = 1.0) -> bool:
        """
        Export point cloud to STL file by first generating a mesh.
        
        Args:
            point_cloud: Point cloud object (Open3D or fallback)
            filename: Output STL filename
            reconstruction_method: Mesh reconstruction method ("poisson" or "alpha_shape")
            scale_factor: Scale factor for the mesh (default 1.0)
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            # First, we need to generate a mesh from the point cloud
            # Import reconstruction module to access mesh generation
            from .reconstruction import StereoReconstructor
            
            reconstructor = StereoReconstructor()
            mesh = reconstructor.generate_mesh(point_cloud, method=reconstruction_method)
            
            if mesh is None:
                print("Failed to generate mesh from point cloud")
                return False
            
            # Now export the mesh to STL
            return self.export_mesh_to_stl(mesh, filename, scale_factor=scale_factor)
            
        except Exception as e:
            print(f"Error exporting point cloud to STL: {e}")
            return False
    
    def export_point_cloud(self, points: np.ndarray, 
                          filename: str, 
                          colors: Optional[np.ndarray] = None,
                          format: str = "ply") -> bool:
        """
        Export point cloud to file.
        
        Args:
            points: Nx3 array of point coordinates
            filename: Output filename
            colors: Nx3 array of RGB colors (optional)
            format: Output format ("ply" or "xyz")
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            if format.lower() == "ply":
                return write_point_cloud_ply(points, filename, colors)
            elif format.lower() == "xyz":
                return self._export_xyz(points, filename)
            else:
                print(f"Unsupported format: {format}")
                return False
        except Exception as e:
            print(f"Error exporting point cloud: {e}")
            return False
    
    def _export_xyz(self, points: np.ndarray, filename: str) -> bool:
        """Export points to simple XYZ format"""
        try:
            np.savetxt(filename, points, fmt='%.6f')
            print(f"Points exported to: {filename}")
            return True
        except Exception as e:
            print(f"Error writing XYZ file: {e}")
            return False
    
    def validate_mesh(self, mesh) -> bool:
        """
        Validate mesh before export.
        
        Args:
            mesh: Mesh object to validate
            
        Returns:
            True if mesh is valid for export
        """
        try:
            if self.has_open3d and hasattr(mesh, 'vertices') and hasattr(mesh, 'triangles'):
                # Open3D mesh validation
                vertices = np.asarray(mesh.vertices)
                triangles = np.asarray(mesh.triangles)
                
                if len(vertices) == 0:
                    print("Mesh has no vertices")
                    return False
                if len(triangles) == 0:
                    print("Mesh has no triangles")
                    return False
                    
                return True
            else:
                # Fallback validation
                mesh_data = extract_mesh_data(mesh)
                if mesh_data is None:
                    print("Could not extract mesh data for validation")
                    return False
                
                vertices, faces = mesh_data
                if len(vertices) == 0:
                    print("Mesh has no vertices")
                    return False
                if len(faces) == 0:
                    print("Mesh has no faces")
                    return False
                
                return True
                
        except Exception as e:
            print(f"Error validating mesh: {e}")
            return False
    
    def get_mesh_info(self, mesh) -> dict:
        """
        Get information about the mesh.
        
        Args:
            mesh: Mesh object
            
        Returns:
            Dictionary with mesh information
        """
        info = {
            'vertices': 0,
            'faces': 0,
            'format': 'unknown',
            'valid': False
        }
        
        try:
            if self.has_open3d and hasattr(mesh, 'vertices') and hasattr(mesh, 'triangles'):
                # Open3D mesh
                vertices = np.asarray(mesh.vertices)
                triangles = np.asarray(mesh.triangles)
                
                info['vertices'] = len(vertices)
                info['faces'] = len(triangles)
                info['format'] = 'open3d'
                info['valid'] = len(vertices) > 0 and len(triangles) > 0
            else:
                # Fallback mesh
                mesh_data = extract_mesh_data(mesh)
                if mesh_data is not None:
                    vertices, faces = mesh_data
                    info['vertices'] = len(vertices)
                    info['faces'] = len(faces)
                    info['format'] = 'fallback'
                    info['valid'] = len(vertices) > 0 and len(faces) > 0
        
        except Exception as e:
            print(f"Error getting mesh info: {e}")
        
        return info