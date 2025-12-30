@echo off
REM JScaner - Image Processing Launcher
REM Processes captured images and metadata for 3D reconstruction

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Launch the image processor
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║          JScaner - Image Processing Mode                    ║
echo ║    Processing captured images and metadata files             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Launching application...
echo.

cd /d "%SCRIPT_DIR%"

python main_processor.py

if errorlevel 1 (
    echo.
    echo Error launching application. Trying with python3...
    python3 main_processor.py
)

pause
