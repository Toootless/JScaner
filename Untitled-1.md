pip install pykinect2# 1. Install vcpkg (one-time setup)
git clone https://github.com/Microsoft/vcpkg.git C:\vcpkg
cd C:\vcpkg
.\bootstrap-vcpkg.bat

# 2. Build libfreenect for Windows
C:\vcpkg\vcpkg install libfreenect:x64-windows

# 3. Copy the DLL to JScaner
Copy-Item "C:\vcpkg\installed\x64-windows\bin\freenect.dll" `
  -Destination "C:\Users\johnj\OneDrive\Documents\VS_projects\3dscaning\freenect.dll"

# 4. Restart JScaner
cd c:\Users\johnj\OneDrive\Documents\VS_projects\3dscaning
python main.py