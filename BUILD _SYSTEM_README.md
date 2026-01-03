# VORTEX 2026 - Windows Build & Distribution System

**Version:** 0.1.0  
**Last Updated:** January 3, 2026  
**Platform Support:** Windows 10/11 (x64)  
**Python:** 3.12+

---

## Overview

This build system compiles the **red-team-osint-tool** (VORTEX) into production-grade Windows executables (.EXE) and distributable ZIP packages with zero external dependencies.

### What You Get

```
vortex_0.1.0_windows.zip (≈40 MB)
├── vortex.exe                (50 MB executable - fully self-contained)
├── config.example.yaml       (Configuration template)
├── README.md                 (User documentation)
├── LICENSE                   (MIT)
└── MANIFEST.json            (Build metadata & checksums)
```

**Key Features:**
- ✅ Single executable - no Python installation required on target machine
- ✅ All dependencies bundled (asyncpg, cryptography, aiohttp, etc.)
- ✅ Code signing ready (production certificates)
- ✅ Windows Defender SmartScreen compatible
- ✅ Automated CI/CD pipeline (GitHub Actions)
- ✅ Cross-platform build support (Linux→Windows via WSL2)

---

## Quick Start (5 minutes)

### Prerequisites
```powershell
# 1. Python 3.12+ (download from python.org)
python --version

# 2. Visual C++ Build Tools (required for cryptography)
# Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# 3. Git (optional, for cloning)
git --version
```

### Build Steps

**Option A: PowerShell (Recommended)**
```powershell
# 1. Clone repository
git clone https://github.com/POWDER-RANGER/red-team-osint-tool.git
cd red-team-osint-tool

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt
pip install -r build_requirements.txt

# 4. Build (automated)
.\build.ps1

# Result: vortex_0.1.0_windows.zip ready for distribution
```

**Option B: Command Prompt**
```batch
REM Same steps, then:
build.bat
```

### Verify Build
```powershell
# Extract and test
Expand-Archive vortex_0.1.0_windows.zip -DestinationPath test
.\test\vortex_dist\vortex.exe --help
```

---

## Detailed Setup

### Step 1: Install Python 3.12

**Method A: Official Installer**
1. Download from https://www.python.org/downloads/
2. Run installer
3. ☑ Add Python to PATH
4. Verify: `python --version` → Python 3.12.x

**Method B: Windows Package Manager**
```powershell
winget install Python.Python.3.12
```

**Method C: Chocolatey**
```powershell
choco install python312
```

### Step 2: Install Visual C++ Build Tools

**Required for:** cryptography, asyncpg, and other compiled modules

**Option 1: Visual Studio Community (includes build tools)**
1. Download: https://visualstudio.microsoft.com/downloads/
2. Select "Desktop development with C++"
3. Install
4. Verify: `cl.exe /version`

**Option 2: Standalone Build Tools**
1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Run installer
3. Select "Desktop development with C++"
4. Install

### Step 3: Clone Repository

```powershell
# Via Git
git clone https://github.com/POWDER-RANGER/red-team-osint-tool.git
cd red-team-osint-tool

# Or download ZIP from GitHub
# Extract and cd into directory
```

### Step 4: Create Virtual Environment

```powershell
# Create isolated Python environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then retry activation
```

### Step 5: Install Dependencies

```powershell
# Upgrade pip/setuptools first
python -m pip install --upgrade pip setuptools wheel

# Install runtime dependencies
pip install -r requirements.txt

# Install build dependencies
pip install -r build_requirements.txt
```

### Step 6: Run Build

```powershell
# Automated build (recommended)
.\build.ps1

# OR manual build
pyinstaller --onefile --name vortex pyinstaller_config.spec
```

---

## Build System Architecture

### Files Included

```
build_system/
├── pyinstaller_config.spec          # PyInstaller configuration
├── build_requirements.txt           # Build-only dependencies
├── build.ps1                        # PowerShell build script
├── build.bat                        # CMD build script
├── build.sh                         # Bash/Linux build script
├── windows-build.yml                # GitHub Actions CI/CD
├── WINDOWS_BUILD_GUIDE.md          # Detailed guide
└── BUILD_SYSTEM_README.md          # This file
```

### Build Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                    VORTEX Build Pipeline                     │
└─────────────────────────────────────────────────────────────┘
         ↓
[1] Validate Environment
    - Check Python 3.12+
    - Check pip
    - Verify C++ compiler
         ↓
