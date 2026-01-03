# VORTEX 2026 Windows Build & Distribution Guide

**Build Date:** January 3, 2026  
**Platform:** Windows 10/11 (x64)  
**Python Version:** 3.12+  

---

## Table of Contents
1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Build Process](#build-process)
4. [Distribution Package](#distribution-package)
5. [Code Signing](#code-signing)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Option A: Automated Build (Recommended)

**PowerShell (Windows 10/11):**
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\build.ps1
```

**Command Prompt (CMD):**
```batch
build.bat
```

### Option B: Manual Build

```powershell
# 1. Install dependencies
pip install -r build_requirements.txt

# 2. Run PyInstaller
pyinstaller --onefile --name vortex pyinstaller_config.spec

# 3. Create ZIP
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory('dist\vortex', 'vortex_0.1.0_windows.zip')
```

---

## Prerequisites

### System Requirements
- **OS:** Windows 10 Build 19041+ or Windows 11
- **RAM:** Minimum 4 GB (8 GB recommended)
- **Disk:** 2 GB free space
- **Architecture:** x64 (64-bit) only

### Software Requirements

#### 1. Python 3.12+
```powershell
# Download from https://www.python.org/downloads/
# Or use Windows Package Manager:
winget install Python.Python.3.12

# Verify installation
python --version
python -m pip --version
```

#### 2. Git (for cloning repository)
```powershell
winget install Git.Git
# or download from https://git-scm.com/download/win
```

#### 3. Visual C++ Build Tools (Required for cryptography module)
```powershell
# Option 1: Visual Studio Community (includes build tools)
# Download from https://visualstudio.microsoft.com/downloads/

# Option 2: Standalone Build Tools
# Download from https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Verify installation
cl.exe /version
```

### Directory Structure
```
red-team-osint-tool/
├── src/
│   └── vortex/
│       ├── cli/
│       │   └── main.py          (CLI entry point)
│       ├── collectors/          (OSINT collection modules)
│       ├── processors/          (Data processing pipeline)
│       ├── storage/             (Database backends)
│       └── export/              (Output formatters)
├── config/
│   ├── vortex.yaml            (Configuration template)
│   └── keys/                   (Signing keys directory)
├── tests/                       (Unit tests)
├── pyinstaller_config.spec      (PyInstaller specification)
├── build_requirements.txt       (Build dependencies)
├── build.ps1                    (PowerShell build script)
├── build.bat                    (CMD build script)
├── README.md
└── LICENSE
```

---

## Build Process

### Step-by-Step Execution

#### 1. Clone Repository
```powershell
git clone https://github.com/POWDER-RANGER/red-team-osint-tool.git
cd red-team-osint-tool
```

#### 2. Create Virtual Environment (Recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### 3. Install Dependencies
```powershell
# Install runtime dependencies
pip install -r requirements.txt

# Install build dependencies
pip install -r build_requirements.txt
```

#### 4. Verify Entry Point
Ensure `src/vortex/cli/main.py` exists and contains:
```python
if __name__ == "__main__":
    # CLI application entry point
    asyncio.run(main())
```

#### 5. Build Assets
```powershell
# Create assets directory with icon
mkdir assets -Force

# (Optional) Create custom icon
# Use online tool: https://icoconvert.com/ to convert PNG -> ICO
# Save as: assets/vortex.ico
```

#### 6. Run Build
**PowerShell (Recommended):**
```powershell
# Verbose output
.\build.ps1 -Verbose

# Clean previous build and rebuild
.\build.ps1 -Clean

# With code signing (production)
.\build.ps1 -Sign -CertPath "C:\path\to\certificate.pfx"
```

**Command Prompt:**
```batch
build.bat
```

#### 7. Verify Output
```powershell
# Test executable
.\dist\vortex_dist\vortex.exe --help

# Check ZIP contents
Expand-Archive vortex_0.1.0_windows.zip -DestinationPath test_extract
dir test_extract\vortex_dist
```

---

## Distribution Package

### Package Contents

The generated `vortex_0.1.0_windows.zip` includes:

```
vortex_0.1.0_windows/
├── vortex.exe                    (Executable - 45-60 MB)
├── config.example.yaml           (Configuration template)
├── README.md                      (Documentation)
├── LICENSE                        (MIT License)
├── MANIFEST.json                 (Build metadata)
└── [embedded dependencies]        (Included in .EXE)
```

### File Sizes

| Component | Size | Notes |
|-----------|------|-------|
| `vortex.exe` | ~50 MB | Includes all dependencies |
| `vortex_0.1.0_windows.zip` | ~40 MB | Compressed package |
| Extracted size | ~120 MB | Including documentation |

### Distribution Methods

#### 1. Direct Download
```powershell
# Host on GitHub Releases
# Upload: vortex_0.1.0_windows.zip
# Users: Download → Extract → Run vortex.exe
```

#### 2. Package Manager
```powershell
# Windows Package Manager
winget install vortex-osint

# Chocolatey
choco install vortex-osint
```

#### 3. MSI Installer (Advanced)
```powershell
# Use WiX Toolset to create installer
# File: vortex_installer.msi
# Handles registry, shortcuts, uninstall
```

---

## Code Signing

### Why Code Sign?

- **Trust:** Users see your publisher name, not "Unknown Publisher"
- **SmartScreen:** Avoids Windows SmartScreen warnings
- **UAC:** Reduces User Account Control elevation prompts
- **Legal:** Required for enterprise distribution

### Process

#### 1. Obtain Code Signing Certificate

**Option A: Commercial Certificate (EV Code Signing)**
- Cost: $200-500/year
- Providers: DigiCert, Sectigo, GlobalSign
- Time: 5-7 business days

**Option B: Internal Test Certificate (Development Only)**
```powershell
# Create self-signed certificate for testing
$cert = New-SelfSignedCertificate `
  -Subject "CN=VORTEX Development" `
  -Type CodeSigningCert `
  -HashAlgorithm SHA256 `
  -NotAfter (Get-Date).AddMonths(12)

Export-PfxCertificate -Cert $cert -FilePath vortex_test.pfx -PasswordProtected
```

#### 2. Sign Executable

```powershell
# Using PowerShell (recommended)
$params = @{
    FilePath      = "dist\vortex_dist\vortex.exe"
    CertificatePath = "C:\path\to\certificate.pfx"
    TimeStampServer = "http://timestamp.digicert.com"
}
Set-AuthenticodeSignature @params

# Or using signtool (Windows SDK)
signtool.exe sign /f certificate.pfx /t http://timestamp.digicert.com `
  /fd SHA256 /v dist\vortex_dist\vortex.exe

# Verify signature
Get-AuthenticodeSignature dist\vortex_dist\vortex.exe
```

#### 3. Timestamp Server

Use a trusted timestamp authority:
- **DigiCert:** `http://timestamp.digicert.com`
- **Sectigo:** `http://timestamp.sectigo.com`
- **GlobalSign:** `http://timestamp.globalsign.com`

**Why timestamp?** Prevents certificate expiration from invalidating signature.

---

## Troubleshooting

### Build Fails: "Python not found"

```powershell
# Check Python installation
python --version

# If not in PATH, use full path
"C:\Python312\python.exe" --version

# Add to PATH
[Environment]::SetEnvironmentVariable(
  "Path",
  [Environment]::GetEnvironmentVariable("Path", "Machine") + ";C:\Python312",
  "Machine"
)
```

### Build Fails: "Cryptography module requires compiler"

```powershell
# Install Visual C++ Build Tools
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Or upgrade pip/setuptools
pip install --upgrade pip setuptools wheel

# Then rebuild
pip install -r build_requirements.txt
```

### Build Fails: "Module not found"

```powershell
# Missing hidden imports - update pyinstaller_config.spec
# Add module to hiddenimports list:
hiddenimports=[
    'vortex.new_module',  # Add here
    # ...
]

# Then rebuild
pyinstaller pyinstaller_config.spec
```

### ZIP Creation Fails

```powershell
# PowerShell method (fallback to 7-Zip)
# Install 7-Zip: https://www.7-zip.org/

# Use 7-Zip directly
& "C:\Program Files\7-Zip\7z.exe" a vortex_0.1.0_windows.zip dist\vortex_dist\*
```

### Executable Crashes on Startup

```powershell
# Check event logs
Get-EventLog Application | Where-Object {$_.Source -eq "vortex"} | 
  Select-Object TimeGenerated, Message | Sort-Object TimeGenerated -Descending

# Run with diagnostic mode
$env:VORTEX_DEBUG = "1"
.\vortex.exe --help

# Verify dependencies are bundled
dumpbin.exe /imports dist\vortex_dist\vortex.exe | grep -E "\.dll"
```

### File Permissions Issue

```powershell
# Ensure write permissions in distribution directory
New-Item -Path "C:\Program Files\VORTEX" -ItemType Directory -Force
icacls "C:\Program Files\VORTEX" /grant:r "$env:USERNAME:(OI)(CI)M"

# Move executable
Move-Item dist\vortex_dist\vortex.exe "C:\Program Files\VORTEX\"
```

---

## Advanced Options

### Custom Entry Point

Modify `pyinstaller_config.spec` to use different entry point:

```python
a = Analysis(
    ['src/vortex/cli/main.py'],  # Change this
    # ...
)
```

### Windowed Application (GUI Mode)

```python
exe = EXE(
    # ...
    console=False,  # Change to False for GUI
    icon='assets/vortex.ico',
)
```

### Single-File vs. Directory

```bash
# Single-file executable (recommended)
pyinstaller --onefile pyinstaller_config.spec

# Directory structure (faster builds)
pyinstaller --onedir pyinstaller_config.spec
```

### UPX Compression (Optional)

```powershell
# Download UPX: https://upx.github.io/
# Place in PATH, then UPX automatically compresses binary

# Disable UPX compression
# In pyinstaller_config.spec:
# upx=False
```

---

## Deployment Checklist

- [ ] Python 3.12+ installed and in PATH
- [ ] Visual C++ Build Tools installed
- [ ] Repository cloned and updated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Build dependencies installed (`pip install -r build_requirements.txt`)
- [ ] Assets directory created (`mkdir assets`)
- [ ] Icon file present (optional: `assets/vortex.ico`)
- [ ] Entry point verified (`src/vortex/cli/main.py`)
- [ ] Build script executed (`.\build.ps1` or `build.bat`)
- [ ] Output verified:
  - [ ] `vortex.exe` exists and runs
  - [ ] ZIP file created and extractable
  - [ ] File signatures correct
- [ ] Code signing completed (production)
- [ ] Distribution ZIP uploaded to GitHub/CDN
- [ ] Release notes published
- [ ] User documentation updated

---

## Additional Resources

- **PyInstaller Docs:** https://pyinstaller.readthedocs.io/
- **Code Signing Guide:** https://learn.microsoft.com/en-us/windows/win32/seccrypto/code-signing
- **Windows Defender SmartScreen:** https://learn.microsoft.com/en-us/windows/security/threat-protection/windows-defender-smartscreen/
- **VORTEX Repository:** https://github.com/POWDER-RANGER/red-team-osint-tool

---

## Support

For build issues, refer to:
1. Build logs: `build_YYYYMMDD_HHMMSS.log`
2. PyInstaller issues: `pyinstaller_config.spec` hiddenimports
3. Repository issues: https://github.com/POWDER-RANGER/red-team-osint-tool/issues