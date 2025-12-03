"""
GPU Acceleration Module

Provides GPU-accelerated alternatives for intensive operations.
Supports NVIDIA CUDA with Numba, CuPy, PyTorch, and OpenCV GPU acceleration.
"""

import numpy as np
import cv2
import os
import sys

# Check for GPU support
HAS_CUDA = False
HAS_CUPY = False
HAS_NUMBA_CUDA = False
HAS_TORCH_CUDA = False
CUDA_VERSION = None

# Check Numba CUDA support
try:
    from numba import cuda as numba_cuda
    if numba_cuda.is_available():
        HAS_NUMBA_CUDA = True
        CUDA_VERSION = numba_cuda.runtime.get_version()
        print(f"✓ Numba CUDA available (CUDA {CUDA_VERSION})")
    else:
        print("Numba CUDA not available - using CPU JIT compilation")
except (ImportError, RuntimeError) as e:
    print(f"Numba CUDA not available: {e}")

# Check CuPy (NumPy on GPU)
try:
    import cupy as cp
    HAS_CUPY = True
    HAS_CUDA = True
    print("✓ CuPy (GPU array acceleration) available")
except ImportError as e:
    print(f"CuPy not available - NumPy operations on CPU")
except Exception as e:
    print(f"CuPy import error: {e}")

# Check PyTorch CUDA support
try:
    import torch
    if torch.cuda.is_available():
        HAS_TORCH_CUDA = True
        print(f"✓ PyTorch CUDA available ({torch.cuda.get_device_name(0)})")
    else:
        print("PyTorch installed but CUDA not available")
except ImportError:
    print("PyTorch not installed")
except Exception as e:
    print(f"PyTorch CUDA error: {e}")

# Check OpenCV CUDA support
try:
    if cv2.cuda.getCudaEnabledDeviceCount() > 0:
        HAS_CUDA = True
        print(f"✓ OpenCV CUDA available - {cv2.cuda.getCudaEnabledDeviceCount()} GPU(s) detected")
    else:
        print("OpenCV CUDA not available - using CPU version")
except AttributeError:
    print("OpenCV compiled without CUDA support - upgrade with: pip install opencv-contrib-python")