[2] Install Dependencies
    - pip install -r requirements.txt
    - pip install -r build_requirements.txt
         ↓
[3] Clean Previous Builds
    - Remove ./dist directory
         ↓
[4] Prepare Assets
    - Create assets/ directory
    - Place icon (optional)
         ↓
[5] Run PyInstaller
    - Analyze dependencies
    - Collect hidden modules
    - Bundle resources
    - Compile to .EXE
         ↓
[6] Create Distribution
    - Copy .EXE to dist/vortex_dist/
    - Copy documentation
    - Generate MANIFEST.json
    - Create ZIP archive
         ↓
    RESULT: vortex_0.1.0_windows.zip
            dist/vortex_dist/vortex.exe
            build_TIMESTAMP.log
```

### Configuration Reference

**pyinstaller_config.spec** - Key sections:

```python
# Entry point (change if using different CLI)
a = Analysis(['src/vortex/cli/main.py'], ...)

# Data files to include in executable
datas=[
    ('config', 'config'),
    ('src/vortex/wordlists', 'wordlists'),
]

# Hidden imports (modules PyInstaller can't detect)
hiddenimports=[
    'vortex.collectors.dns',
    'vortex.processors.dedup',
    # Add as needed
]

# Executable configuration
exe = EXE(
    console=True,          # Console app (True) vs GUI (False)
    icon='assets/vortex.ico',
)
```

---

## Common Tasks

### Task: Add New Module to Build

If PyInstaller misses a module:

**Edit pyinstaller_config.spec:**
```python
hiddenimports=[
    'vortex.existing_module',
    'vortex.new_module',        # ← Add here
]
```

Then rebuild:
```powershell
.\build.ps1
```

### Task: Change Entry Point

If main CLI is in different location:

**Edit pyinstaller_config.spec:**
```python
a = Analysis(
    ['src/vortex/your_main.py'],  # ← Change path
    ...
)
```

Then rebuild.

### Task: Create GUI Executable

**Edit pyinstaller_config.spec:**
```python
exe = EXE(
    # ...
    console=False,  # ← Change to False
    icon='assets/vortex.ico',
)
```

Then rebuild.

### Task: Code Sign Executable (Production)

**Prerequisites:**
- Code signing certificate (.pfx file)
- Certificate password

**Step 1: Sign executable**
```powershell
$params = @{
    FilePath = "dist\vortex_dist\vortex.exe"
    CertificatePath = "C:\path\to\certificate.pfx"
    TimeStampServer = "http://timestamp.digicert.com"
}
Set-AuthenticodeSignature @params
```

**Step 2: Verify signature**
```powershell
Get-AuthenticodeSignature dist\vortex_dist\vortex.exe
# Should show: SignerCertificate: [Your Cert], Status: Valid
```

**Step 3: Recreate ZIP with signed executable**
```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory("dist\vortex_dist", "vortex_0.1.0_windows_signed.zip")
```

### Task: Troubleshoot Failed Build

1. **Check logs:**
```powershell
Get-Content build_*.log | Select-Object -Last 50
```

2. **Rebuild with verbose output:**
```powershell
.\build.ps1 -Verbose
```

3. **Run PyInstaller manually:**
```powershell
pyinstaller --clean --windowed --onefile pyinstaller_config.spec
```

4. **Check for missing modules:**
```powershell
# Edit pyinstaller_config.spec, add to hiddenimports:
hiddenimports=['your.missing.module']
```

---

## GitHub Actions Automation

### Automated Builds on Push

The CI/CD pipeline (**windows-build.yml**) automatically:
1. ✅ Builds .EXE on every push to `main` or `develop`
2. ✅ Runs code quality checks on pull requests
3. ✅ Creates GitHub Release artifacts on version tags
4. ✅ Generates checksums (SHA256)
5. ✅ Uploads build logs

### Enable in Your Repository

1. **Copy** `windows-build.yml` → `.github/workflows/`
2. **Commit** to GitHub
3. **Push** to trigger build

Monitor progress in **Actions** tab.

### Release Builds

Tag a commit to auto-create release:

```bash
git tag v0.2.0
git push origin v0.2.0
```

Artifacts automatically uploaded to **Releases** page.

---

## Distribution Guide

### For End Users

**Installation:**
1. Download: `vortex_0.1.0_windows.zip`
2. Extract to desired location
3. Double-click `vortex.exe` to run
4. Copy `config.example.yaml` → `~\.vortex\config.yaml`
5. Edit configuration as needed

**No additional software needed** - Python, libraries, everything is included.

### For System Administrators

**Enterprise Deployment:**

```powershell
# 1. Download and verify
$zip = "vortex_0.1.0_windows.zip"
$expected_sha = "abc123..."  # From checksums.sha256
$actual_sha = (Get-FileHash $zip -Algorithm SHA256).Hash

