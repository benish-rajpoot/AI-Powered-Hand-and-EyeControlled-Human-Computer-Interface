# Installation Guide

Step-by-step installation instructions for all platforms and methods.

---

## Table of Contents
- [Quick Install (Windows Executable)](#quick-install-windows-executable)
- [Python Installation (From Source)](#python-installation-from-source)
- [Development Setup](#development-setup)
- [Troubleshooting Installation](#troubleshooting-installation)

---

## Quick Install (Windows Executable)

The easiest way to use the application - no Python required!

### Step 1: Download
Download `HCI_Controller.exe` from the releases page or `dist` folder.

### Step 2: Run
Double-click `HCI_Controller.exe` to start.

### Step 3: First-Time Setup
1. Windows may show "Windows protected your PC"
2. Click **"More info"**
3. Click **"Run anyway"**
4. Allow camera access when prompted

**That's it!** The app is ready to use.

---

## Python Installation (From Source)

### Prerequisites

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Python | 3.8+ | `python --version` |
| pip | Latest | `pip --version` |
| Git | Any | `git --version` |
| Webcam | Any | Connected and working |

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

Verify installation:
```bash
python --version
# Should show: Python 3.8.x or higher
```

### Step 2: Clone Repository

```bash
git clone https://github.com/FAbdullah17/AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface.git
cd AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface
```

Or download and extract the ZIP file.

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- opencv-python (video capture)
- mediapipe (hand/face tracking)
- pyautogui (mouse control)
- numpy (numerical operations)
- customtkinter (GUI)
- Pillow (image handling)

### Step 5: Verify Installation

```bash
python -c "import cv2; import mediapipe; import pyautogui; print('✅ All dependencies installed!')"
```

### Step 6: Run the Application

```bash
python launcher.py
```

---

## Development Setup

For contributors and developers.

### Step 1: Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface.git
cd AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface
```

### Step 2: Create Development Environment

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install pytest  # For testing
```

### Step 3: Verify Tests Pass

```bash
pytest tests/ -v
```

### Step 4: Create a Branch

```bash
git checkout -b feature/your-feature-name
```

---

## Dependency Details

### Core Dependencies

| Package | Version | Purpose | Size |
|---------|---------|---------|------|
| opencv-python | ≥4.8.0 | Video capture, image processing | ~50MB |
| mediapipe | 0.10.9 | Hand and face landmark detection | ~30MB |
| pyautogui | ≥0.9.54 | Mouse and keyboard control | ~1MB |
| numpy | ≥1.24.0 | Numerical computations | ~20MB |
| customtkinter | ≥5.2.0 | Modern GUI framework | ~5MB |
| Pillow | ≥10.0.0 | Image handling | ~5MB |

### Optional Dependencies

| Package | Purpose |
|---------|---------|
| pytest | Unit testing |
| pyinstaller | Creating executable |

### MediaPipe Version Note

⚠️ **Important**: Use MediaPipe version **0.10.9** specifically.

Newer versions (0.10.10+) removed the `solutions` API that this application uses.

```bash
# If you have a different version:
pip uninstall mediapipe
pip install mediapipe==0.10.9
```

---

## Troubleshooting Installation

### "Python not found"

**Windows**:
1. Reinstall Python with "Add to PATH" checked
2. Or add manually: Settings → System → Advanced → Environment Variables

**Verify**:
```bash
python --version
```

### "pip not found"

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### "No module named 'cv2'"

```bash
pip install opencv-python
```

### "MediaPipe has no attribute 'solutions'"

Wrong MediaPipe version. Fix:
```bash
pip uninstall mediapipe
pip install mediapipe==0.10.9
```

### "No module named 'customtkinter'"

```bash
pip install customtkinter
```

### "Camera not found"

1. Check webcam connection
2. Close other apps using camera
3. Try different USB port
4. Update webcam drivers

### "Permission denied" errors

**Windows**: Run terminal as Administrator
**macOS/Linux**: Use `sudo` or fix permissions

### Build fails with PyInstaller

```bash
pip install --upgrade pyinstaller
pyinstaller --clean HCI_Controller.spec
```

### General troubleshooting

1. Delete `venv` folder and recreate
2. Update pip: `pip install --upgrade pip`
3. Check Python version: must be 3.8+
4. Check logs: `logs/hci.log`

---

## Uninstallation

### Executable Version
Simply delete `HCI_Controller.exe`

### Source Version
```bash
# Deactivate virtual environment
deactivate

# Delete the project folder
cd ..
rmdir /s AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface
```

---

## System Requirements

### Minimum
- **OS**: Windows 10 (64-bit)
- **CPU**: Intel i3 or equivalent
- **RAM**: 4GB
- **Webcam**: 720p, 30 FPS

### Recommended
- **OS**: Windows 11 (64-bit)
- **CPU**: Intel i5 or better
- **RAM**: 8GB+
- **Webcam**: 1080p, 30+ FPS
- **GPU**: Any (for better performance)

---

## Next Steps

After installation:
1. Read the [User Guide](USER_GUIDE.md)
2. Explore [Settings](../config/settings.json)
3. Check [FAQ](FAQ.md) for common questions