class GPUAccelerator:
    """Provides GPU-accelerated operations when available."""
    
    def __init__(self):
        self.use_gpu = HAS_CUPY or HAS_CUDA
        self.device_info = self._get_device_info()
        self._gpu_memory_pool = None
        self._initialize_gpu()
        
    def _initialize_gpu(self):
        """Initialize GPU memory pool for better performance."""
        if HAS_CUPY:
            try:
                # Use memory pool to reduce allocation overhead
                import cupy
                self._gpu_memory_pool = cupy.get_default_memory_pool()
                # Warm up GPU
                dummy = cupy.zeros((100, 100), dtype=cupy.float32)
                del dummy
                print("✓ GPU memory pool initialized - RTX 3060 ready")
            except Exception as e:
                print(f"Warning: GPU initialization failed: {e}")
                import traceback
                traceback.print_exc()
        
    def _get_device_info(self):
        """Get information about available GPU devices."""
        info = {
            'cpu_only': not self.use_gpu,
            'cupy_available': HAS_CUPY,
            'opencv_cuda_available': HAS_CUDA,
            'devices': []
        }
        
        if HAS_CUPY:
            try:
                device_count = cp.cuda.runtime.getDeviceCount()
                for i in range(device_count):
                    props = cp.cuda.runtime.getDeviceProperties(i)
                    info['devices'].append({
                        'id': i,
                        'name': props['name'].decode(),
                        'memory': props['totalGlobalMem'] // (1024**3),  # GB
                        'compute_capability': f"{props['major']}.{props['minor']}"
                    })
            except Exception as e:
                print(f"Error getting GPU info: {e}")
                
        return info
    
    def print_device_info(self):
        """Print information about available compute devices."""
        print("\nCompute Device Information:")
        print("=" * 40)
        
        if self.device_info['cpu_only']:
            print("Using CPU only")
        else:
            if self.device_info['cupy_available']:
                print("CuPy GPU acceleration: Available")
                for device in self.device_info['devices']:
                    print(f"  GPU {device['id']}: {device['name']}")
                    print(f"    Memory: {device['memory']} GB")
                    print(f"    Compute: {device['compute_capability']}")
            
            if self.device_info['opencv_cuda_available']:
                print(f"OpenCV CUDA: Available ({cv2.cuda.getCudaEnabledDeviceCount()} devices)")
    
    def to_gpu(self, array):
        """Move numpy array to GPU if CuPy is available."""
        if HAS_CUPY:
            return cp.asarray(array)
        return array
    
    def to_cpu(self, array):
        """Move array back to CPU."""
        if HAS_CUPY and hasattr(array, 'get'):
            return array.get()
        return array
    
    def gaussian_blur_gpu(self, image, kernel_size, sigma):
        """GPU-accelerated Gaussian blur."""
        # For small images, GPU overhead isn't worth it
        if image.size < 1000000:  # Less than 1MP
            return cv2.GaussianBlur(image, kernel_size, sigma)
            
        if HAS_CUDA:
            # Use OpenCV CUDA (only if available)
            try:
                gpu_img = cv2.cuda_GpuMat()
                gpu_img.upload(image)
                gpu_blurred = cv2.cuda.GaussianBlur(gpu_img, kernel_size, sigma)
                result = gpu_blurred.download()
                return result
            except AttributeError:
                pass  # Fall through to CuPy method
                
        if HAS_CUPY:
            # Use CuPy with scipy-like operations
            try:
                from cupyx.scipy import ndimage
                gpu_img = self.to_gpu(image.astype(np.float32))
                blurred = ndimage.gaussian_filter(gpu_img, sigma)
                return self.to_cpu(blurred).astype(image.dtype)
            except ImportError:
                pass  # Fall through to CPU
                
        # Fallback to CPU
        return cv2.GaussianBlur(image, kernel_size, sigma)
    
    def canny_edge_gpu(self, image, low_threshold, high_threshold):
        """GPU-accelerated Canny edge detection."""
        if HAS_CUDA:
            try:
                gpu_img = cv2.cuda_GpuMat()
                gpu_img.upload(image)
                gpu_edges = cv2.cuda.Canny(gpu_img, low_threshold, high_threshold)
                return gpu_edges.download()
            except AttributeError:
                pass
        # Fallback to CPU
        return cv2.Canny(image, low_threshold, high_threshold)
    
    def harris_corners_gpu(self, image, block_size=2, k_size=3, k=0.04):
        """GPU-accelerated Harris corner detection."""
        if HAS_CUDA:
            try:
                gpu_img = cv2.cuda_GpuMat()
                gpu_img.upload(image)
                gpu_corners = cv2.cuda.cornerHarris(gpu_img, block_size, k_size, k)
                return gpu_corners.download()
            except AttributeError:
                pass
        
        if HAS_CUPY and image.size > 500000:  # Only use GPU for larger images
            try:
                # Custom Harris corner detection using CuPy
                return self._harris_corners_cupy(image, block_size, k_size, k)
            except Exception:
                pass
                
        # Fallback to CPU
        return cv2.cornerHarris(image, block_size, k_size, k)
    
    def _harris_corners_cupy(self, image, block_size, k_size, k):
        """Custom Harris corner detection using CuPy."""
        import cupy as cp
        from cupyx.scipy import ndimage
        
        # Convert to GPU
        gpu_img = cp.asarray(image, dtype=cp.float32)
        
        # Compute gradients
        sobel_x = cp.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=cp.float32)
        sobel_y = cp.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=cp.float32)
        
        Ix = ndimage.convolve(gpu_img, sobel_x, mode='constant')
        Iy = ndimage.convolve(gpu_img, sobel_y, mode='constant')
        
        # Compute products
        Ixx = Ix * Ix
        Ixy = Ix * Iy
        Iyy = Iy * Iy
        
        # Apply Gaussian filter
        sigma = k_size / 3.0
        Ixx = ndimage.gaussian_filter(Ixx, sigma)
        Ixy = ndimage.gaussian_filter(Ixy, sigma)
        Iyy = ndimage.gaussian_filter(Iyy, sigma)
        
        # Compute Harris response
        det = Ixx * Iyy - Ixy * Ixy
        trace = Ixx + Iyy
        harris_response = det - k * (trace * trace)
        
        return self.to_cpu(harris_response)
    
    def enhance_contrast_gpu(self, image, clip_limit=3.0, tile_size=(8, 8)):
        """GPU-accelerated CLAHE contrast enhancement."""
        if HAS_CUDA:
            try:
                gpu_img = cv2.cuda_GpuMat()
                gpu_img.upload(image)
                clahe = cv2.cuda.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
                gpu_enhanced = clahe.apply(gpu_img)
                return gpu_enhanced.download()
            except AttributeError:
                pass
        
        # Use optimized CPU version
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
        return clahe.apply(image)
    
    def morphology_gpu(self, image, operation, kernel, iterations=1):
        """GPU-accelerated morphological operations."""
        if HAS_CUDA:
            try:
                gpu_img = cv2.cuda_GpuMat()
                gpu_img.upload(image)
                gpu_result = cv2.cuda.morphologyEx(gpu_img, operation, kernel, iterations=iterations)
                return gpu_result.download()
            except AttributeError:
                pass
                
        # Fallback to CPU
        return cv2.morphologyEx(image, operation, kernel, iterations=iterations)

# Global GPU accelerator instance
gpu_accel = GPUAccelerator()

def get_gpu_accelerator():
    """Get the global GPU accelerator instance."""
    return gpu_accel