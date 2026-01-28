# Frequently Asked Questions (FAQ)

Common questions and answers about the AI-Powered Hand & Eye Controlled HCI.

---

## General Questions

### What is this application?
This is an accessibility tool that allows you to control your computer using hand gestures and eye movements, eliminating the need for a traditional mouse.

### Who is this for?
- People with motor disabilities
- Users who want hands-free computing
- Anyone interested in alternative input methods
- Researchers and developers in HCI

### What do I need to run it?
- Windows 10/11 (64-bit)
- A webcam (built-in or USB)
- Python 3.8+ (for source version)

### Is it free?
Yes! This is open-source software under the MIT License.

---

## Installation Questions

### How do I install it?
**Option 1 - Executable (Easiest):**
Download `HCI_Controller.exe` and double-click to run.

**Option 2 - From Source:**
```bash
git clone [repository-url]
cd AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python launcher.py
```

### Why do I get a "missing DLL" error?
This usually means Visual C++ Redistributable is not installed. Download it from Microsoft's website.

### The application won't start. What do I do?
1. Check if your webcam is connected
2. Make sure Python 3.8+ is installed
3. Try running from command line to see error messages
4. Check the `logs/hci.log` file for details

---

## Usage Questions

### How do I move the cursor?
Point your index finger (keep other fingers folded) and move your hand within the blue rectangle shown on screen.

### How do I click?
Pinch your thumb and index finger together.

### How do I right-click?
Open your palm (all 5 fingers extended) and hold for 1.5 seconds.

### How do I scroll?
Make a victory sign (✌️) and move your hand up/down.

### How do I drag and drop?
1. Pinch and hold for 0.5 seconds to start dragging
2. Move your hand to the destination
3. Release the pinch to drop

### How do I switch between modes?
Press keyboard keys:
- `h` - Hand-only mode
- `e` - Eye-only mode
- `b` - Hybrid mode

### How do I quit the application?
Press `q` or close the window.

---

## Performance Questions

### The cursor is too fast/slow
Adjust the **Sensitivity** slider in the Settings GUI, or edit `config/settings.json`.

### The cursor is jumpy/jittery
Increase the **Smoothing** setting.

### Clicks aren't registering
- Decrease the **Pinch Threshold** (makes detection easier)
- Increase the **Click Cooldown** (prevents accidental clicks)

### The app is running slowly
1. Close other applications
2. Disable "Show Landmarks" in settings
3. Ensure good lighting
4. Use hand-only mode (disable eye tracking)

### What FPS should I expect?
- **Good hardware**: 25-30 FPS
- **Average hardware**: 15-20 FPS
- **Minimum usable**: 10+ FPS

---

## Eye Tracking Questions

### Eye tracking isn't working
1. Ensure your face is visible to the camera
2. Check that lighting is even (avoid backlighting)
3. Sit 40-70cm from the webcam
4. Enable "Eye Tracking" in settings

### Is eye tracking accurate?
Eye tracking provides approximate gaze direction. It's best for:
- Coarse cursor movement
- Hands-free browsing
- Combined with hand gestures (hybrid mode)

### Does it work with glasses?
Yes, but accuracy may be slightly reduced.

### Does it track both eyes?
Yes, it tracks both eyes and averages them for better accuracy.

---

## Gesture Recognition Questions

### Why isn't my gesture recognized?
1. Keep your hand 30-60cm from the camera
2. Stay within the blue rectangle (ROI)
3. Ensure good lighting on your hand
4. Move slowly and deliberately
5. Use a plain background

### Can I add custom gestures?
Currently, the app supports 7 predefined gestures. Custom gestures would require modifying the source code.

### Why do I get accidental clicks?
Increase the **Click Cooldown** and **Pinch Threshold** in settings.

---

## Technical Questions

### What technologies does this use?
- **MediaPipe** - Hand and face detection
- **OpenCV** - Video processing
- **PyAutoGUI** - Mouse control
- **CustomTkinter** - Settings GUI

### Can I use this on macOS/Linux?
The code is primarily designed for Windows. macOS/Linux support may require modifications, especially for PyAutoGUI.

### Is my video recorded or stored?
No. Video is processed in real-time and never saved or transmitted.

### Can this work with multiple monitors?
Yes, the cursor can move across all connected monitors.

### What's the "fail-safe" error?
PyAutoGUI has a safety feature that stops when the cursor reaches a screen corner. Our app handles this automatically.

---

## Troubleshooting

### "Camera not found" error
1. Check webcam connection
2. Close other apps using the camera
3. Restart your computer
4. Try a different USB port

### "MediaPipe has no attribute 'solutions'" error
Install the correct MediaPipe version:
```bash
pip install mediapipe==0.10.9
```

### Windows Defender blocks the executable
1. Click "More info"
2. Click "Run anyway"
3. Or add an exclusion in Windows Security

### High CPU usage
- Reduce webcam resolution
- Disable eye tracking
- Use hand-only mode
- Close unnecessary applications

---

## Feature Requests

### Will there be voice control?
It's on the roadmap for future versions.

### Will there be mobile support?
Currently, this is a desktop application only.

### Can I control specific applications?
The app controls the system cursor, which works with all applications.

---

## Getting Help

### Where can I report bugs?
Open an issue on GitHub with:
- Description of the problem
- Steps to reproduce
- System information
- Error messages/logs

### Where can I suggest features?
Open a feature request issue on GitHub.

### Is there a community?
Check the GitHub repository for discussions and updates.
