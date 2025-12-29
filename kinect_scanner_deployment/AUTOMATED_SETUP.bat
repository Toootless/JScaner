@echo off
REM ============================================================================
REM JScaner Kinect Scanner - AUTOMATED INSTALLATION & SETUP
REM Windows 11 Target PC Setup Script
REM ============================================================================
REM
REM This script automates the complete setup process for the Kinect v1 Scanner:
REM 1. Checks system requirements
REM 2. Downloads and installs Python 3.11+ (if needed)
REM 3. Installs Visual C++ redistributable (if needed)
REM 4. Installs Kinect drivers (if needed)
REM 5. Installs Python dependencies
REM 6. Verifies hardware
REM 7. Starts the scanner
REM
REM Usage: Double-click this file or run from command prompt
REM
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo   JScaner - Kinect v1 Scanner
echo   AUTOMATED SETUP & INSTALLATION SCRIPT
echo   Windows 11 Target PC Setup
echo ============================================================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] This script requires Administrator privileges.
    echo.
    echo Please run as Administrator:
    echo   1. Right-click this file
    echo   2. Select "Run as Administrator"
    echo.
    pause
    exit /b 1
)

echo [OK] Running with Administrator privileges
echo.

REM ============================================================================
REM STEP 1: Check Python Installation
REM ============================================================================
echo [STEP 1/7] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Python not found. Downloading Python 3.12...
    echo.
    echo Downloading Python 3.12 from https://www.python.org/downloads/
    powershell -Command "& {
        $url = 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe'
        $output = '%TEMP%\python-3.12.0-amd64.exe'
        try {
            Write-Host 'Downloading Python...' -ForegroundColor Yellow
            (New-Object System.Net.WebClient).DownloadFile($url, $output)
            Write-Host 'Download complete!' -ForegroundColor Green
        } catch {
            Write-Host 'Download failed!' -ForegroundColor Red
            exit 1
        }
    }" || goto :PythonDownloadFailed
    
    echo [INFO] Running Python installer...
    %TEMP%\python-3.12.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 || goto :PythonInstallFailed
    echo [SUCCESS] Python installed
    del %TEMP%\python-3.12.0-amd64.exe
) else (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo [OK] Python found: !PYTHON_VERSION!
)

REM Refresh PATH environment
set "PATH=C:\Program Files\Python312;C:\Program Files\Python312\Scripts;!PATH!"

echo.

REM ============================================================================
REM STEP 2: Install Visual C++ Redistributable
REM ============================================================================
echo [STEP 2/7] Checking Visual C++ Redistributable...

REM Check if Visual C++ is installed by looking for vcruntime140.dll
if exist "C:\Windows\System32\vcruntime140.dll" (
    echo [OK] Visual C++ Redistributable already installed
) else (
    echo [WARNING] Visual C++ Redistributable not found. Downloading...
    echo.
    
    powershell -Command "& {
        $url = 'https://aka.ms/vs/17/release/vc_redist.x64.exe'
        $output = '%TEMP%\vc_redist.x64.exe'
        try {
            Write-Host 'Downloading Visual C++ Redistributable...' -ForegroundColor Yellow
            (New-Object System.Net.WebClient).DownloadFile($url, $output)
            Write-Host 'Download complete!' -ForegroundColor Green
        } catch {
            Write-Host 'Download failed!' -ForegroundColor Red
            exit 1
        }
    }" || goto :VCRedistDownloadFailed
    
    echo [INFO] Running Visual C++ installer...
    %TEMP%\vc_redist.x64.exe /passive /norestart || goto :VCRedistInstallFailed
    echo [SUCCESS] Visual C++ installed
    del %TEMP%\vc_redist.x64.exe
)

echo.

REM ============================================================================
REM STEP 3: Verify Kinect Hardware
REM ============================================================================
echo [STEP 3/7] Checking Kinect hardware...
echo.
echo [INFO] Checking Device Manager for Kinect v1 (Xbox 360 Kinect)...
echo.
echo If Kinect is NOT shown or has a warning icon:
echo   1. Make sure Kinect v1 is connected via USB
echo   2. Ensure Kinect has power (LED should be GREEN)
echo   3. Try different USB port
echo   4. Install drivers from: https://www.microsoft.com/download/details.aspx?id=34808
echo.
pause

REM Open Device Manager to check
start devmgmt.msc

