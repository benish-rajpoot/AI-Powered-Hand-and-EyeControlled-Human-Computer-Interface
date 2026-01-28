# Technical Documentation

## Architecture Overview

This document provides in-depth technical details about the AI-Powered Hand & Eye Controlled Human-Computer Interface.

---

## System Components

### 1. Hand Tracking Module (`hand_tracker.py`)

#### MediaPipe Hands Configuration
```python
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,      # Video stream mode
    max_num_hands=1,              # Track single hand
    min_detection_confidence=0.7, # Detection threshold
    min_tracking_confidence=0.7   # Tracking threshold
)
```

#### 21 Hand Landmarks
| Index | Landmark | Description |
|-------|----------|-------------|
| 0 | WRIST | Base of palm |
| 1-4 | THUMB | CMC, MCP, IP, TIP |
| 5-8 | INDEX | MCP, PIP, DIP, TIP |
| 9-12 | MIDDLE | MCP, PIP, DIP, TIP |
| 13-16 | RING | MCP, PIP, DIP, TIP |
| 17-20 | PINKY | MCP, PIP, DIP, TIP |

#### Key Methods
- `process_frame(frame)` - Process BGR frame, return annotated frame
- `get_all_landmarks(shape)` - Get all 21 landmarks as (x, y) tuples
- `get_index_finger_tip(shape)` - Get index fingertip position
- `hand_detected` - Property indicating if hand is visible

---

### 2. Eye Tracking Module (`eye_tracker.py`)

#### MediaPipe Face Mesh Configuration
```python
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,         # Enable iris landmarks
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
```

#### Iris Landmark Indices
| Eye | Center | Left | Right | Top | Bottom |
|-----|--------|------|-------|-----|--------|
| Left | 468 | 469 | 470 | 471 | 472 |
| Right | 473 | 474 | 475 | 476 | 477 |

#### Gaze Estimation Algorithm
```python
def get_gaze_point(self, screen_width, screen_height):
    # Get iris centers
    left_iris = self._get_iris_center(LEFT_IRIS_INDICES)
    right_iris = self._get_iris_center(RIGHT_IRIS_INDICES)
    
    # Average both eyes
    gaze_x = (left_iris.x + right_iris.x) / 2
    gaze_y = (left_iris.y + right_iris.y) / 2
    
    # Map to screen with smoothing
    screen_x = int(gaze_x * screen_width * sensitivity)
    screen_y = int(gaze_y * screen_height * sensitivity)
    
    return self._smooth(screen_x, screen_y)
```

---

### 3. Gesture Recognition (`gesture_recognizer.py`)

#### Gesture Detection Logic

##### Finger Extension Check
```python
def _is_finger_extended(tip_idx, pip_idx):
    # Finger is extended if TIP is above (lower y) than PIP
    return landmarks[tip_idx][1] < landmarks[pip_idx][1]
```

##### Thumb Extension Check
```python
def _is_thumb_extended():
    # Thumb uses X-axis (horizontal extension)
    thumb_tip = landmarks[THUMB_TIP]
    thumb_ip = landmarks[THUMB_IP]
    wrist = landmarks[WRIST]
    
    # Extended if TIP is further from wrist than IP
    return abs(thumb_tip[0] - wrist[0]) > abs(thumb_ip[0] - wrist[0])
```

#### Gesture State Machine
```
                    ┌─────────────┐
                    │    NONE     │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│    POINT      │  │    PINCH      │  │   OPEN_PALM   │
│ (index only)  │  │ (thumb+index) │  │  (all fingers)│
└───────────────┘  └───────┬───────┘  └───────────────┘
                           │
                    ┌──────┴──────┐
                    ↓             ↓
             ┌───────────┐  ┌───────────┐
             │  CLICK    │  │   DRAG    │
             │ (<0.5s)   │  │ (>0.5s)   │
             └───────────┘  └───────────┘
```

---

### 4. Mouse Controller (`mouse_controller.py`)

#### ROI (Region of Interest) Mapping
```python
# Default ROI boundaries (percentages of frame)
roi_x_min = 0.2  # Left 20%
roi_x_max = 0.8  # Right 80%
roi_y_min = 0.1  # Top 10%
roi_y_max = 0.7  # Bottom 70%

def map_to_screen(x, y, frame_width, frame_height):
    # Normalize position within ROI
    norm_x = (x - roi_left) / roi_width
    norm_y = (y - roi_top) / roi_height
    
    # Map to screen with sensitivity
    screen_x = norm_x * screen_width * sensitivity
    screen_y = norm_y * screen_height * sensitivity
    
    return clamp(screen_x, screen_y)
```

