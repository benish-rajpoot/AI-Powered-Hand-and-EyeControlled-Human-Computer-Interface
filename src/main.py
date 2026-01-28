"""
AI-Powered Hand and Eye Controlled Human-Computer Interface

Main entry point for the application.
Captures webcam feed and processes hand gestures and eye gaze for mouse control.
"""

import cv2
import time
import pyautogui
from hand_tracker import HandTracker
from eye_tracker import EyeTracker
from gesture_recognizer import GestureRecognizer, Gesture
from mouse_controller import MouseController
from calibration import CalibrationManager


def main():
    """Main application loop."""
    print("=" * 50)
    print("AI-Powered Hand & Eye Controlled HCI")
    print("=" * 50)
    print("\nGesture Controls:")
    print("  - Point (index finger): Move cursor")
    print("  - Pinch (thumb + index): Left click")
    print("  - Quick double pinch:    Double click")
    print("  - Hold pinch (0.5s):     Start drag")
    print("  - Open palm (hold 1.5s): Right click")
    print("  - Victory sign (✌️):     Scroll mode")
    print("\nMode Controls:")
    print("  - Press 'h': Hand-only mode")
    print("  - Press 'e': Eye-only mode")
    print("  - Press 'b': Hybrid mode (both)")
    print("  - Press 'q': Quit")
    print("=" * 50)
    
    # Get screen size
    screen_width, screen_height = pyautogui.size()
    
    # Initialize components
    config = CalibrationManager()
    hand_tracker = HandTracker(
        max_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.7
    )
    eye_tracker = EyeTracker(
        detection_confidence=0.7,
        tracking_confidence=0.7
    )
    gesture_recognizer = GestureRecognizer(
        pinch_threshold=config.get("pinch_threshold", 40),
        click_cooldown=config.get("click_cooldown", 0.3)
    )
    mouse_controller = MouseController(
        sensitivity=config.get("cursor_sensitivity", 1.5),
        smoothing=config.get("cursor_smoothing", 0.5)
    )
    
    # Control mode: 'hand', 'eye', or 'hybrid'
    control_mode = 'hand' if not config.get("enable_eye_tracking", False) else 'hybrid'
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # FPS calculation
    prev_time = time.time()
    fps = 0
    
    # Scroll tracking
    scroll_start_y = None
    
    print("\nStarting... (Show your hand to the camera)")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Flip horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            frame_height, frame_width = frame.shape[:2]
            
            # Process based on control mode
            if control_mode in ['hand', 'hybrid']:
                frame = hand_tracker.process_frame(frame)
                
                # Draw ROI rectangle for visual feedback
                roi_left = int(frame_width * mouse_controller.roi_x_min)
                roi_right = int(frame_width * mouse_controller.roi_x_max)
                roi_top = int(frame_height * mouse_controller.roi_y_min)
                roi_bottom = int(frame_height * mouse_controller.roi_y_max)
                cv2.rectangle(frame, (roi_left, roi_top), (roi_right, roi_bottom), (100, 100, 255), 2)
                cv2.putText(frame, "Hand Zone", (roi_left + 5, roi_top + 25),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 255), 2)
            
            if control_mode in ['eye', 'hybrid']:
                frame = eye_tracker.process_frame(frame)
            
            # Display current mode
            mode_colors = {'hand': (0, 255, 0), 'eye': (255, 165, 0), 'hybrid': (255, 0, 255)}
            cv2.putText(
                frame, f"Mode: {control_mode.upper()}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, mode_colors.get(control_mode, (255, 255, 255)), 2
            )
            
            # Get landmarks and recognize gesture
            landmarks = hand_tracker.get_all_landmarks((frame_height, frame_width, 3))
            gesture = gesture_recognizer.recognize(landmarks)
            
            # Display gesture (only in hand/hybrid mode)
            if control_mode in ['hand', 'hybrid']:
                gesture_text = f"Gesture: {gesture.value}"
                cv2.putText(
                    frame, gesture_text, (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
                )
            
            # Eye gaze indicator (in eye/hybrid mode)
            if control_mode in ['eye', 'hybrid'] and eye_tracker.face_detected:
                gaze_point = eye_tracker.get_gaze_point(screen_width, screen_height)
                if gaze_point:
                    # Draw gaze indicator on screen position mapped to frame
                    gaze_frame_x = int(gaze_point[0] / screen_width * frame_width)
                    gaze_frame_y = int(gaze_point[1] / screen_height * frame_height)
                    cv2.circle(frame, (gaze_frame_x, gaze_frame_y), 10, (255, 165, 0), 2)
                    cv2.putText(
                        frame, f"Gaze: ({gaze_point[0]}, {gaze_point[1]})", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2
                    )
            
            # Reset cursor history when hand leaves frame
            if not hand_tracker.hand_detected:
                mouse_controller.reset_history()
            
            # ===== CURSOR CONTROL =====
            # Eye-only mode: use gaze for cursor
            if control_mode == 'eye':
                if eye_tracker.face_detected:
                    gaze_point = eye_tracker.get_gaze_point(screen_width, screen_height)
                    if gaze_point:
                        pyautogui.moveTo(gaze_point[0], gaze_point[1])
            
            # Hybrid mode: eye for coarse, hand for fine control
            elif control_mode == 'hybrid':
                if eye_tracker.face_detected and not hand_tracker.hand_detected:
                    # Use eye gaze when no hand detected
                    gaze_point = eye_tracker.get_gaze_point(screen_width, screen_height)
                    if gaze_point:
                        pyautogui.moveTo(gaze_point[0], gaze_point[1])
            
            # Process gestures (hand or hybrid mode)
            if hand_tracker.hand_detected:
                index_pos = hand_tracker.get_index_finger_tip((frame_height, frame_width, 3))
                
                # Check for drag end first (before other gesture processing)
                if gesture_recognizer.should_end_drag(gesture):
                    mouse_controller.drag_end()
                    cv2.putText(
                        frame, "DRAG END!", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 128, 0), 2
                    )
                
                # Show dragging status
                if gesture_recognizer.get_drag_state():
                    cv2.putText(
                        frame, "DRAGGING...", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 2
                    )
                    # Move cursor while dragging
                    if index_pos:
                        mouse_controller.move_cursor(
                            index_pos[0], index_pos[1],
                            frame_width, frame_height
                        )
                
                elif gesture == Gesture.POINT and index_pos:
                    # Move cursor
                    mouse_controller.move_cursor(
                        index_pos[0], index_pos[1],
                        frame_width, frame_height
                    )
                    scroll_start_y = None
                    
                elif gesture == Gesture.PINCH:
                    # Check for double-click first
                    if gesture_recognizer.should_double_click(gesture):
                        mouse_controller.double_click()
                        cv2.putText(
                            frame, "DOUBLE CLICK!", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2
                        )
                    # Then check for drag start
                    elif gesture_recognizer.should_start_drag(gesture):
                        mouse_controller.drag_start()
                        cv2.putText(
                            frame, "DRAG START!", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 128, 0), 2
                        )
                    # Then regular click
                    elif gesture_recognizer.should_click(gesture):
                        mouse_controller.left_click()
                        cv2.putText(
                            frame, "LEFT CLICK!", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
                        )
                    scroll_start_y = None
                    
                elif gesture == Gesture.OPEN_PALM:
                    if gesture_recognizer.should_right_click(gesture):
                        mouse_controller.right_click()
                        cv2.putText(
                            frame, "RIGHT CLICK!", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2
                        )
                    scroll_start_y = None
                    
                elif gesture == Gesture.VICTORY and index_pos:
                    # Scroll mode
                    if scroll_start_y is None:
                        scroll_start_y = index_pos[1]
                    else:
                        scroll_delta = scroll_start_y - index_pos[1]
                        if abs(scroll_delta) > 20:
                            scroll_amount = int(scroll_delta / 20) * config.get("scroll_speed", 5)
                            mouse_controller.scroll(scroll_amount)
                            scroll_start_y = index_pos[1]
                    
                    cv2.putText(
                        frame, "SCROLL MODE", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2
                    )
            
            # Calculate and display FPS
            current_time = time.time()
            fps = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
            prev_time = current_time
            
            if config.get("show_fps", True):
                cv2.putText(
                    frame, f"FPS: {int(fps)}", (frame_width - 120, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2
                )
            
            # Display frame
            cv2.imshow("Hand & Eye Controlled HCI", frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('h'):
                control_mode = 'hand'
                print("Switched to HAND-only mode")
            elif key == ord('e'):
                control_mode = 'eye'
                print("Switched to EYE-only mode")
            elif key == ord('b'):
                control_mode = 'hybrid'
                print("Switched to HYBRID mode (hand + eye)")
                
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        hand_tracker.release()
        eye_tracker.release()
        print("\nApplication closed.")


if __name__ == "__main__":
    main()
