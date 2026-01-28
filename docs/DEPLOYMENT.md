# Deployment Guide - HCI Controller

## Quick Deployment (Recommended)

### Option 1: Create Standalone Executable

1. **Double-click `build.bat`** or run in terminal:
   ```bash
   build.bat
   ```

2. Wait for build to complete (2-5 minutes)

3. Find executable at: `dist\HCI_Controller.exe`

4. **Run the app**: Double-click `HCI_Controller.exe`

---

## Manual Build Steps

If the batch script doesn't work, follow these steps:

### Step 1: Install PyInstaller
```bash
venv\Scripts\activate
pip install pyinstaller
```

### Step 2: Build Executable
```bash
pyinstaller --clean HCI_Controller.spec
```

### Step 3: Run
```bash
dist\HCI_Controller.exe
```

---

## Deploying to Another Computer

### What to Copy
Copy the entire `dist` folder containing:
- `HCI_Controller.exe`

### Requirements on Target Computer
- **Windows 10/11** (64-bit)
- **Webcam** (built-in or USB)
- **No Python required** - everything is bundled!

### First Run on New Computer
1. Windows may show "Windows protected your PC" warning
2. Click **"More info"** → **"Run anyway"**
3. Allow webcam access when prompted

---

## Running from Source (Development)

If you prefer running from Python source:

```bash
# 1. Create virtual environment (first time only)
python -m venv venv

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python launcher.py
```

---

## Shortcuts

| File | Purpose |
|------|---------|
| `run.bat` | Quick launch (auto-detects exe or Python) |
| `build.bat` | Create standalone executable |
| `launcher.py` | Main Python entry point |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Build fails with "mediapipe" error | Run: `pip install mediapipe==0.10.9` |
| Executable is very large | Normal (~300-500MB) due to bundled libraries |
| Antivirus blocks exe | Add to exclusions or use source version |
| Camera not detected | Check webcam connection, try different USB port |
| App crashes on start | Run from command line to see error messages |

### View Error Messages
```bash
# Run with console output for debugging
dist\HCI_Controller.exe --debug
```

Or modify `HCI_Controller.spec` line 56: `console=True`

---

## File Structure After Build

```
AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface/
├── dist/
│   └── HCI_Controller.exe    ← Standalone executable
├── build/                     ← Temporary build files (can delete)
├── venv/                      ← Python environment
├── src/                       ← Source code
├── gui/                       ← GUI code
├── config/                    ← Settings
├── docs/                      ← Documentation
├── build.bat                  ← Build script
├── run.bat                    ← Quick run script
└── requirements.txt           ← Python dependencies
```
