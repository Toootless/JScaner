#!/usr/bin/env python3
"""
Check GPU acceleration capabilities in JScaner environment
Verifies installed CUDA-related packages and their functionality
"""

import sys
import platform

def check_gpu_packages():
    """Check for GPU acceleration packages."""
    
    print("=" * 70)
    print("JScaner GPU Acceleration Diagnostics")
    print("=" * 70)
    print(f"\nSystem: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Architecture: {platform.machine()}\n")
    
    # Check installed packages
    packages_to_check = {
        "numba": "JIT compilation for CUDA-compatible CPUs",
        "numexpr": "Vectorized numerical expressions",
        "bottleneck": "Optimized NumPy functions",
        "numpy": "Numerical computing foundation",
        "opencv-contrib-python": "Advanced OpenCV features (CUDA-ready when compiled)",
        "scipy": "Scientific computing library",
        "scikit-image": "Image processing with GPU potential",
        "open3d": "3D data processing library",
        "torch": "PyTorch (CUDA support if installed)",
        "tensorflow": "TensorFlow (CUDA support if installed)",
    }
    
    print("Installed GPU-Related Packages:")
    print("-" * 70)
    
    gpu_available = False
    
    for package_name, description in packages_to_check.items():
        try:
            module = __import__(package_name)
            version = getattr(module, "__version__", "Unknown")
            
            # Check for CUDA support
            cuda_support = "❌"
            if package_name == "numba":
                try:
                    from numba import cuda as nb_cuda
                    if nb_cuda.is_available():
                        cuda_support = "✓ CUDA"
                        gpu_available = True
                    else:
                        cuda_support = "⚠ No CUDA"
                except:
                    cuda_support = "⚠ Limited"
            elif package_name == "torch":
                try:
                    if module.cuda.is_available():
                        cuda_support = f"✓ CUDA {module.version.cuda}"
                        gpu_available = True
                    else:
                        cuda_support = "⚠ CPU only"
                except:
                    pass
            elif package_name == "tensorflow":
                try:
                    gpu_devices = module.config.list_physical_devices('GPU')
                    if gpu_devices:
                        cuda_support = f"✓ CUDA ({len(gpu_devices)} GPUs)"
                        gpu_available = True
                    else:
                        cuda_support = "⚠ No GPUs"
                except:
                    cuda_support = "⚠ Unknown"
            elif package_name == "open3d":
                cuda_support = "✓ Available" if version != "Unknown" else "❌"
            elif package_name == "opencv-contrib-python":
                try:
                    import cv2
                    build_info = cv2.getBuildInformation()
                    if "CUDA" in build_info:
                        cuda_support = "✓ CUDA"
                    else:
                        cuda_support = "⚠ CPU (recompile for CUDA)"
                except:
                    cuda_support = "⚠ Check manually"
            elif package_name in ["scipy", "scikit-image"]:
                cuda_support = "✓ CPU/OpenMP"
            
            status = "✓" if version != "Unknown" else "⚠"
            print(f"{status} {package_name:30} v{version:15} | {cuda_support}")
            
        except ImportError:
            print(f"❌ {package_name:30} {'Not installed':15} | N/A")
    
    print("\n" + "=" * 70)
    print("GPU Acceleration Status:")
    print("-" * 70)
    
    if gpu_available:
        print("✓ GPU acceleration is ENABLED and ready!")
        print("\nConfigured GPU packages:")
        print("  • Numba: JIT compilation for numerical code")
        print("  • PyTorch/TensorFlow: If installed with CUDA support")
        print("  • OpenCV: GPU acceleration available")
        return True
    else:
        print("⚠ GPU acceleration is NOT fully configured")
        print("\nTo enable GPU acceleration:")
        print("  1. Install NVIDIA CUDA Toolkit (12.4 or compatible)")
        print("  2. Install cuDNN libraries")
        print("  3. Reinstall PyTorch with CUDA support:")
        print("     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124")
        print("  4. For CuPy (NumPy on GPU):")
        print("     pip install cupy-cuda12x")
        print("  5. Recompile OpenCV with CUDA support")
        print("\nAlternatively, CPU optimization is configured with:")
        print("  • Numba: JIT compilation")
        print("  • NumExpr: Vectorized operations")
        print("  • OpenMP: Multi-threaded CPU operations")
        return False
    
    print("\n" + "=" * 70)

def check_numba_cuda():
    """Check Numba CUDA capabilities."""
    print("\nNumba CUDA Diagnostics:")
    print("-" * 70)
    try:
        from numba import cuda
        
        if cuda.is_available():
            print("✓ Numba CUDA support: ENABLED")
            print(f"  - CUDA version: {cuda.runtime.get_version()}")
            print(f"  - Device count: {cuda.device_count()}")
            
            for i in range(cuda.device_count()):
                device = cuda.get_current_device()
                print(f"  - Device {i}: {device.name if hasattr(device, 'name') else 'Unknown'}")
        else:
            print("⚠ Numba CUDA support: DISABLED (CUDA not available)")
            print("  Install NVIDIA CUDA Toolkit to enable GPU acceleration")
    except ImportError:
        print("❌ Numba not installed")
    except Exception as e:
        print(f"⚠ Error checking Numba CUDA: {e}")

def main():
    """Run all GPU checks."""
    check_gpu_packages()
    check_numba_cuda()
    print("\n" + "=" * 70)
    print("For more information, visit:")
    print("  - https://numba.pydata.org/numba-doc/latest/cuda/")
    print("  - https://pytorch.org/get-started/locally/")
    print("  - https://docs.nvidia.com/cuda/")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
