#!/usr/bin/env pwsh
# Kinect Scanner GUI Launcher - Python 3.9 for Kinect v1 Support

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  KINECT v1 SCANNER - GUI VERSION (Python 3.9)" -ForegroundColor Cyan
Write-Host "  Live Preview + Image Collection Interface" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Use Python 3.9 for Kinect v1 .NET SDK support
$python39 = "C:\Users\johnj\AppData\Local\Programs\Python\Python39\python.exe"

Write-Host "[*] Checking Python 3.9 installation..." -ForegroundColor Yellow
if (-not (Test-Path $python39)) {
    Write-Host "[ERROR] Python 3.9 not found at: $python39" -ForegroundColor Red
    Write-Host "Please install Python 3.9 from python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

$pythonCheck = & $python39 --version 2>&1
Write-Host "[OK] Python found: $pythonCheck" -ForegroundColor Green
Write-Host ""

# Check dependencies
Write-Host "[*] Checking dependencies..." -ForegroundColor Yellow

$deps = @{
    "cv2" = "opencv-python"
    "numpy" = "numpy"
    "PIL" = "Pillow"
    "clr" = "pythonnet"
}

foreach ($module in $deps.Keys) {
    & $python39 -c "import $module" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[!] Installing $($deps[$module])..." -ForegroundColor Yellow
        & $python39 -m pip install $deps[$module] --user
    }
}

Write-Host "[OK] All dependencies ready" -ForegroundColor Green
Write-Host ""
Write-Host "[*] Starting GUI Scanner with Kinect v1 support..." -ForegroundColor Yellow
Write-Host ""

& $python39 kinect_scanner_gui.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Scanner exited with error code: $LASTEXITCODE" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