#### Smoothing Algorithm
```python
def _smooth_position(x, y):
    # Add to position history
    position_history.append((x, y))
    
    # Weighted moving average (recent = higher weight)
    total_weight = 0
    weighted_x = weighted_y = 0
    
    for i, (px, py) in enumerate(position_history):
        weight = i + 1  # Linear weighting
        weighted_x += px * weight
        weighted_y += py * weight
        total_weight += weight
    
    avg_x = weighted_x / total_weight
    avg_y = weighted_y / total_weight
    
    # Exponential smoothing
    final_x = prev_x + (avg_x - prev_x) * (1 - smoothing)
    final_y = prev_y + (avg_y - prev_y) * (1 - smoothing)
    
    return final_x, final_y
```

---

### 5. Application Class (`app.py`)

#### Lifecycle Management
```
┌─────────────────────────────────────────────────┐
│                 HCIApplication                   │
├─────────────────────────────────────────────────┤
│  __init__()                                      │
│    ├── Load configuration                        │
│    ├── Initialize logger                         │
│    └── Set initial mode                         │
│                                                  │
│  run()                                           │
│    ├── _init_components()                        │
│    │     ├── HandTracker                         │
│    │     ├── EyeTracker                          │
│    │     ├── GestureRecognizer                   │
│    │     └── MouseController                     │
│    ├── _init_camera()                            │
│    └── Main Loop:                                │
│          ├── capture frame                       │
│          ├── process_frame()                     │
│          ├── _handle_gestures()                  │
│          ├── _draw_ui()                          │
│          └── handle keyboard                     │
│                                                  │
│  cleanup()                                       │
│    ├── Release camera                            │
│    ├── Release trackers                          │
│    └── Close windows                             │
└─────────────────────────────────────────────────┘
```

---

## Performance Optimization

### Frame Processing Pipeline
1. **Capture**: ~5ms (webcam read)
2. **Hand Detection**: ~15-20ms (MediaPipe)
3. **Eye Detection**: ~15-20ms (MediaPipe Face Mesh)
4. **Gesture Recognition**: ~1ms (landmark processing)
5. **Cursor Update**: ~1ms (PyAutoGUI)
6. **UI Rendering**: ~5ms (OpenCV drawing)

**Total**: ~40-50ms per frame = **20-25 FPS**

### Optimization Techniques
1. **Single hand tracking** - Reduces processing load
2. **Lazy initialization** - Components loaded on demand
3. **Position history buffer** - Fixed size deque for smoothing
4. **Skip frames** - Optional frame skipping for lower-end hardware

---

## Configuration System

### Settings Priority
1. **Runtime changes** (keyboard shortcuts)
2. **GUI settings** (saved to JSON)
3. **Config file** (`config/settings.json`)
4. **Default values** (hardcoded)

### CalibrationManager Class
```python
class CalibrationManager:
    def __init__(self, config_path=None):
        self.config_path = config_path or "config/settings.json"
        self.settings = self._load_settings()
    
    def get(self, key, default=None):
        return self.settings.get(key, default)
    
    def set(self, key, value):
        self.settings[key] = value
    
    def save_settings(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.settings, f, indent=2)
```

---

## Error Handling

### Fail-Safe Protection
```python
def _safe_move_to(x, y):
    # Keep cursor away from edges
    edge_padding = 5
    safe_x = clamp(x, edge_padding, screen_width - edge_padding)
    safe_y = clamp(y, edge_padding, screen_height - edge_padding)
    
    try:
        pyautogui.moveTo(safe_x, safe_y)
    except pyautogui.FailSafeException:
        # Skip movement if fail-safe triggered
        logger.warning("Fail-safe triggered")
```

### Graceful Degradation
- Camera failure → Show error, exit gracefully
- Tracking loss → Reset position history
- Low FPS → Continue with reduced accuracy

---

## Testing Strategy

### Unit Tests
- **GestureRecognizer**: 11 tests (gesture detection, thresholds)
- **MouseController**: 6 tests (mapping, smoothing, ROI)
- **CalibrationManager**: 4 tests (load, save, defaults)

### Integration Tests
- Full pipeline with mock webcam input
- Mode switching verification
- Settings persistence

### Manual Testing
- Real webcam with various lighting
- Different hand sizes and skin tones
- Multiple control modes

---

## Security Considerations

### PyAutoGUI Fail-Safe
- Enabled by default (cursor to corner = emergency stop)
- Edge padding prevents accidental triggers
- Exception handling for graceful recovery

### Camera Access
- Requires explicit user permission
- Camera released on application exit
- No network transmission of video data

---

## Future Improvements

### Planned Features
- [ ] Blink-to-click functionality
- [ ] Voice command integration
- [ ] Multi-gesture macros
- [ ] Calibration wizard
- [ ] Profile management

### Performance Goals
- [ ] 30+ FPS on mid-range hardware
- [ ] GPU acceleration for detection
- [ ] Reduced memory footprint
