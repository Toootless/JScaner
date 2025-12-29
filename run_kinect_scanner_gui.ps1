#!/usr/bin/env pwsh
# Kinect Scanner GUI Launcher (PowerShell)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  KINECT v1 SCANNER - GUI VERSION" -ForegroundColor Cyan
Write-Host "  Live Preview + Image Collection Interface" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[*] Checking Python installation..." -ForegroundColor Yellow
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[OK] Python found: $pythonCheck" -ForegroundColor Green
Write-Host ""

# Check dependencies
Write-Host "[*] Checking dependencies..." -ForegroundColor Yellow

$deps = @("cv2", "numpy", "PIL")
foreach ($dep in $deps) {
    $check = python -c "import $dep" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[!] Installing $dep..." -ForegroundColor Yellow
        if ($dep -eq "cv2") {
            pip install opencv-python
        } elseif ($dep -eq "PIL") {
            pip install Pillow
        } else {
            pip install $dep
        }
    }
}

Write-Host "[OK] All dependencies ready" -ForegroundColor Green
Write-Host ""
Write-Host "[*] Starting GUI Scanner..." -ForegroundColor Yellow
Write-Host ""

python kinect_scanner_gui.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Scanner exited with error code: $LASTEXITCODE" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
