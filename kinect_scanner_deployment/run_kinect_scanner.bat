@echo off
REM JScaner Kinect Scanner - Windows 11 Batch Launcher
REM This script sets up and runs the Kinect v1 scanner
REM Usage: Double-click this file or run from PowerShell
REM Last Updated: December 29, 2025

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo   JScaner - Kinect v1 Scanner
echo   Standalone Batch Launcher for Windows 11
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.11+ from: https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
python --version

REM Get the script directory
set SCRIPT_DIR=%~dp0

REM Check if kinect_scanner.py exists
if not exist "%SCRIPT_DIR%kinect_scanner.py" (
    echo.
    echo [ERROR] kinect_scanner.py not found in: %SCRIPT_DIR%
    echo.
    pause
    exit /b 1
)

echo [OK] kinect_scanner.py found
echo.

REM Check if requirements file exists
if exist "%SCRIPT_DIR%requirements_kinect_scanner.txt" (
    echo [SETUP] Installing Python dependencies...
    echo.
    pip install -r "%SCRIPT_DIR%requirements_kinect_scanner.txt"
    
    if errorlevel 1 (
        echo.
        echo [WARNING] Some dependencies may not have installed correctly
        echo Attempting to continue...
        echo.
    )
) else (
    echo [WARNING] requirements_kinect_scanner.txt not found
    echo Installing minimal dependencies manually...
    pip install opencv-python numpy Pillow tqdm
)

echo.
echo ============================================================
echo [STARTUP] Starting Kinect Scanner...
echo ============================================================
echo.

REM Run the scanner
python "%SCRIPT_DIR%kinect_scanner.py"

REM Capture exit code
set EXIT_CODE=%errorlevel%

echo.
echo ============================================================
if %EXIT_CODE% equ 0 (
    echo [DONE] Kinect Scanner closed successfully
) else (
    echo [ERROR] Scanner exited with error code: %EXIT_CODE%
)
echo ============================================================
echo.

pause
exit /b %EXIT_CODE%
