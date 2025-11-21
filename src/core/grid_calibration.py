"""
Grid Detection and Calibration Module

Handles detection of reference grids in images and calculates calibration parameters
for accurate 3D measurements.
"""

import cv2
import numpy as np
from typing import Tuple, Optional, List, Dict
import json
from .gpu_acceleration import get_gpu_accelerator, HAS_CUPY

class GridDetector:
    """Detects and analyzes reference grids in images."""
    
    def __init__(self, grid_size_mm: Tuple[float, float] = (10.0, 10.0)):
        """
        Initialize grid detector.
        
        Args:
            grid_size_mm: Real-world size of each grid square in millimeters (width, height)
        """
        self.grid_size_mm = grid_size_mm
        self.grid_points_3d = None
        self.grid_points_2d = None
        self.gpu_accel = get_gpu_accelerator()
        
        # Print GPU info on first initialization
        if not hasattr(GridDetector, '_gpu_info_printed'):
            self.gpu_accel.print_device_info()
            GridDetector._gpu_info_printed = True
        
    def detect_grid(self, image: np.ndarray, grid_pattern: Tuple[int, int] = (9, 6)) -> Optional[np.ndarray]:
        """
        Detect grid pattern in image - supports both checkerboard and line-based grids.
        
        Args:
            image: Input image (BGR or grayscale)
            grid_pattern: Number of inner corners (columns, rows)
            
        Returns:
            Array of detected corner points, or None if detection failed
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        print(f"Attempting to detect grid pattern {grid_pattern} in image...")
        
        # First try standard checkerboard detection
        corners = self._detect_checkerboard(gray, grid_pattern)
        if corners is not None:
            print("Grid detected using checkerboard method")
            return corners
        
        # Try line-based grid detection for grids with line patterns
        corners = self._detect_line_grid(gray, grid_pattern)
        if corners is not None:
            print("Grid detected using line-based method")
            return corners
            
        print("Grid detection failed with all methods")
        return None
    
    def _detect_checkerboard(self, gray: np.ndarray, grid_pattern: Tuple[int, int]) -> Optional[np.ndarray]:
        """Detect standard checkerboard pattern."""
        # Try multiple detection methods and patterns
        patterns_to_try = [
            grid_pattern,
            (grid_pattern[1], grid_pattern[0]),  # Swap rows and columns
            (8, 6), (9, 6), (10, 7), (7, 5),    # Common patterns
            (6, 8), (6, 9), (7, 10), (5, 7)     # Rotated versions
        ]
        
        # Different flag combinations to try
        flag_combinations = [
            cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE,
            cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE,
            cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE,
            cv2.CALIB_CB_ADAPTIVE_THRESH,
            None  # Default flags
        ]
        
        for pattern in patterns_to_try:
            for flags in flag_combinations:
                try:
                    if flags is None:
                        ret, corners = cv2.findChessboardCorners(gray, pattern)
                    else:
                        ret, corners = cv2.findChessboardCorners(gray, pattern, flags)
                    
                    if ret:
                        print(f"Checkerboard detected with pattern {pattern}")
                        # Refine corner positions
                        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
                        corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                        return corners
                except Exception as e:
                    continue  # Try next combination
        
        return None
    
    def _detect_line_grid(self, gray: np.ndarray, grid_pattern: Tuple[int, int]) -> Optional[np.ndarray]:
        """Detect line-based grid pattern (like gold background with white lines)."""
        try:
            print("Trying line-based grid detection...")
            
            # For very fine patterns like 3D printer beds, we need different preprocessing
            # Try multiple preprocessing approaches
            
            # Method 1: Enhanced contrast and edge detection
            corners = self._detect_fine_dot_pattern(gray, grid_pattern)
            if corners is not None:
                return corners
            
            # Method 2: Template matching for cross patterns
            corners = self._detect_cross_pattern(gray, grid_pattern)
            if corners is not None:
                return corners
            
            # Method 3: Standard line detection (original method)
            corners = self._detect_standard_lines(gray, grid_pattern)
            if corners is not None:
                return corners
                
            return None
            
        except Exception as e:
            print(f"Line grid detection failed: {e}")
            return None
    
    def _detect_fine_dot_pattern(self, gray: np.ndarray, grid_pattern: Tuple[int, int]) -> Optional[np.ndarray]:
        """Detect fine dot/cross patterns like on 3D printer beds."""
        try:
            print("Trying fine dot pattern detection...")
            
            # Enhance contrast for fine patterns using GPU if available
            enhanced = self.gpu_accel.enhance_contrast_gpu(gray, clip_limit=3.0, tile_size=(8, 8))
            
            # Apply unsharp masking to enhance fine details using GPU blur
            blurred = self.gpu_accel.gaussian_blur_gpu(enhanced, (5, 5), 0)
            unsharp = cv2.addWeighted(enhanced, 1.5, blurred, -0.5, 0)
            
            # Use a more aggressive threshold to reduce initial point count
            corners_harris = self.gpu_accel.harris_corners_gpu(unsharp, 2, 3, 0.04)
            corners_harris = cv2.dilate(corners_harris, None)
            
            # Use adaptive threshold to reduce points
            mean_response = np.mean(corners_harris)
            std_response = np.std(corners_harris)
            threshold = mean_response + 3 * std_response  # More aggressive threshold
            
            corner_points = np.where(corners_harris > threshold)
            
            print(f"Initial corner detection found {len(corner_points[0])} points")
            
            if len(corner_points[0]) < grid_pattern[0] * grid_pattern[1]:
                print(f"Not enough corners detected: {len(corner_points[0])}")
                return None
            
            # Limit the number of points to process (performance optimization)
            max_points = min(len(corner_points[0]), 50000)  # Limit to 50k points max
            indices = np.random.choice(len(corner_points[0]), max_points, replace=False) if len(corner_points[0]) > max_points else range(len(corner_points[0]))
            
            # Convert to coordinate pairs
            detected_corners = []
            for i in indices:
                y, x = corner_points[0][i], corner_points[1][i]
                detected_corners.append((x, y))
            
            print(f"Processing {len(detected_corners)} corner points for grid organization")
            
            # Organize into grid
            grid_points = self._organize_grid_points(detected_corners, grid_pattern)
            if grid_points is not None:
                return grid_points.reshape(-1, 1, 2).astype(np.float32)
            
            return None
            
        except Exception as e:
            print(f"Fine dot pattern detection failed: {e}")
            return None
    
    def _detect_cross_pattern(self, gray: np.ndarray, grid_pattern: Tuple[int, int]) -> Optional[np.ndarray]:
        """Detect cross/plus patterns in the grid."""
        try:
            print("Trying cross pattern detection...")
            
            # Create kernels for cross detection
            cross_kernel = np.array([
                [-1, -1, -1, -1, -1],
                [-1, -1,  1, -1, -1],
                [-1,  1,  1,  1, -1],
                [-1, -1,  1, -1, -1],
                [-1, -1, -1, -1, -1]
            ], dtype=np.float32)
            
            # Apply morphological operations to enhance pattern using GPU
            kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
            morph = self.gpu_accel.morphology_gpu(gray, cv2.MORPH_TOPHAT, kernel)
            
            # Apply cross template matching
            response = cv2.filter2D(morph, -1, cross_kernel)
            
            # Find local maxima
            min_distance = 20  # Minimum distance between detected points
            threshold = np.mean(response) + 2 * np.std(response)
            
            # Find peaks using simple local maxima detection
            h, w = response.shape
            peaks = []
            
            for y in range(min_distance//2, h - min_distance//2, min_distance//2):
                for x in range(min_distance//2, w - min_distance//2, min_distance//2):
                    # Check if this point is a local maximum
                    region = response[y-min_distance//2:y+min_distance//2, 
                                    x-min_distance//2:x+min_distance//2]
                    if response[y, x] == np.max(region) and response[y, x] > threshold:
                        peaks.append((x, y))
            
            if len(peaks) < grid_pattern[0] * grid_pattern[1]:
                print(f"Not enough cross patterns detected: {len(peaks)}")
                return None
            
            print(f"Detected {len(peaks)} cross patterns")
            
            # Organize into grid
            grid_points = self._organize_grid_points(peaks, grid_pattern)
            if grid_points is not None:
                return grid_points.reshape(-1, 1, 2).astype(np.float32)
            
            return None
            
        except Exception as e:
            print(f"Cross pattern detection failed: {e}")
            return None
    
    def _detect_standard_lines(self, gray: np.ndarray, grid_pattern: Tuple[int, int]) -> Optional[np.ndarray]:
        """Standard line detection method."""
        try:
            print("Trying standard line detection...")
            
            # Apply Gaussian blur to reduce noise using GPU
            blurred = self.gpu_accel.gaussian_blur_gpu(gray, (3, 3), 0)
            
            # Detect lines using GPU-accelerated edge detection
            edges = self.gpu_accel.canny_edge_gpu(blurred, 50, 150)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
            
            if lines is None:
                print("No lines detected in image")
                return None
            
            print(f"Detected {len(lines)} lines")
            
            # Separate horizontal and vertical lines
            horizontal_lines = []
            vertical_lines = []
            
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                
                if abs(angle) < 10 or abs(angle) > 170:  # Horizontal lines
                    horizontal_lines.append(line[0])
                elif abs(abs(angle) - 90) < 10:  # Vertical lines
                    vertical_lines.append(line[0])
            
            print(f"Found {len(horizontal_lines)} horizontal and {len(vertical_lines)} vertical lines")
            
            if len(horizontal_lines) < 3 or len(vertical_lines) < 3:
                print("Insufficient grid lines detected")
                return None
            
            # Find intersections of horizontal and vertical lines
            intersections = self._find_line_intersections(horizontal_lines, vertical_lines)
            
            if len(intersections) >= grid_pattern[0] * grid_pattern[1]:
                # Sort and select the grid points
                grid_points = self._organize_grid_points(intersections, grid_pattern)
                if grid_points is not None:
                    return grid_points.reshape(-1, 1, 2).astype(np.float32)
            
            return None
            
        except Exception as e:
            print(f"Standard line detection failed: {e}")
            return None
    
    def _find_line_intersections(self, horizontal_lines, vertical_lines):
        """Find intersections between horizontal and vertical lines."""
        intersections = []
        
        for h_line in horizontal_lines:
            hx1, hy1, hx2, hy2 = h_line
            for v_line in vertical_lines:
                vx1, vy1, vx2, vy2 = v_line
                
                # Calculate intersection point
                intersection = self._line_intersection(
                    (hx1, hy1, hx2, hy2), (vx1, vy1, vx2, vy2)
                )
                
                if intersection is not None:
                    intersections.append(intersection)
        
        return intersections
    
    def _line_intersection(self, line1, line2):
        """Calculate intersection point of two lines."""
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2
        
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(denom) < 1e-10:
            return None  # Lines are parallel
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
        
        if 0 <= t <= 1 and 0 <= u <= 1:
            # Intersection point
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return (x, y)
        
        return None
    
    def _organize_grid_points(self, intersections, grid_pattern):
        """Organize intersection points into a regular grid."""
        if len(intersections) < grid_pattern[0] * grid_pattern[1]:
            return None
        
        # Convert to numpy array
        points = np.array(intersections)
        
        # For very fine grids, we need more sophisticated clustering
        if len(points) > grid_pattern[0] * grid_pattern[1] * 2:
            # Use K-means like clustering to find the most regular grid points
            points = self._cluster_grid_points(points, grid_pattern)
        
        # Sort points by y-coordinate first, then x-coordinate
        points = points[np.lexsort((points[:, 0], points[:, 1]))]
        
        # Group points into rows with adaptive tolerance
        rows = []
        current_y = points[0][1]
        current_row = []
        
        # Calculate adaptive tolerance based on image size
        img_height = max(points[:, 1]) - min(points[:, 1])
        tolerance = max(20, img_height / (grid_pattern[1] * 3))  # Adaptive tolerance
        
        print(f"Using row grouping tolerance: {tolerance}")
        
        for point in points:
            if abs(point[1] - current_y) <= tolerance:
                current_row.append(point)
            else:
                if len(current_row) >= grid_pattern[0]:
                    # Sort current row by x-coordinate and take the most evenly spaced points
                    current_row = sorted(current_row, key=lambda p: p[0])
                    if len(current_row) > grid_pattern[0]:
                        # Select most evenly spaced points
                        current_row = self._select_evenly_spaced_points(current_row, grid_pattern[0])
                    rows.append(current_row[:grid_pattern[0]])
                current_row = [point]
                current_y = point[1]
        
        # Add the last row
        if len(current_row) >= grid_pattern[0]:
            current_row = sorted(current_row, key=lambda p: p[0])
            if len(current_row) > grid_pattern[0]:
                current_row = self._select_evenly_spaced_points(current_row, grid_pattern[0])
            rows.append(current_row[:grid_pattern[0]])
        
        # Select the required number of rows
        if len(rows) >= grid_pattern[1]:
            # If we have too many rows, select the most evenly spaced ones
            if len(rows) > grid_pattern[1]:
                rows = self._select_evenly_spaced_rows(rows, grid_pattern[1])
            
            selected_rows = rows[:grid_pattern[1]]
            
            # Flatten the grid points
            grid_points = []
            for row in selected_rows:
                grid_points.extend(row)
            
            result_points = np.array(grid_points[:grid_pattern[0] * grid_pattern[1]])
            print(f"Organized {len(result_points)} points into {grid_pattern[0]}x{grid_pattern[1]} grid")
            return result_points
        
        print(f"Could not organize points into grid: found {len(rows)} rows, need {grid_pattern[1]}")
        return None
    
    def _cluster_grid_points(self, points, grid_pattern):
        """Use simple clustering to find the most regular grid points."""
        # Calculate expected grid spacing
        x_range = np.max(points[:, 0]) - np.min(points[:, 0])
        y_range = np.max(points[:, 1]) - np.min(points[:, 1])
        
        expected_x_spacing = x_range / (grid_pattern[0] + 1)
        expected_y_spacing = y_range / (grid_pattern[1] + 1)
        
        # Use more aggressive filtering to reduce processing time
        min_distance = min(expected_x_spacing, expected_y_spacing) * 0.7  # Increased from 0.5
        
        # Pre-sort points for more efficient processing
        points_sorted = points[np.lexsort((points[:, 0], points[:, 1]))]
        
        filtered_points = []
        # Use GPU-accelerated distance calculations if available and worthwhile
        if HAS_CUPY and len(points_sorted) > 10000:
            filtered_points = self._gpu_cluster_points(points_sorted, min_distance, grid_pattern)
        else:
            # CPU clustering with optimizations
            for point in points_sorted:
                too_close = False
                # Early termination - only check recent points
                check_count = min(len(filtered_points), 50)  # Limit search scope
                for i in range(-check_count, 0):
                    if i + len(filtered_points) >= 0:
                        existing = filtered_points[i]
                        if abs(point[0] - existing[0]) < min_distance and abs(point[1] - existing[1]) < min_distance:
                            if np.linalg.norm(point - existing) < min_distance:
                                too_close = True
                                break
                
                if not too_close:
                    filtered_points.append(point)
                
                # Early termination if we have enough points
                if len(filtered_points) > grid_pattern[0] * grid_pattern[1] * 3:
                    break
        
        print(f"Clustered {len(points)} points down to {len(filtered_points)}")
        return np.array(filtered_points)
    
    def _gpu_cluster_points(self, points, min_distance, grid_pattern):
        """GPU-accelerated point clustering using CuPy."""
        try:
            import cupy as cp
            
            # Move points to GPU
            gpu_points = cp.asarray(points)
            filtered_indices = []
            
            # Process in batches to avoid memory issues
            batch_size = 5000
            for i in range(0, len(points), batch_size):
                batch_end = min(i + batch_size, len(points))
                current_batch = gpu_points[i:batch_end]
                
                # For each point in batch, check against already filtered points
                for j, point in enumerate(current_batch):
                    if len(filtered_indices) == 0:
                        filtered_indices.append(i + j)
                        continue
                    
                    # Check distance to last few filtered points (most likely to be close)
                    check_count = min(len(filtered_indices), 20)
                    too_close = False
                    
                    for k in range(-check_count, 0):
                        if k + len(filtered_indices) >= 0:
                            ref_idx = filtered_indices[k]
                            ref_point = gpu_points[ref_idx]
                            dist = cp.linalg.norm(point - ref_point)
                            if dist < min_distance:
                                too_close = True
                                break
                    
                    if not too_close:
                        filtered_indices.append(i + j)
                    
                    # Early exit if we have enough points
                    if len(filtered_indices) > grid_pattern[0] * grid_pattern[1] * 3:
                        break
                
                if len(filtered_indices) > grid_pattern[0] * grid_pattern[1] * 3:
                    break
            
            # Convert back to CPU
            filtered_points = []
            for idx in filtered_indices:
                filtered_points.append(points[idx])
            
            return filtered_points
            
        except Exception as e:
            print(f"GPU clustering failed, falling back to CPU: {e}")
            # Fallback to simple CPU clustering
            return points[:grid_pattern[0] * grid_pattern[1] * 3]
    
    def _select_evenly_spaced_points(self, points, count):
        """Select evenly spaced points from a list."""
        if len(points) <= count:
            return points
            
        # Calculate spacing
        total_span = points[-1][0] - points[0][0]
        ideal_spacing = total_span / (count - 1)
        
        selected = [points[0]]  # Always include first point
        
        for i in range(1, count - 1):
            target_x = points[0][0] + i * ideal_spacing
            # Find closest point to target
            best_idx = min(range(len(points)), key=lambda j: abs(points[j][0] - target_x))
            selected.append(points[best_idx])
        
        selected.append(points[-1])  # Always include last point
        return selected
    
    def _select_evenly_spaced_rows(self, rows, count):
        """Select evenly spaced rows."""
        if len(rows) <= count:
            return rows
            
        # Select rows based on their y-coordinates
        row_y_coords = [np.mean([p[1] for p in row]) for row in rows]
        indices = np.linspace(0, len(rows) - 1, count, dtype=int)
        
        return [rows[i] for i in indices]
    
    def detect_and_visualize_grid(self, image: np.ndarray, grid_pattern: Tuple[int, int] = (9, 6), save_debug: bool = False) -> Tuple[Optional[np.ndarray], np.ndarray]:
        """
        Detect grid and return both corners and visualization image.
        
        Args:
            image: Input image
            grid_pattern: Number of inner corners (columns, rows)
            save_debug: Whether to save debug images
            
        Returns:
            Tuple of (corners, visualization_image)
        """
        corners = self.detect_grid(image, grid_pattern)
        
        # Create visualization
        vis_image = image.copy()
        if corners is not None:
            # Draw detected grid points
            for i, corner in enumerate(corners):
                x, y = corner.ravel().astype(int)
                cv2.circle(vis_image, (x, y), 5, (0, 255, 0), -1)
                cv2.putText(vis_image, str(i), (x+10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 0), 1)
            
            # Draw grid lines to show the detected pattern
            if len(corners) == grid_pattern[0] * grid_pattern[1]:
                for row in range(grid_pattern[1]):
                    for col in range(grid_pattern[0] - 1):
                        pt1_idx = row * grid_pattern[0] + col
                        pt2_idx = row * grid_pattern[0] + col + 1
                        if pt1_idx < len(corners) and pt2_idx < len(corners):
                            pt1 = tuple(corners[pt1_idx].ravel().astype(int))
                            pt2 = tuple(corners[pt2_idx].ravel().astype(int))
                            cv2.line(vis_image, pt1, pt2, (255, 0, 0), 2)
                
                for col in range(grid_pattern[0]):
                    for row in range(grid_pattern[1] - 1):
                        pt1_idx = row * grid_pattern[0] + col
                        pt2_idx = (row + 1) * grid_pattern[0] + col
                        if pt1_idx < len(corners) and pt2_idx < len(corners):
                            pt1 = tuple(corners[pt1_idx].ravel().astype(int))
                            pt2 = tuple(corners[pt2_idx].ravel().astype(int))
                            cv2.line(vis_image, pt1, pt2, (255, 0, 0), 2)
            
            status_text = f"Grid detected: {grid_pattern[0]}x{grid_pattern[1]} ({len(corners)} points)"
            cv2.putText(vis_image, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(vis_image, "Grid NOT detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(vis_image, "Try line-based grid detection", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
        if save_debug:
            # Save debug image
            debug_filename = f"debug_grid_detection_{hash(image.tobytes()) % 10000}.jpg"
            cv2.imwrite(debug_filename, vis_image)
            print(f"Debug image saved as {debug_filename}")
            
        return corners, vis_image
    
    def analyze_grid_patterns(self, image: np.ndarray) -> List[Tuple[int, int]]:
        """
        Analyze an image to find possible grid patterns.
        
        Args:
            image: Input image
            
        Returns:
            List of detected grid patterns (cols, rows)
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
            
        detected_patterns = []
        
        print("Analyzing possible grid patterns in image...")
        
        # First try standard checkerboard patterns
        test_patterns = [
            (3, 3), (4, 3), (5, 4), (6, 4), (7, 5), (8, 6), (9, 6), (10, 7),
            (6, 8), (7, 9), (8, 10), (9, 7), (10, 8), (11, 8), (12, 9),
            (5, 3), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9)
        ]
        
        for pattern in test_patterns:
            try:
                ret, corners = cv2.findChessboardCorners(
                    gray, pattern, 
                    cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
                )
                if ret:
                    detected_patterns.append(pattern)
                    print(f"✓ Detected checkerboard pattern: {pattern[0]}x{pattern[1]} inner corners")
            except:
                continue
        
        # If no checkerboard found, try line-based detection
        if not detected_patterns:
            print("No checkerboard patterns found. Trying line-based grid detection...")
            
            # Detect lines
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            edges = cv2.Canny(blurred, 50, 150, apertureSize=3)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
            
            if lines is not None:
                # Count approximate grid structure
                horizontal_lines = []
                vertical_lines = []
                
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                    
                    if abs(angle) < 10 or abs(angle) > 170:
                        horizontal_lines.append(line[0])
                    elif abs(abs(angle) - 90) < 10:
                        vertical_lines.append(line[0])
                
                h_count = len(horizontal_lines)
                v_count = len(vertical_lines)
                
                if h_count >= 3 and v_count >= 3:
                    # Estimate grid pattern based on line counts
                    estimated_cols = min(v_count - 1, 15)  # Intersections = lines - 1
                    estimated_rows = min(h_count - 1, 15)
                    
                    if estimated_cols >= 3 and estimated_rows >= 3:
                        pattern = (estimated_cols, estimated_rows)
                        detected_patterns.append(pattern)
                        print(f"✓ Detected line-based grid pattern: {pattern[0]}x{pattern[1]} (estimated from {h_count} horizontal, {v_count} vertical lines)")
                        
                        # Add some variations
                        for delta_c in [-1, 0, 1]:
                            for delta_r in [-1, 0, 1]:
                                new_c = estimated_cols + delta_c
                                new_r = estimated_rows + delta_r
                                if new_c >= 3 and new_r >= 3 and (new_c, new_r) not in detected_patterns:
                                    detected_patterns.append((new_c, new_r))
        
        if not detected_patterns:
            print("No grid patterns detected.")
            print("Make sure your image contains:")
            print("- Clear checkerboard pattern OR regular grid lines")
            print("- Good contrast between grid elements")
            print("- Grid is flat and not severely distorted")
            print("- Grid takes up a significant portion of the image")
            print("- For line grids: ensure lines are clearly visible and form regular intersections")
        
        return detected_patterns
    
    def generate_3d_points(self, grid_pattern: Tuple[int, int]) -> np.ndarray:
        """
        Generate 3D world coordinates for grid points.
        
        Args:
            grid_pattern: Number of inner corners (columns, rows)
            
        Returns:
            3D points array in world coordinates
        """
        # Create 3D points (z=0, grid lies in xy-plane)
        objp = np.zeros((grid_pattern[0] * grid_pattern[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:grid_pattern[0], 0:grid_pattern[1]].T.reshape(-1, 2)
        
        # Scale by actual grid size
        objp[:, 0] *= self.grid_size_mm[0]
        objp[:, 1] *= self.grid_size_mm[1]
        
        return objp
    
    def calibrate_camera(self, images: List[np.ndarray], grid_pattern: Tuple[int, int] = (9, 6)) -> Dict:
        """
        Calibrate camera using multiple grid images.
        
        Args:
            images: List of images containing grid patterns
            grid_pattern: Number of inner corners (columns, rows)
            
        Returns:
            Dictionary containing calibration parameters
        """
        # Prepare object points
        objp = self.generate_3d_points(grid_pattern)
        
        # Arrays to store object points and image points
        objpoints = []  # 3d points in real world space
        imgpoints = []  # 2d points in image plane
        
        image_size = None
        successful_detections = 0
        
        print(f"Starting calibration with {len(images)} images...")
        print(f"Looking for grid pattern: {grid_pattern[0]}x{grid_pattern[1]} inner corners")
        
        for i, image in enumerate(images):
            print(f"Processing image {i+1}/{len(images)}...")
            corners, vis_image = self.detect_and_visualize_grid(image, grid_pattern, save_debug=True)
            
            if corners is not None:
                objpoints.append(objp)
                imgpoints.append(corners)
                successful_detections += 1
                print(f"✓ Grid detected in image {i+1}")
                
                if image_size is None:
                    image_size = (image.shape[1], image.shape[0])
            else:
                print(f"✗ Grid NOT detected in image {i+1}")
        
        print(f"Grid detection summary: {successful_detections}/{len(images)} images successful")
        
        if successful_detections < 3:
            error_msg = f"Need at least 3 successful grid detections for calibration. Got {successful_detections}/{len(images)}. Check if your images contain a clear checkerboard pattern with {grid_pattern[0]}x{grid_pattern[1]} inner corners."
            raise ValueError(error_msg)
        
        print(f"Performing camera calibration with {successful_detections} valid images...")
        
        # Perform camera calibration
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, image_size, None, None
        )
        
        print(f"Camera calibration completed with reprojection error: {ret:.3f}")
        
        return {
            'camera_matrix': mtx,
            'distortion_coefficients': dist,
            'rotation_vectors': rvecs,
            'translation_vectors': tvecs,
            'reprojection_error': ret,
            'image_size': image_size,
            'successful_detections': successful_detections,
            'total_images': len(images)
        }
    
    def save_calibration(self, calibration: Dict, filename: str):
        """Save calibration data to JSON file."""
        # Convert numpy arrays to lists for JSON serialization
        json_data = {
            'camera_matrix': calibration['camera_matrix'].tolist(),
            'distortion_coefficients': calibration['distortion_coefficients'].tolist(),
            'reprojection_error': float(calibration['reprojection_error']),
            'image_size': calibration['image_size'],
            'grid_size_mm': self.grid_size_mm
        }
        
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=2)
    
    def load_calibration(self, filename: str) -> Dict:
        """Load calibration data from JSON file."""
        with open(filename, 'r') as f:
            json_data = json.load(f)
        
        return {
            'camera_matrix': np.array(json_data['camera_matrix']),
            'distortion_coefficients': np.array(json_data['distortion_coefficients']),
            'reprojection_error': json_data['reprojection_error'],
            'image_size': tuple(json_data['image_size']),
            'grid_size_mm': tuple(json_data.get('grid_size_mm', self.grid_size_mm))
        }