echo.
echo [INFO] Device Manager opened. Look for:
echo   - Cameras: "Kinect" or similar
echo   - Human Interface Devices: "Kinect Sensor"
echo.
echo Press Enter when ready to continue...
pause

echo.

REM ============================================================================
REM STEP 4: Install Python Dependencies
REM ============================================================================
echo [STEP 4/7] Installing Python packages...
echo.

python -m pip install --upgrade pip
if %errorlevel% neq 0 goto :PipUpgradeFailed

REM Get the path to requirements file
set SCRIPT_DIR=%~dp0
set REQUIREMENTS=%SCRIPT_DIR%requirements_kinect_scanner.txt

if exist "!REQUIREMENTS!" (
    echo [INFO] Installing from requirements file...
    python -m pip install -r "!REQUIREMENTS!"
    if %errorlevel% neq 0 goto :PipInstallFailed
) else (
    echo [WARNING] requirements_kinect_scanner.txt not found
    echo [INFO] Installing packages manually...
    python -m pip install opencv-python numpy Pillow tqdm
    if %errorlevel% neq 0 goto :PipInstallFailed
)

echo [SUCCESS] Python packages installed
echo.

REM ============================================================================
REM STEP 5: Test Hardware
REM ============================================================================
echo [STEP 5/7] Testing Kinect hardware...
echo.

if exist "!SCRIPT_DIR!test_kinect_v1.py" (
    python "!SCRIPT_DIR!test_kinect_v1.py"
    if %errorlevel% neq 0 (
        echo.
        echo [WARNING] Hardware test encountered issues.
        echo [INFO] This might be normal if Kinect is not yet connected.
        echo.
    )
) else (
    echo [WARNING] test_kinect_v1.py not found - skipping hardware test
)

echo.

REM ============================================================================
REM STEP 6: Verify Installation
REM ============================================================================
echo [STEP 6/7] Verifying installation...
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 goto :VerificationFailed

python -c "import cv2; print('[OK] OpenCV found')" >nul 2>&1
if %errorlevel% neq 0 goto :OpenCVNotFound

python -c "import numpy; print('[OK] NumPy found')" >nul 2>&1
if %errorlevel% neq 0 goto :NumpyNotFound

echo [SUCCESS] All components verified!
echo.

REM ============================================================================
REM STEP 7: Start Scanner
REM ============================================================================
echo [STEP 7/7] Starting Kinect Scanner...
echo.
echo Your scanner system is ready!
echo.
echo Scanner starting in 5 seconds...
timeout /t 5

if exist "!SCRIPT_DIR!kinect_scanner.py" (
    python "!SCRIPT_DIR!kinect_scanner.py"
) else (
    echo [ERROR] kinect_scanner.py not found
    pause
    exit /b 1
)

goto :Success

REM ============================================================================
REM ERROR HANDLERS
REM ============================================================================

:PythonDownloadFailed
echo [ERROR] Failed to download Python
echo Please download manually from https://www.python.org/downloads/
pause
exit /b 1

:PythonInstallFailed
echo [ERROR] Failed to install Python
echo Please install manually from https://www.python.org/downloads/
echo IMPORTANT: Check "Add Python to PATH" during installation
pause
exit /b 1

:VCRedistDownloadFailed
echo [ERROR] Failed to download Visual C++ Redistributable
echo Please download manually from https://support.microsoft.com/help/2977003
pause
exit /b 1

:VCRedistInstallFailed
echo [ERROR] Failed to install Visual C++ Redistributable
echo Please install manually from https://support.microsoft.com/help/2977003
pause
exit /b 1

:PipUpgradeFailed
echo [ERROR] Failed to upgrade pip
echo Please run: python -m pip install --upgrade pip
pause
exit /b 1

:PipInstallFailed
echo [ERROR] Failed to install Python packages
echo Please run: pip install -r requirements_kinect_scanner.txt
pause
exit /b 1

:VerificationFailed
echo [ERROR] Verification failed - Python not working correctly
pause
exit /b 1

:OpenCVNotFound
echo [ERROR] OpenCV not installed correctly
echo Run: pip install opencv-python
pause
exit /b 1

:NumpyNotFound
echo [ERROR] NumPy not installed correctly
echo Run: pip install numpy
pause
exit /b 1

:Success
echo.
echo ============================================================================
echo [SUCCESS] Installation and setup complete!
echo ============================================================================
echo.
echo You can now run: python kinect_scanner.py
echo.
pause
exit /b 0
