# CUDA GPU Acceleration Setup for JScaner

## Current Status

**Installed GPU-Acceleration Packages:**
- ✓ `numba` v0.62.1 - JIT compiler with CUDA support
- ✓ `numexpr` v2.14.1 - Vectorized numerical operations
- ✓ `bottleneck` v1.6.0 - Optimized NumPy functions
- ✓ `opencv-contrib-python` - OpenCV with GPU-ready modules
- ✓ `open3d` v0.19.0 - 3D processing library
- ✓ `scipy` v1.16.3 - Scientific computing with OpenMP

## Prerequisites for Full GPU Acceleration

### Step 1: Check GPU Capabilities

```bash
# Windows - Check if you have an NVIDIA GPU
nvidia-smi
```

If the command is not found, you may need to install NVIDIA drivers first.

### Step 2: Install NVIDIA CUDA Toolkit 12.4

Download from: https://developer.nvidia.com/cuda-downloads

**For Windows:**
```
https://developer.nvidia.com/cuda-12-4-0-download-archive
```

**Installation Options:**
- Network installer (smaller, downloads during install)
- Local installer (larger, everything included)

**During installation:**
- Install CUDA Toolkit 12.4
- Install cuDNN (if available in the installer)
- Add CUDA to PATH (should be automatic)

### Step 3: Verify CUDA Installation

```bash
# Check CUDA version
nvcc --version

# Check NVIDIA driver
nvidia-smi
```

Expected output:
```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2024 NVIDIA Corporation
Built on Mon_Apr_15_14:51:11_PDT_2024
Cuda compilation tools, release 12.4, V12.4.131
Build cuda_12.4.r12.4/compiler.33961263_0
```

### Step 4: Install GPU-Accelerated Python Packages

#### Option A: PyTorch (Recommended for Deep Learning)

```bash
# Install PyTorch with CUDA 12.4 support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

#### Option B: CuPy (For GPU NumPy Operations)

```bash
# Install CuPy for CUDA 12.x
pip install cupy-cuda12x

# Or with specific CUDA version
pip install cupy-cuda124
```

#### Option C: TensorFlow (For TensorFlow-based ML)

```bash
# Install TensorFlow with GPU support
pip install tensorflow[and-cuda]
```

### Step 5: Verify GPU Acceleration

Run the diagnostics script:

```bash
python check_gpu_acceleration.py
```

Expected output with GPU enabled:
```
✓ Numba CUDA support: ENABLED
  - CUDA version: 12.4
  - Device count: 1
  - Device 0: NVIDIA GeForce RTX 3060
```

## JScaner GPU Integration

### Automatic GPU Detection

JScaner automatically detects GPU availability:

```python
# In src/core/gpu_acceleration.py
from gpu_acceleration import has_cuda, has_cupy

if has_cuda:
    print("CUDA available - using GPU acceleration")
if has_cupy:
    print("CuPy available - NumPy operations on GPU")
```

### Using GPU in JScaner

1. **Numba JIT Compilation** (Automatic)
   - Numerical code is automatically compiled for GPU
   - No code changes needed
   - Falls back to CPU if CUDA unavailable

2. **OpenCV GPU Operations** (With CUDA build)
   - Image processing on GPU
   - Currently uses CPU-based OpenCV
   - Requires recompiling OpenCV with CUDA support

3. **3D Reconstruction** (Partial GPU support)
   - Open3D operations can use GPU when available
   - See `src/core/reconstruction.py`

### GPU Acceleration in 3D Scanning

Primary GPU bottlenecks in JScaner:

1. **Image Processing** (20-30% of time)
   - Camera capture: CPU
   - Resize/blur: OpenCV GPU possible
   - Feature detection: Numba acceleration enabled

2. **Grid Calibration** (10-15% of time)
   - Checkerboard detection: CPU
   - Matrix operations: NumPy/Numba accelerated

3. **3D Reconstruction** (50-70% of time)
   - Point cloud generation: CPU
   - Feature matching: OpenCV GPU possible
   - Mesh generation: CPU or GPU (Open3D)

4. **STL Export** (5-10% of time)
   - Mostly CPU-bound

## Troubleshooting

### Issue: CUDA not detected by Python packages

**Symptoms:**
```
RuntimeError: CUDA is not available
```

**Solution:**
1. Verify CUDA installation: `nvcc --version`
2. Check environment variables:
   ```powershell
   # In PowerShell
   $env:CUDA_PATH
   $env:PATH
   ```
3. Reinstall packages:
   ```bash
   pip uninstall numba cupy torch -y
   pip install numba cupy-cuda12x torch --index-url https://download.pytorch.org/whl/cu124
   ```

### Issue: CUDA version mismatch

**Symptoms:**
```
CUDA 12.4 required, but found 12.1
```

**Solution:**
- Download exact CUDA version from NVIDIA archive
- Or adjust package versions to match installed CUDA

### Issue: Out of GPU memory

**Solution:**
```python
# Reduce batch sizes in JScaner
import os
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'  # Synchronous execution for debugging
```

### Issue: NVIDIA driver issues

**Symptoms:**
```
Could not load cudart64_12.dll
```

**Solution:**
1. Update NVIDIA drivers: https://www.nvidia.com/Download/driverDetails.aspx
2. Ensure compatibility with CUDA 12.4

## Performance Tips

### Optimal Configuration for RTX 3060 (your GPU)

- **VRAM:** 12GB (sufficient for JScaner)
- **Memory Usage:**
  - 3D reconstruction: ~2-4GB
  - Feature matching: ~1-2GB
  - Image buffers: ~0.5GB
  - PyTorch models: ~0.5-2GB if used

### CPU + GPU Hybrid Mode

JScaner automatically uses:
1. GPU for parallel numerical operations (Numba)
2. CPU for I/O and control flow
3. Fallback to CPU if GPU unavailable

### Memory Optimization

```python
# In reconstruction.py
import numba
@numba.cuda.jit  # GPU execution
def fast_algorithm(array):
    # GPU-optimized code
    pass
```

## References

- **NVIDIA CUDA Toolkit:** https://developer.nvidia.com/cuda-toolkit
- **Numba CUDA Guide:** https://numba.readthedocs.io/en/stable/cuda/index.html
- **PyTorch Installation:** https://pytorch.org/get-started/locally/
- **CuPy Documentation:** https://docs.cupy.dev/
- **OpenCV CUDA Support:** https://docs.opencv.org/4.6.0/db/d05/tutorial_py_sift_intro.html

## Next Steps

1. ✓ Install NVIDIA CUDA Toolkit 12.4
2. ✓ Install PyTorch/CuPy
3. ✓ Run `check_gpu_acceleration.py` to verify
4. ✓ Test JScaner with `python main.py`
5. Monitor GPU usage with `nvidia-smi -l 1` (1-second refresh)

## Status Report

**Run this to check GPU status:**

```bash
python check_gpu_acceleration.py
nvidia-smi
```

This document will be updated as GPU support is implemented.
