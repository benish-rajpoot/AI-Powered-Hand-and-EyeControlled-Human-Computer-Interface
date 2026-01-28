<<<<<<< HEAD
# 🖐️ AI-Powered Hand & Eye Controlled Human-Computer Interface

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-orange.svg)](https://mediapipe.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A revolutionary accessibility tool that allows users to control their computer using **hand gestures** and **eye gaze**, eliminating the need for traditional input devices like mouse and keyboard.

![Demo Preview](docs/demo.gif)

---

## 📑 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Hand Gestures](#-hand-gestures)
- [Eye Tracking](#-eye-tracking)
- [Control Modes](#-control-modes)
- [Settings GUI](#%EF%B8%8F-settings-gui)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [Configuration](#%EF%B8%8F-configuration)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Technical Architecture](#-technical-architecture)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Team](#-team)
- [License](#-license)

---

## ✨ Features

### Core Capabilities
| Feature | Description |
|---------|-------------|
| 🖐️ **Hand Tracking** | Real-time 21-landmark hand detection using MediaPipe |
| 👁️ **Eye Gaze Estimation** | 468-point face mesh with iris tracking |
| 🎯 **Gesture Recognition** | 7 distinct gestures for mouse control |
| 🖱️ **Full Mouse Control** | Move, click, double-click, right-click, drag, scroll |
| 🔄 **Hybrid Mode** | Seamlessly combine hand and eye tracking |
| ⚙️ **Settings GUI** | Modern dark-themed configuration interface |
| 📊 **Performance Monitoring** | Real-time FPS display and logging |

### Gesture Support
- ✅ Cursor movement (point gesture)
- ✅ Left click (pinch)
- ✅ Double click (double pinch)
- ✅ Right click (open palm hold)
- ✅ Drag and drop (pinch hold)
- ✅ Scroll (victory sign + movement)

### Technical Highlights
- 🎬 30+ FPS real-time processing
- 🔧 Adjustable sensitivity and smoothing
- 📁 Persistent settings via JSON config
- 🖥️ Multi-monitor support
- 🛡️ Fail-safe cursor protection
- 📝 Comprehensive logging system

---

## 🎬 Demo

### Hand Gesture Control
| Gesture | Action | Visual |
|---------|--------|--------|
| Point | Move cursor | ☝️ |
| Pinch | Left click | 🤏 |
| Open Palm | Right click | ✋ |
| Victory | Scroll mode | ✌️ |

### Control Modes
| Mode | Description |
|------|-------------|
| **Hand Only** | Cursor controlled entirely by hand gestures |
| **Eye Only** | Cursor follows your eye gaze direction |
| **Hybrid** | Eye for coarse movement, hand for precision |

---

## 🚀 Quick Start

### Option 1: Run Executable (Easiest)
```bash
# Double-click the executable
dist\HCI_Controller.exe
```

### Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/FAbdullah17/AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface.git
cd AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python launcher.py
```

---

## 📦 Installation

### Prerequisites
- **Python**: 3.8 or higher
- **Operating System**: Windows 10/11 (64-bit)
- **Hardware**: Webcam (built-in or USB)
- **RAM**: Minimum 4GB (8GB recommended)

### Step-by-Step Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/FAbdullah17/AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface.git
cd AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface
```

#### 2. Create Virtual Environment
```bash
python -m venv venv
```

#### 3. Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Verify Installation
```bash
python -c "import cv2; import mediapipe; import pyautogui; print('All dependencies installed!')"
```

### Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| opencv-python | ≥4.8.0 | Video capture and image processing |
| mediapipe | 0.10.9 | Hand and face landmark detection |
| pyautogui | ≥0.9.54 | Mouse and keyboard control |
| numpy | ≥1.24.0 | Numerical computations |
| customtkinter | ≥5.2.0 | Modern GUI framework |
| Pillow | ≥10.0.0 | Image handling |
| pytest | ≥7.0.0 | Unit testing |

---

## 🎮 Usage

### Launch Options

| Command | Description |
|---------|-------------|
| `python launcher.py` | Open settings GUI, then start app |
| `python launcher.py --no-gui` | Start directly without settings GUI |
| `python launcher.py --settings-only` | Open settings GUI only |
| `python launcher.py --legacy` | Use legacy main.py |

### Quick Run Scripts
| Script | Purpose |
|--------|---------|
| `run.bat` | Auto-detect and launch (exe or Python) |
| `build.bat` | Create standalone executable |

---

## 🖐️ Hand Gestures

### Complete Gesture Reference

| Gesture | How To Perform | Action | Hold Time |
|---------|----------------|--------|-----------|
| **Point** | Extend index finger only, fold others | Move cursor | Continuous |
| **Pinch** | Touch thumb tip to index finger tip | Left click | Instant |
| **Double Pinch** | Pinch twice quickly | Double click | <0.4s between |
| **Hold Pinch** | Maintain pinch gesture | Start drag | 0.5s |
| **Release Pinch** | Stop pinching while dragging | Drop/End drag | Instant |
| **Open Palm** | Extend all 5 fingers | Right click | 1.5s |
| **Victory** | Extend index + middle fingers (✌️) | Enter scroll mode | Continuous |

### Scroll Mode Operation
1. Make the **victory sign** (✌️) to enter scroll mode
2. Move hand **UP** → Page scrolls **UP**
3. Move hand **DOWN** → Page scrolls **DOWN**
4. Change to any other gesture to exit scroll mode

### Gesture Tips
- Keep hand **30-60cm** from camera
- Stay within the **blue ROI rectangle** shown on screen
- Use **smooth, deliberate movements**
- Ensure good lighting on your hand
- Plain background works best

---

## 👁️ Eye Tracking

### How It Works
1. **Face Detection**: MediaPipe Face Mesh detects 468 facial landmarks
2. **Iris Tracking**: 10 specialized iris landmarks locate eye centers
3. **Gaze Estimation**: Iris position relative to eye corners determines gaze direction
4. **Screen Mapping**: Gaze direction is mapped to screen coordinates
5. **Smoothing**: Algorithm reduces jitter for stable cursor movement

### Eye Tracking Tips
| Tip | Description |
|-----|-------------|
| **Face Position** | Keep face centered in camera view |
| **Distance** | Sit 40-70cm from your webcam |
| **Lighting** | Even lighting on face, avoid backlighting |
| **Glasses** | Works with glasses, may reduce accuracy |
| **Calibration** | Look at screen center when starting |

### Eye Gaze Controls
| Action | How To | Result |
|--------|--------|--------|
| Move Cursor | Look at different screen areas | Cursor follows gaze |
| Blink Detection | Close both eyes briefly | (Reserved for future) |

---

## 🔄 Control Modes

### Mode Comparison

| Feature | Hand Mode | Eye Mode | Hybrid Mode |
|---------|-----------|----------|-------------|
| Cursor control | Hand gestures | Eye gaze | Both |
| Click actions | ✅ Full support | ❌ Eye only moves | ✅ Full support |
| Precision | High | Medium | High |
| Fatigue | Low (short sessions) | Medium | Low |
| Best for | Precise clicking | Hands-free browsing | General use |

### Mode Switching
- Press `h` → Hand-only mode
- Press `e` → Eye-only mode  
- Press `b` → Hybrid mode (default)

### Hybrid Mode Behavior
1. When **hand is visible**: Hand controls cursor with full gesture support
2. When **hand is hidden**: Eye gaze takes over cursor movement
3. **Seamless transition**: Switch between hand and eye automatically

---

## ⚙️ Settings GUI

### Accessing Settings
```bash
python launcher.py          # Opens GUI before app
python launcher.py --settings-only  # GUI only
```

### Available Settings

#### Cursor Settings
| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| Sensitivity | 0.5 - 3.0 | 1.0 | Cursor movement speed multiplier |
| Smoothing | 0% - 90% | 70% | Reduces cursor jitter (higher = smoother) |

#### Gesture Settings
| Setting | Range | Default | Description |
|---------|-------|---------|-------------|
| Pinch Threshold | 20 - 80px | 45px | Max distance for pinch detection |
| Click Cooldown | 0.1 - 1.0s | 0.5s | Minimum time between clicks |
| Scroll Speed | 1 - 15 | 3 | Scroll sensitivity |

#### Display Options
| Option | Default | Description |
|--------|---------|-------------|
| Show FPS | ✅ On | Display frames per second |
| Show Landmarks | ✅ On | Show hand tracking points |
| Enable Eye Tracking | ✅ On | Enable eye gaze features |

#### Control Mode
- **Hand Only**: Pure hand gesture control
- **Eye Only**: Pure eye gaze control
- **Hybrid**: Combined hand + eye control

---

## ⌨️ Keyboard Shortcuts

### Runtime Controls
| Key | Action |
|-----|--------|
| `h` | Switch to Hand-only mode |
| `e` | Switch to Eye-only mode |
| `b` | Switch to Hybrid mode |
| `q` | Quit application |

---

## 🛠️ Configuration

### Config File Location
```
config/settings.json
```

### Default Configuration
```json
{
  "cursor_sensitivity": 1.0,
  "cursor_smoothing": 0.7,
  "pinch_threshold": 45,
  "click_cooldown": 0.5,
  "scroll_speed": 3,
  "enable_eye_tracking": true,
  "enable_hand_tracking": true,
  "show_landmarks": true,
  "show_fps": true,
  "control_mode": "hand"
}
```

### Configuration Options Explained

| Key | Type | Description |
|-----|------|-------------|
| `cursor_sensitivity` | float | Movement speed (0.5-3.0) |
| `cursor_smoothing` | float | Smoothing factor (0.0-0.9) |
| `pinch_threshold` | int | Pinch detection distance in pixels |
| `click_cooldown` | float | Seconds between allowed clicks |
| `scroll_speed` | int | Scroll multiplier |
| `enable_eye_tracking` | bool | Enable/disable eye tracking |
| `enable_hand_tracking` | bool | Enable/disable hand tracking |
| `show_landmarks` | bool | Display tracking points |
| `show_fps` | bool | Show FPS counter |
| `control_mode` | string | "hand", "eye", or "hybrid" |

---

## 📦 Deployment

### Creating Standalone Executable

#### Method 1: Build Script (Recommended)
```bash
# Double-click or run:
build.bat
```

#### Method 2: Manual Build
```bash
venv\Scripts\activate
pip install pyinstaller
pyinstaller --clean HCI_Controller.spec
```

#### Output
```
dist/HCI_Controller.exe   # Standalone executable (~300-500MB)
```

### Deploying to Another Computer

1. **Copy** `dist\HCI_Controller.exe` to target computer
2. **Run** by double-clicking the executable
3. **First run**: Click "More info" → "Run anyway" (Windows SmartScreen)

### Target System Requirements
- Windows 10/11 (64-bit)
- Webcam
- No Python required!

---

## 📁 Project Structure

```
AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface/
│
├── 📂 src/                          # Core application modules
│   ├── __init__.py                  # Package initialization
│   ├── app.py                       # Main application class
│   ├── main.py                      # Legacy entry point
│   ├── hand_tracker.py              # MediaPipe hand tracking
│   ├── eye_tracker.py               # MediaPipe eye/gaze tracking
│   ├── gesture_recognizer.py        # Gesture detection logic
│   ├── mouse_controller.py          # PyAutoGUI mouse control
│   ├── calibration.py               # Settings management
│   └── logger.py                    # Logging utilities
│
├── 📂 gui/                          # GUI components
│   ├── __init__.py                  # Package initialization
│   └── settings_gui.py              # CustomTkinter settings window
│
├── 📂 config/                       # Configuration files
│   └── settings.json                # User settings
│
├── 📂 docs/                         # Documentation
│   ├── USER_GUIDE.md                # User manual
│   └── DEPLOYMENT.md                # Deployment guide
│
├── 📂 tests/                        # Unit tests
│   ├── __init__.py                  # Package initialization
│   └── test_gestures.py             # Gesture recognition tests
│
├── 📂 logs/                         # Application logs
│   └── hci.log                      # Runtime log file
│
├── 📂 dist/                         # Built executable (after build)
│   └── HCI_Controller.exe           # Standalone application
│
├── 📄 launcher.py                   # Main entry point
├── 📄 requirements.txt              # Python dependencies
├── 📄 HCI_Controller.spec           # PyInstaller configuration
├── 📄 build.bat                     # Build script
├── 📄 run.bat                       # Quick run script
├── 📄 README.md                     # This file
├── 📄 LICENSE                       # MIT License
└── 📄 .gitignore                    # Git ignore rules
```

---

## 🏗️ Technical Architecture

### System Overview
```
┌─────────────────────────────────────────────────────────────┐
│                     HCI Application                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Webcam    │→ │  OpenCV     │→ │  Frame Processing   │  │
│  │   Input     │  │  Capture    │  │  (flip, resize)     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                                              │               │
│                         ┌────────────────────┴───────────┐  │
│                         ↓                                ↓  │
│              ┌─────────────────┐          ┌─────────────────┐│
│              │  Hand Tracker   │          │  Eye Tracker    ││
│              │  (MediaPipe     │          │  (MediaPipe     ││
│              │   Hands)        │          │   Face Mesh)    ││
│              └────────┬────────┘          └────────┬────────┘│
│                       ↓                            ↓         │
│              ┌─────────────────┐          ┌─────────────────┐│
│              │    Gesture      │          │  Gaze Point     ││
│              │   Recognizer    │          │  Estimation     ││
│              └────────┬────────┘          └────────┬────────┘│
│                       └────────────┬───────────────┘         │
│                                    ↓                         │
│                       ┌─────────────────────┐                │
│                       │   Mode Controller   │                │
│                       │ (hand/eye/hybrid)   │                │
│                       └──────────┬──────────┘                │
│                                  ↓                           │
│                       ┌─────────────────────┐                │
│                       │  Mouse Controller   │                │
│                       │    (PyAutoGUI)      │                │
│                       └──────────┬──────────┘                │
│                                  ↓                           │
│                       ┌─────────────────────┐                │
│                       │   System Cursor     │                │
│                       └─────────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

### Class Diagram
```
┌─────────────────────┐
│   HCIApplication    │
├─────────────────────┤
│ - hand_tracker      │
│ - eye_tracker       │
│ - gesture_recognizer│
│ - mouse_controller  │
│ - config            │
│ - logger            │
├─────────────────────┤
│ + run()             │
│ + set_mode()        │
│ + cleanup()         │
└─────────────────────┘
         │
         │ uses
         ↓
┌─────────────────┐  ┌─────────────────┐  ┌──────────────────┐
│  HandTracker    │  │   EyeTracker    │  │ GestureRecognizer│
├─────────────────┤  ├─────────────────┤  ├──────────────────┤
│ + process_frame │  │ + process_frame │  │ + recognize()    │
│ + get_landmarks │  │ + get_gaze_point│  │ + should_click() │
└─────────────────┘  └─────────────────┘  └──────────────────┘
```

### Data Flow
1. **Input**: Webcam captures video frames at 30 FPS
2. **Processing**: MediaPipe extracts hand/face landmarks
3. **Recognition**: Gestures are classified from landmark positions
4. **Mapping**: Hand/eye positions are mapped to screen coordinates
5. **Smoothing**: Position history creates smooth cursor movement
6. **Output**: PyAutoGUI moves the system cursor

---

## 📚 API Reference

### HandTracker Class
```python
from hand_tracker import HandTracker

tracker = HandTracker(
    max_hands=1,
    detection_confidence=0.7,
    tracking_confidence=0.7
)

# Process a frame
processed_frame = tracker.process_frame(frame)

# Get landmarks
landmarks = tracker.get_all_landmarks(frame.shape)

# Get index finger position
index_pos = tracker.get_index_finger_tip(frame.shape)

# Check if hand detected
if tracker.hand_detected:
    # Handle hand tracking
    pass

# Cleanup
tracker.release()
```

### EyeTracker Class
```python
from eye_tracker import EyeTracker

tracker = EyeTracker(
    detection_confidence=0.7,
    tracking_confidence=0.7
)

# Process frame
processed_frame = tracker.process_frame(frame)

# Get gaze point
gaze_x, gaze_y = tracker.get_gaze_point(screen_width, screen_height)

# Check blink
ear = tracker.get_eye_aspect_ratio()

# Cleanup
tracker.release()
```

### GestureRecognizer Class
```python
from gesture_recognizer import GestureRecognizer, Gesture

recognizer = GestureRecognizer(
    pinch_threshold=45,
    click_cooldown=0.5
)

# Recognize gesture
gesture = recognizer.recognize(landmarks)

# Check gesture type
if gesture == Gesture.PINCH:
    if recognizer.should_click(gesture):
        # Perform click
        pass

# Check for drag
if recognizer.should_start_drag(gesture):
    # Start drag
    pass
```

### MouseController Class
```python
from mouse_controller import MouseController

controller = MouseController(
    sensitivity=1.0,
    smoothing=0.7
)

# Move cursor
controller.move_cursor(x, y, frame_width, frame_height)

# Click actions
controller.left_click()
controller.right_click()
controller.double_click()

# Drag operations
controller.drag_start()
controller.drag_end()

# Scroll
controller.scroll(amount)  # positive=up, negative=down
```

---

## 🔧 Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Cursor jumps around | Low smoothing | Increase smoothing in settings |
| Clicks not registering | Threshold too low | Decrease pinch threshold |
| Too many accidental clicks | Cooldown too short | Increase click cooldown |
| Cursor too fast | Sensitivity too high | Decrease sensitivity |
| Eye tracking inaccurate | Poor lighting | Improve face lighting |
| Camera not found | Driver issue | Reinstall webcam drivers |
| Build fails | Missing deps | Run `pip install -r requirements.txt` |
| Fail-safe error | Cursor at corner | Already fixed in latest version |

### Performance Optimization
1. **Reduce resolution**: Lower webcam resolution for better FPS
2. **Disable landmarks**: Turn off "Show Landmarks" in settings
3. **Use hand-only mode**: Disable eye tracking if not needed
4. **Close other apps**: Free up CPU/GPU resources

### Getting Help
1. Check `logs/hci.log` for error details
2. Run with console output for debugging:
   ```bash
   python launcher.py
   ```
3. Open an issue on GitHub with:
   - Error message
   - System specs
   - Steps to reproduce

---

## 🤝 Contributing

### How to Contribute
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface.git

# Install dev dependencies
pip install -r requirements.txt
pip install pytest

# Run tests
pytest tests/ -v
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions
- Add unit tests for new features

---

## 👥 Team

| Name | Roll Number | Role |
|------|-------------|------|
| **Sundas Safder** | 079884 | Developer |
| **Benish Batool** | 079888 | Developer |
| **Pakiza Imran** | 079889 | Developer |

### Supervisor
**Sir Marsad Akbar**

### Institution
**University of Punjab**  
Faculty of Computing & Information Technology

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 AI-Powered HCI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

- [MediaPipe](https://mediapipe.dev/) - Hand and face tracking
- [OpenCV](https://opencv.org/) - Computer vision
- [PyAutoGUI](https://pyautogui.readthedocs.io/) - Mouse control
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern GUI

---

<div align="center">

**⭐ Star this repository if you find it helpful! ⭐**

Made with ❤️ by the HCI Team

</div>
=======
# AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface
>>>>>>> 6ec2eac4504ad119563fe233ba0759e66282119d