if ($actual_sha -ne $expected_sha) {
    Write-Error "Checksum mismatch!"
    exit 1
}

# 2. Extract to program files
Expand-Archive $zip "C:\Program Files\VORTEX"

# 3. Create shortcut
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Desktop\VORTEX.lnk")
$Shortcut.TargetPath = "C:\Program Files\VORTEX\vortex.exe"
$Shortcut.Save()

# 4. Grant permissions
icacls "C:\Program Files\VORTEX" /grant:r "$env:USERNAME:(OI)(CI)RX"

# 5. Distribute via GPO/SCCM/MDM
# Use your enterprise management tools
```

---

## File Specifications

### vortex.exe
- **Size:** ~50 MB
- **Format:** PE32+ (x64)
- **Dependencies:** None (all bundled)
- **Subsystem:** Console
- **Architecture:** x64 only
- **Min OS:** Windows 7 SP1+ (actually Windows 10+)

### vortex_0.1.0_windows.zip
- **Size:** ~40 MB (compressed)
- **Format:** ZIP deflate
- **Integrity:** SHA256 checksums included
- **Signing:** Optional (production)

### MANIFEST.json
```json
{
  "name": "vortex",
  "version": "0.1.0",
  "timestamp": "2026-01-03T16:18:00Z",
  "buildJob": "12345",
  "buildCommit": "abc123def456"
}
```

---

## Troubleshooting

### Issue: "Python not found"
```powershell
# Check PATH
$env:PATH -split ';' | Select-String python

# Or use full path
C:\Python312\python.exe --version
```

### Issue: "Visual C++ Build Tools required"
```powershell
# Install from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Then verify:
cl.exe /version
```

### Issue: "Module not found" (after build)
```powershell
# Add to hiddenimports in pyinstaller_config.spec
hiddenimports=[
    'missing.module.name',  # ← Add here
]

# Rebuild
.\build.ps1 -Clean
```

### Issue: Build takes >5 minutes
- Normal for first build (2-3 min)
- UPX compression may add time
- Edit pyinstaller_config.spec: `upx=False` to disable

### Issue: vortex.exe crashes on startup
```powershell
# Check event logs
Get-EventLog Application | Where-Object Source -eq vortex | Select-Object -Last 10

# Run with diagnostics
$env:VORTEX_DEBUG=1
.\vortex.exe
```

---

## Advanced Usage

### WSL2 Cross-Compilation (Linux→Windows)

```bash
# In WSL2 Ubuntu environment
wsl --install -d Ubuntu
wsl

# Install dependencies
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3-pip

# Clone and setup
git clone https://github.com/POWDER-RANGER/red-team-osint-tool.git
cd red-team-osint-tool
python3.12 -m venv venv
source venv/bin/activate

# Install
pip install -r requirements.txt
pip install -r build_requirements.txt

# Build
bash build.sh

# Transfer to Windows for testing
cp vortex_0.1.0_windows.zip /mnt/c/Users/YourUser/Downloads/
```

### Docker Build

```dockerfile
FROM python:3.12-windowsservercore

WORKDIR /build
COPY . .

RUN pip install -r build_requirements.txt && \
    pip install -r requirements.txt && \
    pyinstaller --onefile pyinstaller_config.spec

FROM mcr.microsoft.com/windows/servercore:ltsc2022
COPY --from=0 /build/dist/vortex_dist/vortex.exe /app/
ENTRYPOINT ["/app/vortex.exe"]
```

---

## Support & Resources

- **Repository:** https://github.com/POWDER-RANGER/red-team-osint-tool
- **Issues:** https://github.com/POWDER-RANGER/red-team-osint-tool/issues
- **PyInstaller Docs:** https://pyinstaller.readthedocs.io/
- **Python:** https://docs.python.org/3.12/

---

## License

VORTEX is licensed under the MIT License - see LICENSE file for details.

---

**Build Date:** January 3, 2026  
**Maintained by:** POWDER-RANGER  
**Last Updated:** 2026-01-03