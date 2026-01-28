# API Reference

Complete API documentation for the AI-Powered Hand & Eye Controlled HCI.

---

## Module: `hand_tracker.py`

### Class: `HandTracker`

Real-time hand detection and landmark tracking using MediaPipe.

#### Constructor

```python
HandTracker(
    max_hands: int = 1,
    detection_confidence: float = 0.7,
    tracking_confidence: float = 0.7
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_hands` | int | 1 | Maximum number of hands to detect |
| `detection_confidence` | float | 0.7 | Minimum detection confidence (0.0-1.0) |
| `tracking_confidence` | float | 0.7 | Minimum tracking confidence (0.0-1.0) |

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `hand_detected` | bool | True if a hand is currently detected |

#### Methods

##### `process_frame(frame: np.ndarray) -> np.ndarray`
Process a video frame and detect hand landmarks.

```python
tracker = HandTracker()
processed_frame = tracker.process_frame(bgr_frame)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `frame` | np.ndarray | BGR image from webcam |
| **Returns** | np.ndarray | Frame with landmarks drawn |

##### `get_all_landmarks(frame_shape: tuple) -> List[Tuple[int, int]]`
Get all 21 hand landmarks as pixel coordinates.

```python
landmarks = tracker.get_all_landmarks((height, width, channels))
# Returns: [(x0, y0), (x1, y1), ..., (x20, y20)]
```

##### `get_index_finger_tip(frame_shape: tuple) -> Optional[Tuple[int, int]]`
Get the index finger tip position.

```python
pos = tracker.get_index_finger_tip(frame.shape)
if pos:
    x, y = pos
```

##### `release()`
Release MediaPipe resources.

```python
tracker.release()
```

---

## Module: `eye_tracker.py`

### Class: `EyeTracker`

Eye gaze estimation using MediaPipe Face Mesh with iris tracking.

#### Constructor

```python
EyeTracker(
    detection_confidence: float = 0.7,
    tracking_confidence: float = 0.7
)
```

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `face_detected` | bool | True if a face is currently detected |

#### Methods

##### `process_frame(frame: np.ndarray) -> np.ndarray`
Process frame for face and iris detection.

```python
tracker = EyeTracker()
processed_frame = tracker.process_frame(bgr_frame)
```

##### `get_gaze_point(screen_width: int, screen_height: int) -> Optional[Tuple[int, int]]`
Get estimated gaze point in screen coordinates.

```python
gaze = tracker.get_gaze_point(1920, 1080)
if gaze:
    screen_x, screen_y = gaze
```

##### `get_eye_aspect_ratio() -> float`
Calculate Eye Aspect Ratio (EAR) for blink detection.

```python
ear = tracker.get_eye_aspect_ratio()
if ear < 0.2:
    print("Blink detected!")
```

##### `reset()`
Reset tracking state and smoothing history.

##### `release()`
Release MediaPipe resources.

---

## Module: `gesture_recognizer.py`

### Enum: `Gesture`

Enumeration of recognized hand gestures.

```python
class Gesture(Enum):
    NONE = "none"
    POINT = "point"
    PINCH = "pinch"
    OPEN_PALM = "open_palm"
    VICTORY = "victory"
    FIST = "fist"
