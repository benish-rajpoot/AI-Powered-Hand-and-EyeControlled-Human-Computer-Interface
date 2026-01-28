# User Guide - Hand & Eye Controlled HCI

## Quick Start

```bash
# Activate virtual environment
venv\Scripts\activate

# Launch with Settings GUI
python launcher.py

# Launch without GUI
python launcher.py --no-gui
```

---

## Hand Gestures

| Gesture | How To Do It | Action |
|---------|--------------|--------|
| **Point** | Extend only index finger, keep others folded | Move cursor |
| **Pinch** | Touch thumb tip to index finger tip | Left click |
| **Double Pinch** | Pinch twice quickly (within 0.4 seconds) | Double click |
| **Hold Pinch** | Hold pinch for 0.5 seconds | Start drag |
| **Release Pinch** | Stop pinching while dragging | Drop (end drag) |
| **Open Palm** | Extend all 5 fingers, hold for 1.5 seconds | Right click |
| **Victory Sign** | Extend index + middle fingers (✌️) | Scroll mode |

---

## Scroll Mode (Victory Sign)

1. Make the victory sign (✌️)
2. Move hand UP → Scroll UP
3. Move hand DOWN → Scroll DOWN
4. Change gesture to exit scroll mode

---

## Eye Gaze Controls

Eye tracking uses your webcam to detect where you're looking on the screen.

| Action | How To Do It | Result |
|--------|--------------|--------|
| **Move Cursor** | Look at different areas of the screen | Cursor follows your gaze |
| **Blink Detection** | Close both eyes briefly, then open | Left click |

### How Eye Tracking Works

1. **Face Detection**: Camera detects your face using 468 landmarks
2. **Iris Tracking**: Detects iris center in both eyes (10 iris landmarks)
3. **Gaze Estimation**: Maps iris position to screen coordinates
4. **Smoothing**: Applies smoothing to reduce jitter

### Eye Tracking Tips

- **Face Position**: Keep your face centered in the camera view
- **Distance**: Sit 40-70cm from your webcam
- **Lighting**: Ensure even lighting on your face (avoid backlighting)
- **Glasses**: Works with glasses, but may reduce accuracy
- **Calibration**: Look at screen center when starting for best results

### Eye Mode vs Hybrid Mode

| Mode | Behavior |
|------|----------|
| **Eye-only** (`e` key) | Cursor always follows your gaze |
| **Hybrid** (`b` key) | Gaze controls cursor when hand not detected; hand takes over when visible |

---

## Keyboard Controls

| Key | Action |
|-----|--------|
| `h` | Switch to **Hand-only** mode |
| `e` | Switch to **Eye-only** mode |
| `b` | Switch to **Hybrid** mode (both) |
| `q` | Quit application |

---

## Control Modes

| Mode | Description |
|------|-------------|
| **Hand** | Cursor follows hand gestures only |
| **Eye** | Cursor follows your eye gaze |
| **Hybrid** | Eye for coarse movement, hand for fine control |

---

## Settings GUI Options

| Setting | Range | Description |
|---------|-------|-------------|
| Sensitivity | 0.5 - 3.0 | How fast cursor moves |
| Smoothing | 0% - 90% | Reduces cursor jitter |
| Pinch Threshold | 20 - 80px | Distance for pinch detection |
| Click Cooldown | 0.1 - 1.0s | Delay between clicks |
| Scroll Speed | 1 - 15 | How fast scrolling works |

---

## Tips for Best Performance

1. **Lighting**: Use good, even lighting on your face and hands
2. **Background**: Plain background works better than cluttered
3. **Distance**: Keep hand 30-60cm from camera
4. **Active Zone**: Keep hand inside the blue rectangle on screen
5. **Smooth movements**: Avoid jerky hand movements

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Cursor jumps around | Increase smoothing in settings |
| Clicks not registering | Decrease pinch threshold |
| Too many accidental clicks | Increase click cooldown |
| Cursor moves too slow | Increase sensitivity |
| Eye tracking not working | Ensure face is visible, check lighting |

---

## Command Line Options

```bash
python launcher.py              # Full launch with settings GUI
python launcher.py --no-gui     # Skip settings, start directly
python launcher.py --settings-only  # Open settings only
python launcher.py --legacy     # Use old main.py instead of app.py
```
