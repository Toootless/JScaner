# JScaner Kinect Scanner - PowerShell Launcher Script
# Usage: .\run_kinect_scanner.ps1
# Last Updated: December 29, 2025

Write-Host ""
Write-Host "============================================================"
Write-Host "  JScaner - Kinect v1 Scanner"
Write-Host "  Standalone PowerShell Launcher for Windows 11"
Write-Host "============================================================"
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion"
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.11+ from: https://www.python.org/downloads/"
    Write-Host "IMPORTANT: Check 'Add Python to PATH' during installation"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if kinect_scanner.py exists
$ScannerPath = Join-Path $ScriptDir "kinect_scanner.py"
if (-not (Test-Path $ScannerPath)) {
    Write-Host "[ERROR] kinect_scanner.py not found in: $ScriptDir" -ForegroundColor Red
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] kinect_scanner.py found"
Write-Host ""

# Check and install requirements
$RequirementsPath = Join-Path $ScriptDir "requirements_kinect_scanner.txt"
if (Test-Path $RequirementsPath) {
    Write-Host "[SETUP] Installing Python dependencies..."
    Write-Host ""
    
    & python -m pip install -r $RequirementsPath
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[WARNING] Some dependencies may not have installed correctly" -ForegroundColor Yellow
        Write-Host "Attempting to continue..."
        Write-Host ""
    }
} else {
    Write-Host "[WARNING] requirements_kinect_scanner.txt not found" -ForegroundColor Yellow
    Write-Host "Installing minimal dependencies manually..."
    Write-Host ""
    
    & python -m pip install opencv-python numpy Pillow tqdm
}

Write-Host ""
Write-Host "============================================================"
Write-Host "[STARTUP] Starting Kinect Scanner..."
Write-Host "============================================================"
Write-Host ""

# Run the scanner
& python $ScannerPath
$ExitCode = $LASTEXITCODE

Write-Host ""
Write-Host "============================================================"
if ($ExitCode -eq 0) {
    Write-Host "[DONE] Kinect Scanner closed successfully"
} else {
    Write-Host "[ERROR] Scanner exited with error code: $ExitCode" -ForegroundColor Red
}
Write-Host "============================================================"
Write-Host ""

Read-Host "Press Enter to exit"
exit $ExitCode
