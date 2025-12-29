@echo off
REM Kinect Scanner GUI Launcher
REM Starts the enhanced GUI version with live preview

title Kinect v1 Scanner - GUI Version
color 0A

echo.
echo ============================================================
echo   KINECT v1 SCANNER - GUI VERSION
echo   Live Preview + Image Collection Interface
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11+ from python.org
    pause
    exit /b 1
)

echo [*] Checking dependencies...
python -c "import cv2" >nul 2>&1
if errorlevel 1 (
    echo [!] Installing opencv-python...
    pip install opencv-python
)

python -c "import numpy" >nul 2>&1
if errorlevel 1 (
    echo [!] Installing numpy...
    pip install numpy
)

python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo [!] Installing Pillow...
    pip install Pillow
)

echo [OK] All dependencies ready
echo.
echo [*] Starting GUI Scanner...
echo.

python kinect_scanner_gui.py

if errorlevel 1 (
    echo.
    echo [ERROR] Scanner exited with an error
    pause
)
