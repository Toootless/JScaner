# Kinect Device Status Check (No admin required)

Write-Host "Kinect Device Status Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check SDK
$sdk = Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Kinect" -ErrorAction SilentlyContinue
if ($sdk) {
    Write-Host "OK - Kinect SDK v1.8 installed" -ForegroundColor Green
} else {
    Write-Host "NOT FOUND - Kinect SDK" -ForegroundColor Red
}

Write-Host ""
Write-Host "Kinect Devices:" -ForegroundColor Yellow
Get-PnpDevice -FriendlyName "*kinect*" | Format-Table FriendlyName, Status, Class -AutoSize

$broken = @(Get-PnpDevice -FriendlyName "*kinect*" | Where-Object {$_.Status -ne 'OK'})
$ok = @(Get-PnpDevice -FriendlyName "*kinect*" | Where-Object {$_.Status -eq 'OK'})

Write-Host ""
Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "  Working: $($ok.Count) devices" -ForegroundColor Green
Write-Host "  Broken:  $($broken.Count) devices" -ForegroundColor $(if ($broken.Count -gt 0) { "Red" } else { "Green" })

if ($broken.Count -gt 0) {
    Write-Host ""
    Write-Host "FIX NEEDED:" -ForegroundColor Red
    Write-Host "1. Right-click PowerShell icon -> Run as Administrator" -ForegroundColor Yellow
    Write-Host "2. cd to this folder" -ForegroundColor Yellow
    Write-Host "3. Run: .\fix_kinect_drivers.ps1" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "OR manually:" -ForegroundColor Yellow
    Write-Host "  Device Manager -> Kinect devices -> Uninstall -> Replug USB" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "All devices OK! Now test camera detection:" -ForegroundColor Green
    Write-Host "  python find_kinect_camera.py" -ForegroundColor Yellow
}

Write-Host ""
