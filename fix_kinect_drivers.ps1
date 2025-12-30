# Fix Kinect v1 Driver Issues
# Run as Administrator

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Kinect v1 Driver Repair Tool" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Right-click this file and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Checking Kinect SDK installation..." -ForegroundColor Yellow
$sdkPath = Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Kinect" -ErrorAction SilentlyContinue

if ($null -eq $sdkPath) {
    Write-Host "ERROR: Kinect SDK v1.8 not found!" -ForegroundColor Red
    Write-Host "Please install from: https://www.microsoft.com/en-us/download/details.aspx?id=40278" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "OK - Kinect SDK v1.8 found at: $($sdkPath.SDKInstallPath)" -ForegroundColor Green
Write-Host ""
Write-Host "Current Kinect device status:" -ForegroundColor Yellow
Get-PnpDevice -FriendlyName "*kinect*" | Format-Table FriendlyName, Status, Class -AutoSize
Write-Host ""

$brokenDevices = Get-PnpDevice -FriendlyName "*kinect*" | Where-Object {$_.Status -ne 'OK'}
$brokenCount = ($brokenDevices | Measure-Object).Count

if ($brokenCount -eq 0) {
    Write-Host "OK - All Kinect devices are working!" -ForegroundColor Green
    Write-Host "If camera still not detected, try unplugging and replugging Kinect USB" -ForegroundColor Yellow
    pause
    exit 0
}

Write-Host "Found $brokenCount device(s) with issues - attempting fix..." -ForegroundColor Yellow
Write-Host ""

# Disable and re-enable each broken device
foreach ($device in $brokenDevices) {
    Write-Host "Resetting: $($device.FriendlyName)" -ForegroundColor White
    Disable-PnpDevice -InstanceId $device.InstanceId -Confirm:$false -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Enable-PnpDevice -InstanceId $device.InstanceId -Confirm:$false -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

Write-Host "Updating drivers..." -ForegroundColor Cyan
foreach ($device in $brokenDevices) {
    Update-PnpDevice -InstanceId $device.InstanceId -Confirm:$false -ErrorAction SilentlyContinue
}

Start-Sleep -Seconds 3
Write-Host ""
Write-Host "Results:" -ForegroundColor Yellow
Get-PnpDevice -FriendlyName "*kinect*" | Format-Table FriendlyName, Status, Class -AutoSize

$stillBroken = Get-PnpDevice -FriendlyName "*kinect*" | Where-Object {$_.Status -ne 'OK'}
$stillBrokenCount = ($stillBroken | Measure-Object).Count

if ($stillBrokenCount -eq 0) {
    Write-Host "SUCCESS - All devices fixed!" -ForegroundColor Green
    Write-Host "Run: python find_kinect_camera.py" -ForegroundColor Yellow
} else {
    Write-Host "Still $stillBrokenCount device(s) broken" -ForegroundColor Yellow
    Write-Host "Manual fix needed - see KINECT_NOT_DETECTED.md" -ForegroundColor Yellow
}

pause
