@echo off
REM Kinect Scanner GUI Launcher - Python 3.9 for Kinect v1 Support
REM Starts the enhanced GUI version with live preview and Kinect v1 via .NET SDK

title Kinect v1 Scanner - GUI Version
color 0A

echo.
echo ============================================================
echo   KINECT v1 SCANNER - GUI VERSION (Python 3.9)
echo   Live Preview + Image Collection Interface
echo ============================================================
echo.

REM Use Python 3.9 for Kinect v1 .NET SDK support
set PYTHON39=C:\Users\johnj\AppData\Local\Programs\Python\Python39\python.exe

if not exist "%PYTHON39%" (
    echo [ERROR] Python 3.9 not found at: %PYTHON39%
    echo Please install Python 3.9 from python.org
    pause
    exit /b 1
)

echo [*] Using Python 3.9 for Kinect v1 support
%PYTHON39% --version
echo.

echo [*] Checking dependencies
%PYTHON39% -c "import cv2" >nul 2>&1
if errorlevel 1 (
    echo [+] Installing opencv-python
    %PYTHON39% -m pip install opencv-python --user
)

%PYTHON39% -c "import numpy" >nul 2>&1
if errorlevel 1 (
    echo [+] Installing numpy
    %PYTHON39% -m pip install numpy --user
)

%PYTHON39% -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo [+] Installing Pillow
    %PYTHON39% -m pip install Pillow --user
)

%PYTHON39% -c "import clr" >nul 2>&1
if errorlevel 1 (
    echo [+] Installing pythonnet required for Kinect
    %PYTHON39% -m pip install pythonnet --user
)

echo [OK] All dependencies ready
echo.
echo [*] Starting GUI Scanner with Kinect v1 support
echo.

%PYTHON39% kinect_scanner_gui.py

if errorlevel 1 (
    echo.
    echo [ERROR] Scanner exited with an error
    pause
)