```

### Class: `GestureRecognizer`

Recognizes hand gestures from landmark data.

#### Constructor

```python
GestureRecognizer(
    pinch_threshold: int = 40,
    click_cooldown: float = 0.3
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `pinch_threshold` | int | 40 | Max pixel distance for pinch detection |
| `click_cooldown` | float | 0.3 | Seconds between allowed clicks |

#### Methods

##### `recognize(landmarks: List[Tuple[int, int]]) -> Gesture`
Recognize gesture from hand landmarks.

```python
recognizer = GestureRecognizer()
gesture = recognizer.recognize(landmarks)

if gesture == Gesture.PINCH:
    # Handle pinch
    pass
```

##### `should_click(gesture: Gesture) -> bool`
Check if click action should be performed (respects cooldown).

```python
if recognizer.should_click(gesture):
    mouse.left_click()
```

##### `should_double_click(gesture: Gesture) -> bool`
Check for double-click (two pinches within threshold).

##### `should_start_drag(gesture: Gesture) -> bool`
Check if drag operation should start (pinch held).

##### `should_end_drag(gesture: Gesture) -> bool`
Check if drag operation should end.

##### `should_right_click(gesture: Gesture) -> bool`
Check for right-click (palm held).

##### `is_scroll_mode(gesture: Gesture) -> bool`
Check if in scroll mode (victory gesture).

##### `get_drag_state() -> bool`
Returns True if currently dragging.

##### Configuration Methods

```python
recognizer.set_pinch_threshold(50)
recognizer.set_click_cooldown(0.5)
```

---

## Module: `mouse_controller.py`

### Class: `MouseController`

System mouse control with ROI mapping and smoothing.

#### Constructor

```python
MouseController(
    sensitivity: float = 1.5,
    smoothing: float = 0.5,
    history_size: int = 5
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sensitivity` | float | 1.5 | Movement speed multiplier |
| `smoothing` | float | 0.5 | Smoothing factor (0=none, 1=max) |
| `history_size` | int | 5 | Position buffer size |

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `screen_width` | int | Screen width in pixels |
| `screen_height` | int | Screen height in pixels |
| `roi_x_min` | float | Left ROI boundary (0-1) |
| `roi_x_max` | float | Right ROI boundary (0-1) |
| `roi_y_min` | float | Top ROI boundary (0-1) |
| `roi_y_max` | float | Bottom ROI boundary (0-1) |

#### Methods

##### `move_cursor(x, y, frame_width, frame_height)`
Move cursor based on hand position in frame.

```python
controller = MouseController()
controller.move_cursor(320, 240, 640, 480)
```

##### `map_to_screen(x, y, frame_width, frame_height) -> Tuple[int, int]`
Map webcam coordinates to screen coordinates.

```python
screen_x, screen_y = controller.map_to_screen(x, y, 640, 480)
```

##### Click Methods

```python
controller.left_click()      # Single left click
controller.right_click()     # Right click
controller.double_click()    # Double left click
```

##### Drag Methods

```python
controller.drag_start()      # Begin drag (mouse down)
controller.drag_end()        # End drag (mouse up)
```

##### Scroll Methods

```python
controller.scroll(5)         # Scroll up
controller.scroll(-5)        # Scroll down
```

##### Configuration Methods

```python
controller.set_sensitivity(2.0)
controller.set_smoothing(0.7)
controller.set_roi(0.2, 0.8, 0.1, 0.7)
controller.reset_history()
```

---

## Module: `calibration.py`

### Class: `CalibrationManager`

Manages application settings with JSON persistence.

#### Constructor

```python
CalibrationManager(config_path: Optional[str] = None)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `config_path` | str | None | Path to config file |

#### Methods

##### `get(key: str, default=None) -> Any`
Get a setting value.

```python
manager = CalibrationManager()
sensitivity = manager.get("cursor_sensitivity", 1.5)
```

##### `set(key: str, value: Any)`
Set a setting value.

```python
manager.set("cursor_sensitivity", 2.0)
```

##### `get_all() -> Dict[str, Any]`
Get all settings as dictionary.

##### `save_settings()`
Save settings to JSON file.

##### `reset_to_defaults()`
Reset all settings to default values.

---

## Module: `app.py`

### Class: `HCIApplication`

Main application class orchestrating all components.

#### Constructor

```python
HCIApplication(config_path: Optional[str] = None)
```

#### Methods

##### `run()`
Start the main application loop.

```python
app = HCIApplication()
app.run()  # Blocks until quit
```

##### `set_mode(mode: str)`
Set control mode.

```python
app.set_mode("hand")    # Hand only
app.set_mode("eye")     # Eye only
app.set_mode("hybrid")  # Combined
```

##### `cleanup()`
Release all resources.

---

## Module: `logger.py`

### Function: `get_logger(name, log_path)`

Get or create a logger instance.

```python
from logger import get_logger

logger = get_logger("MyModule", "logs/app.log")
logger.info("Application started")
logger.warning("Low FPS detected")
logger.error("Camera not found")
```

### Class: `HCILogger`

Custom logger with color-coded console output.

#### Methods

```python
logger.log_startup()           # Log app start
logger.log_shutdown()          # Log app stop
logger.log_fps(fps: float)     # Log FPS
logger.log_gesture(gesture)    # Log detected gesture
logger.log_mode_change(mode)   # Log mode switch
```

---

## Error Handling

### Common Exceptions

| Exception | Cause | Handling |
|-----------|-------|----------|
| `cv2.error` | Camera issues | Check webcam connection |
| `pyautogui.FailSafeException` | Cursor at corner | Caught and ignored |
| `FileNotFoundError` | Missing config | Uses defaults |

### Example Error Handling

```python
from app import HCIApplication

try:
    app = HCIApplication()
    app.run()
except KeyboardInterrupt:
    print("Interrupted by user")
except Exception as e:
    print(f"Error: {e}")
finally:
    app.cleanup()
```
