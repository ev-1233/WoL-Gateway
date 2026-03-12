# Testing Cross-Platform Compatibility

This document explains how to test the setup script's cross-platform functionality.

## Test Modes

### 1. Platform Detection Test (`--test`)

Tests the OS and package manager detection logic for Windows, macOS, and Linux:

```bash
python3 setup_wol.py --test
```

**What it does:**
- Simulates different operating systems (Windows, macOS, Linux)
- Tests package manager detection (choco, scoop, winget, brew, port, apt, dnf, etc.)
- Shows what installation commands would be used for each platform
- **Recommended for verifying cross-platform compatibility**

**Example Output:**
```
Testing OS Detection Logic:
  ✓ OS: Windows    | Commands: ['choco']  | Detected: Windows, choco
  ✓ OS: Darwin     | Commands: ['brew']   | Detected: macOS, brew
  ✓ OS: Linux      | ...                  | Detected: Fedora, dnf

Testing Installation Commands:
  brew      : brew install wakeonlan
  choco     : choco install -y wakeonlan
  winget    : winget install --id wakeonlan -e --silent
```

### 2. Dry Run Mode (`--dry-run`)

Shows what commands would be executed during a real setup without actually running them:

```bash
python3 setup_wol.py --dry-run
```

**What it does:**
- Goes through the normal setup process
- Shows what commands would be executed
- Does not install packages or modify the system
- Useful for debugging and seeing the full setup flow

**Example Output:**
```
[DRY RUN] Would execute: /usr/bin/python3 -m pip install --user flask
[DRY RUN] Would execute: dnf install -y wakeonlan
```

## Supported Platforms

### Windows
- **Package Managers:**
  - Chocolatey (`choco`)
  - Scoop (`scoop`)
  - Winget (`winget`)
- **Admin Detection:** Uses `ctypes.windll.shell32.IsUserAnAdmin()`
- **Command Check:** Uses `where` instead of `which`

### macOS
- **Package Managers:**
  - Homebrew (`brew`) - Recommended
  - MacPorts (`port`)
- **Unix Commands:** Uses standard Unix tools

### Linux
- **Package Managers:**
  - apt (Debian/Ubuntu)
  - dnf (Fedora)
  - yum (RHEL/CentOS)
  - pacman (Arch)
  - zypper (openSUSE)
  - apk (Alpine)
  - pkg (Termux)

## Cross-Platform Features

### Command Existence Check
Uses `shutil.which()` for cross-platform compatibility with fallbacks:
- Windows: `where command`
- Unix: `which command`

### Admin/Root Detection
- **Linux/macOS:** `os.geteuid() != 0`
- **Windows:** `ctypes.windll.shell32.IsUserAnAdmin()`

### Package Installation
The script automatically:
1. Detects the OS and available package managers
2. Selects the appropriate installation commands
3. Handles sudo/admin privileges correctly per platform
4. Falls back to pip if system packages fail

## Testing Without Access to Other Platforms

Since you're on Linux, use the `--test` flag to verify the logic works for Windows and macOS:

```bash
python3 setup_wol.py --test
```

This comprehensively tests:
- ✓ Windows detection with all 3 package managers
- ✓ macOS detection with both package managers
- ✓ Correct installation commands for each platform
- ✓ Proper handling of systems without package managers

## What Was Fixed

1. **`os.geteuid()` errors on Windows** - Now checks with `hasattr()` first
2. **`which` command unavailable on Windows** - Uses `shutil.which()` or `where`
3. **No Windows package manager support** - Added choco, scoop, winget
4. **No macOS package manager support** - Added brew and port
5. **Admin detection on Windows** - Added proper Windows admin checking

## Validation

Run the test to verify all platforms are properly detected:
```bash
python3 setup_wol.py --test
```

All checks should show ✓ for successful detection.
