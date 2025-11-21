# JScaner Changelog

## Version 1.1.0 - November 14, 2025

### 🎉 **Major Feature: Python 3.14 Compatibility**
- **Added** comprehensive Python 3.14 support with fallback reconstruction
- **Added** `reconstruction_fallback.py` module using SciPy and scikit-learn
- **Added** `stl_fallback.py` for manual STL export when Open3D unavailable
- **Added** intelligent detection and graceful degradation for missing Open3D

### ⚡ **GPU Acceleration Enhancements**
- **Added** NVIDIA CuPy integration for GPU-accelerated image processing
- **Added** `gpu_acceleration.py` module with memory pool optimization
- **Added** GPU-accelerated Harris corner detection
- **Added** Intelligent CPU/GPU switching based on workload characteristics
- **Improved** performance benchmarking showing 1.2-1.3x speedup on large images

### 🔍 **Enhanced Grid Detection**
- **Added** multiple grid detection algorithms: line-based, fine dot patterns, cross patterns
- **Added** support for 3D printer bed patterns (gold background with white lines)
- **Added** automatic pattern size detection (tested: 5x4 through 8x11 grids)
- **Added** CLAHE preprocessing for improved contrast
- **Improved** clustering and row organization algorithms
- **Added** comprehensive debug image output for troubleshooting

### 🛠️ **Reconstruction System Overhaul**
- **Added** `Point3DReconstruction` class for Open3D-free 3D reconstruction
- **Added** SciPy-based stereo triangulation
- **Added** Statistical outlier filtering using KD-trees
- **Added** Normal estimation for point clouds
- **Added** Poisson and Alpha Shape mesh reconstruction fallbacks
- **Enhanced** STL export with both Open3D and manual binary/ASCII writers

### 📚 **Documentation & Setup**
- **Updated** README.md with Python 3.14 installation instructions
- **Created** `PYTHON_314_SETUP.md` comprehensive setup guide
- **Updated** `PROJECT_SUMMARY.md` with latest achievements
- **Enhanced** `API_REFERENCE.md` with fallback class documentation
- **Updated** `requirements.txt` with Python 3.14 compatible dependencies

### 🔧 **Technical Improvements**
- **Added** compatibility layer in `main.py` for Open3D detection
- **Enhanced** error handling and user notifications
- **Added** mesh validation and information extraction utilities
- **Improved** camera diagnostics and GPU device detection
- **Added** comprehensive feature compatibility matrix

### 🐛 **Bug Fixes & Stability**
- **Fixed** import errors when Open3D not available
- **Fixed** type annotations for dynamic reconstruction backends
- **Improved** memory management for GPU operations
- **Enhanced** error messages and fallback notifications

---

## Version 1.0.0 - November 13, 2025

### 🎯 **Initial Release**
- **Core 3D Scanning Pipeline**: Multi-view stereo reconstruction from photographs
- **Logitech C920 Support**: Optimized camera integration with DirectShow backend
- **Grid-based Calibration**: Accurate measurements using reference patterns
- **STL Export**: 3D printing-ready file generation
- **Interactive GUI**: Tab-based workflow interface
- **Advanced Computer Vision**: SIFT feature detection and matching

### 📁 **Project Structure**
- `src/core/`: Core algorithms for image capture, calibration, and reconstruction
- `src/gui/`: User interface components
- `data/`: Sample calibration patterns and test images
- `docs/`: Comprehensive documentation and API reference
- `examples/`: Usage examples and tutorials

### 🔧 **Core Features**
- Camera diagnostics and optimization
- Multi-algorithm grid detection
- Feature detection and matching
- 3D point cloud generation
- Mesh reconstruction
- STL file validation

---

## Migration Guide

### From Version 1.0.0 to 1.1.0

#### For Python 3.14 Users (New)
1. Install Python 3.14 dependencies:
   ```bash
   pip install opencv-python numpy scipy scikit-learn matplotlib tqdm cupy-cuda12x
   ```
2. Run JScaner - fallback reconstruction will be used automatically

#### For Python 3.11-3.13 Users (Existing)
1. Update dependencies:
   ```bash
   pip install --upgrade cupy-cuda12x scikit-learn
   ```
2. Existing workflows remain unchanged - Open3D will be used when available

#### API Changes
- `StereoReconstructor.reconstruct_from_images()` now returns `object` instead of `o3d.geometry.PointCloud`
- `STLExporter.export_mesh_to_stl()` now accepts `object` mesh parameter instead of `o3d.geometry.TriangleMesh`
- New classes: `Point3DReconstruction`, `GPUAccelerator`
- Enhanced grid detection methods with additional parameters

#### Configuration Updates
- GPU memory pool settings for optimal performance
- Enhanced camera optimization parameters
- New debug image output options

---

## Upcoming Features (Roadmap)

### Version 1.2.0 (Planned)
- **Multi-GPU support** for workstation setups
- **Advanced mesh repair** algorithms
- **Texture mapping** from source photographs
- **Real-time preview** of 3D reconstruction
- **Batch processing** for multiple objects

### Version 1.3.0 (Planned)
- **Cloud processing** integration
- **Mobile app** for remote image capture
- **AI-enhanced** grid detection
- **Quality assessment** metrics
- **Professional calibration targets**

---

## Known Issues

### Python 3.14
- Open3D not yet available, fallback reconstruction has limitations
- Some advanced mesh processing features require Python 3.11-3.13
- PyMeshLab and trimesh may not be available for complex mesh operations

### GPU Acceleration
- Requires NVIDIA GPU with CUDA 11.0+ support
- Memory usage may be high for very large images
- AMD GPU support not yet implemented

### Grid Detection
- 3D printer bed patterns still challenging for very fine grids
- Complex lighting conditions may affect detection accuracy
- Standard checkerboard patterns recommended for best results

---

## Contributing

### Development Setup
1. Fork the repository
2. Install development dependencies
3. Run tests: `python -m pytest tests/`
4. Submit pull request

### Bug Reports
- Include Python version and GPU information
- Attach debug images if grid detection issues
- Provide minimal reproduction case

### Feature Requests
- Check roadmap for planned features
- Discuss in issues before implementing
- Consider backward compatibility

---

## Credits

- **OpenCV Team**: Computer vision algorithms
- **Open3D Team**: 3D geometry processing
- **NVIDIA**: CuPy GPU acceleration
- **SciPy Community**: Scientific computing fallbacks
- **Contributors**: Testing and feedback

## License

This project is licensed under the MIT License - see LICENSE file for details.