"""
HCI Application Class

Unified application class that integrates all modules with proper
lifecycle management, error handling, and performance optimization.
"""

import cv2
import time
import pyautogui
from typing import Optional, Dict, Any
from pathlib import Path

from hand_tracker import HandTracker
from eye_tracker import EyeTracker
from gesture_recognizer import GestureRecognizer, Gesture
from mouse_controller import MouseController
from calibration import CalibrationManager
from logger import get_logger


class HCIApplication:
    """
    Main application class that orchestrates all HCI components.
    
    Features:
    - Unified lifecycle management (init, run, cleanup)
    - Mode switching (hand/eye/hybrid)
    - Performance monitoring
    - Error recovery
    - Configurable settings
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the HCI application.
        
        Args:
            config_path: Optional path to config file
        """
        # Setup logging
        log_path = Path(__file__).parent.parent / "logs" / "hci.log"
        self.logger = get_logger("HCI", str(log_path))
        self.logger.log_startup()
        
        # Load configuration
        self.config = CalibrationManager(config_path)
        self.logger.info("Configuration loaded")
        
        # Control state - load from config or default to hybrid
        saved_mode = self.config.get("control_mode", "hybrid")
        if saved_mode in ['hand', 'eye', 'hybrid']:
            self.control_mode = saved_mode
        else:
            self.control_mode = 'hybrid'
        self.logger.info(f"Control mode: {self.control_mode}")
        self.running = False
        
        # Performance tracking
        self.fps = 0
        self.prev_time = time.time()
        self.frame_count = 0
        
        # Screen dimensions with edge padding to avoid fail-safe
        self.screen_width, self.screen_height = pyautogui.size()
        self.edge_padding = 5  # Stay 5px away from edges
        self.logger.info(f"Screen: {self.screen_width}x{self.screen_height}")
        
        # Initialize components (lazy - done in start())
        self.hand_tracker: Optional[HandTracker] = None
        self.eye_tracker: Optional[EyeTracker] = None
        self.gesture_recognizer: Optional[GestureRecognizer] = None
        self.mouse_controller: Optional[MouseController] = None
        self.cap: Optional[cv2.VideoCapture] = None
        
        # Scroll state
        self.scroll_start_y: Optional[int] = None
        
        # Blink-to-click state
        self.blink_click_enabled = True
        self.last_blink_time = 0
        self.blink_click_cooldown = 0.5  # Prevent rapid clicks
        self.was_blinking = False  # Track previous blink state for edge detection
        
    def _init_components(self):
        """Initialize all tracking components."""
        self.logger.info("Initializing components...")
        
        # Hand tracker
        self.hand_tracker = HandTracker(
            max_hands=1,
            detection_confidence=0.7,
            tracking_confidence=0.7
        )
        self.logger.info("Hand tracker initialized")
        
        # Eye tracker
        self.eye_tracker = EyeTracker(
            detection_confidence=0.7,
            tracking_confidence=0.7
        )
        self.logger.info("Eye tracker initialized")
        
        # Gesture recognizer
        self.gesture_recognizer = GestureRecognizer(
            pinch_threshold=self.config.get("pinch_threshold", 40),
            click_cooldown=self.config.get("click_cooldown", 0.3)
        )
        self.logger.info("Gesture recognizer initialized")
        
        # Mouse controller
        self.mouse_controller = MouseController(
            sensitivity=self.config.get("cursor_sensitivity", 1.5),
            smoothing=self.config.get("cursor_smoothing", 0.5)
        )
        self.logger.info("Mouse controller initialized")
        
    def _init_camera(self) -> bool:
        """
        Initialize webcam capture.
        
        Returns:
            True if camera opened successfully
        """
        self.logger.info("Opening webcam...")
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            self.logger.error("Failed to open webcam!")
            return False
        
        # Set resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Get actual resolution
        actual_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.logger.info(f"Camera resolution: {actual_w}x{actual_h}")
        
        return True
    
    def set_mode(self, mode: str):
        """
        Set control mode.
        
        Args:
            mode: 'hand', 'eye', or 'hybrid'
        """
        if mode in ['hand', 'eye', 'hybrid']:
            self.control_mode = mode
            self.logger.log_mode_change(mode)
            
            # Reset tracking state when changing modes
            if self.mouse_controller:
                self.mouse_controller.reset_history()
            if self.eye_tracker:
                self.eye_tracker.reset()
    
    def _safe_move_to(self, x: int, y: int):
        """
        Move cursor safely, avoiding screen corners to prevent fail-safe.
        
        Args:
            x: Target x coordinate
            y: Target y coordinate
        """
        # Clamp coordinates to stay away from edges
        safe_x = max(self.edge_padding, min(x, self.screen_width - self.edge_padding))
        safe_y = max(self.edge_padding, min(y, self.screen_height - self.edge_padding))
        
        try:
            pyautogui.moveTo(safe_x, safe_y)
        except pyautogui.FailSafeException:
            # If still triggered, just skip this movement
            self.logger.warning("Fail-safe triggered, skipping movement")
    
    def _process_frame(self, frame) -> tuple:
        """
        Process a single frame.
        
        Args:
            frame: BGR image from webcam
            
        Returns:
            Tuple of (processed_frame, gesture)
        """
        frame_height, frame_width = frame.shape[:2]
        
        # Process based on mode
        if self.control_mode in ['hand', 'hybrid']:
            frame = self.hand_tracker.process_frame(frame)
            
            # Draw ROI
            roi_left = int(frame_width * self.mouse_controller.roi_x_min)
            roi_right = int(frame_width * self.mouse_controller.roi_x_max)
            roi_top = int(frame_height * self.mouse_controller.roi_y_min)
            roi_bottom = int(frame_height * self.mouse_controller.roi_y_max)
            cv2.rectangle(frame, (roi_left, roi_top), (roi_right, roi_bottom), (100, 100, 255), 2)
        
        if self.control_mode in ['eye', 'hybrid']:
            frame = self.eye_tracker.process_frame(frame)
        
        # Get gesture
        landmarks = self.hand_tracker.get_all_landmarks((frame_height, frame_width, 3))
        gesture = self.gesture_recognizer.recognize(landmarks)
        
        return frame, gesture
    
    def _handle_gestures(self, gesture: Gesture, frame_shape: tuple):
        """Handle gesture actions."""
        frame_height, frame_width = frame_shape[:2]
        
        # Check drag end first
        if self.gesture_recognizer.should_end_drag(gesture):
            self.mouse_controller.drag_end()
        
        # Handle dragging
        if self.gesture_recognizer.get_drag_state():
            index_pos = self.hand_tracker.get_index_finger_tip((frame_height, frame_width, 3))
            if index_pos:
                self.mouse_controller.move_cursor(
                    index_pos[0], index_pos[1],
                    frame_width, frame_height
                )
            return
        
        # Eye-only mode cursor and blink-to-click
        if self.control_mode == 'eye':
            if self.eye_tracker.face_detected:
                gaze_point = self.eye_tracker.get_gaze_point(self.screen_width, self.screen_height)
                if gaze_point:
                    self._safe_move_to(gaze_point[0], gaze_point[1])
                
                # Blink-to-click detection
                if self.blink_click_enabled:
                    is_blinking = self.eye_tracker.is_blink_detected()
                    current_time = time.time()
                    
                    # Trigger click on blink END (eyes reopened after being closed)
                    if self.was_blinking and not is_blinking:
                        if current_time - self.last_blink_time > self.blink_click_cooldown:
                            self.mouse_controller.left_click()
                            self.last_blink_time = current_time
                            self.logger.debug("Blink click triggered")
                    
                    self.was_blinking = is_blinking
            return
        
        # Hybrid mode - eye when no hand
        if self.control_mode == 'hybrid':
            if self.eye_tracker.face_detected and not self.hand_tracker.hand_detected:
                gaze_point = self.eye_tracker.get_gaze_point(self.screen_width, self.screen_height)
                if gaze_point:
                    self._safe_move_to(gaze_point[0], gaze_point[1])
                
                # Blink-to-click in hybrid mode (only when hand not detected)
                if self.blink_click_enabled:
                    is_blinking = self.eye_tracker.is_blink_detected()
                    current_time = time.time()
                    
                    # Trigger click on blink END (eyes reopened after being closed)
                    if self.was_blinking and not is_blinking:
                        if current_time - self.last_blink_time > self.blink_click_cooldown:
                            self.mouse_controller.left_click()
                            self.last_blink_time = current_time
                            self.logger.debug("Blink click triggered (hybrid)")
                    
                    self.was_blinking = is_blinking
        
        # Hand gesture processing
        if self.hand_tracker.hand_detected:
            index_pos = self.hand_tracker.get_index_finger_tip((frame_height, frame_width, 3))
            
            if gesture == Gesture.POINT and index_pos:
                self.mouse_controller.move_cursor(
                    index_pos[0], index_pos[1],
                    frame_width, frame_height
                )
                self.scroll_start_y = None
                
            elif gesture == Gesture.PINCH:
                if self.gesture_recognizer.should_double_click(gesture):
                    self.mouse_controller.double_click()
                elif self.gesture_recognizer.should_start_drag(gesture):
                    self.mouse_controller.drag_start()
                elif self.gesture_recognizer.should_click(gesture):
                    self.mouse_controller.left_click()
                self.scroll_start_y = None
                
            elif gesture == Gesture.OPEN_PALM:
                if self.gesture_recognizer.should_right_click(gesture):
                    self.mouse_controller.right_click()
                self.scroll_start_y = None
                
            elif gesture == Gesture.VICTORY and index_pos:
                if self.scroll_start_y is None:
                    self.scroll_start_y = index_pos[1]
                else:
                    scroll_delta = self.scroll_start_y - index_pos[1]
                    if abs(scroll_delta) > 20:
                        scroll_amount = int(scroll_delta / 20) * self.config.get("scroll_speed", 5)
                        self.mouse_controller.scroll(scroll_amount)
                        self.scroll_start_y = index_pos[1]
        else:
            self.mouse_controller.reset_history()
    
    def _draw_ui(self, frame, gesture: Gesture):
        """Draw UI overlay on frame."""
        frame_height, frame_width = frame.shape[:2]
        
        # Mode indicator
        mode_colors = {'hand': (0, 255, 0), 'eye': (255, 165, 0), 'hybrid': (255, 0, 255)}
        cv2.putText(
            frame, f"Mode: {self.control_mode.upper()}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, mode_colors.get(self.control_mode, (255, 255, 255)), 2
        )
        
        # Gesture (hand/hybrid mode)
        if self.control_mode in ['hand', 'hybrid']:
            cv2.putText(
                frame, f"Gesture: {gesture.value}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
            )
        
        # FPS
        if self.config.get("show_fps", True):
            cv2.putText(
                frame, f"FPS: {int(self.fps)}", (frame_width - 100, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2
            )
        
        # Drag indicator
        if self.gesture_recognizer.get_drag_state():
            cv2.putText(
                frame, "DRAGGING", (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2
            )
        
        return frame
    
    def _update_fps(self):
        """Update FPS calculation."""
        current_time = time.time()
        self.frame_count += 1
        
        elapsed = current_time - self.prev_time
        if elapsed >= 1.0:
            self.fps = self.frame_count / elapsed
            self.frame_count = 0
            self.prev_time = current_time
            self.logger.log_fps(self.fps)
    
    def run(self):
        """Main application loop."""
        # Initialize
        self._init_components()
        
        if not self._init_camera():
            self.logger.error("Cannot start without camera")
            return
        
        self.running = True
        self.logger.info("Application started - show hand to camera")
        
        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    self.logger.warning("Failed to read frame")
                    continue
                
                # Mirror frame
                frame = cv2.flip(frame, 1)
                
                # Process
                frame, gesture = self._process_frame(frame)
                
                # Handle gestures
                self._handle_gestures(gesture, frame.shape)
                
                # Update gesture state
                self.gesture_recognizer.last_gesture = gesture
                
                # Draw UI
                frame = self._draw_ui(frame, gesture)
                
                # Update FPS
                self._update_fps()
                
                # Display
                cv2.imshow("Hand & Eye Controlled HCI", frame)
                
                # Handle keys
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.running = False
                elif key == ord('h'):
                    self.set_mode('hand')
                elif key == ord('e'):
                    self.set_mode('eye')
                elif key == ord('b'):
                    self.set_mode('hybrid')
                    
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user")
        except Exception as e:
            self.logger.error(f"Error: {e}")
            raise
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        self.logger.info("Cleaning up...")
        
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        
        if self.hand_tracker:
            self.hand_tracker.release()
        if self.eye_tracker:
            self.eye_tracker.release()
        
        self.logger.log_shutdown()


def main():
    """Entry point for the application."""
    app = HCIApplication()
    app.run()


if __name__ == "__main__":
    main()
