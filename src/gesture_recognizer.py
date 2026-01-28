"""
Gesture Recognizer Module

Detects hand gestures from landmark positions and triggers corresponding actions.
Supports: cursor movement, left/right click, scrolling, drag operations.
"""

import numpy as np
from typing import List, Tuple, Optional
from enum import Enum
import time


class Gesture(Enum):
    """Enum of recognized gestures."""
    NONE = "none"
    POINT = "point"           # Index finger extended - cursor movement
    PINCH = "pinch"           # Thumb + Index close - left click
    OPEN_PALM = "open_palm"   # All fingers extended - right click (hold)
    VICTORY = "victory"       # Index + Middle extended - scroll mode
    FIST = "fist"             # All fingers closed


class GestureRecognizer:
    """
    Hand gesture recognition from MediaPipe landmarks.
    
    Attributes:
        pinch_threshold: Distance threshold for pinch detection
        click_cooldown: Minimum time between clicks (seconds)
    """
    
    # Landmark indices
    THUMB_TIP = 4
    INDEX_TIP = 8
    MIDDLE_TIP = 12
    RING_TIP = 16
    PINKY_TIP = 20
    
    THUMB_IP = 3
    INDEX_PIP = 6
    MIDDLE_PIP = 10
    RING_PIP = 14
    PINKY_PIP = 18
    
    WRIST = 0
    
    def __init__(
        self,
        pinch_threshold: int = 40,
        click_cooldown: float = 0.3,
        double_click_threshold: float = 0.4
    ):
        """
        Initialize gesture recognizer.
        
        Args:
            pinch_threshold: Pixel distance for pinch detection
            click_cooldown: Seconds between consecutive clicks
            double_click_threshold: Max seconds between clicks to register double-click
        """
        self.pinch_threshold = pinch_threshold
        self.click_cooldown = click_cooldown
        self.double_click_threshold = double_click_threshold
        
        self.last_click_time = 0
        self.last_gesture = Gesture.NONE
        self.gesture_start_time = 0
        
        # For detecting gesture holds
        self.open_palm_hold_time = 0
        self.open_palm_threshold = 1.5  # seconds to hold for right-click
        
        # Double-click detection
        self.click_count = 0
        self.first_click_time = 0
        
        # Drag mode tracking
        self.is_dragging = False
        self.drag_start_time = 0
        self.pinch_hold_threshold = 0.5  # seconds to hold pinch to start drag
        
    def _distance(
        self, 
        p1: Tuple[int, int], 
        p2: Tuple[int, int]
    ) -> float:
        """Calculate Euclidean distance between two points."""
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def _is_finger_extended(
        self,
        landmarks: List[Tuple[int, int]],
        tip_idx: int,
        pip_idx: int
    ) -> bool:
        """
        Check if a finger is extended based on tip vs PIP joint position.
        
        Args:
            landmarks: List of 21 landmark positions
            tip_idx: Fingertip landmark index
            pip_idx: PIP joint landmark index
            
        Returns:
            True if finger is extended
        """
        if landmarks[tip_idx] is None or landmarks[pip_idx] is None:
            return False
            
        # Finger is extended if tip is above (lower y) than PIP joint
        return landmarks[tip_idx][1] < landmarks[pip_idx][1]
    
    def _is_thumb_extended(
        self,
        landmarks: List[Tuple[int, int]]
    ) -> bool:
        """Check if thumb is extended (uses x-axis comparison)."""
        if landmarks[self.THUMB_TIP] is None or landmarks[self.THUMB_IP] is None:
            return False
            
        # Thumb extended if tip is further from palm than IP joint
        return abs(landmarks[self.THUMB_TIP][0] - landmarks[self.WRIST][0]) > \
               abs(landmarks[self.THUMB_IP][0] - landmarks[self.WRIST][0])
    
    def recognize(
        self,
        landmarks: Optional[List[Tuple[int, int]]]
    ) -> Gesture:
        """
        Recognize gesture from hand landmarks.
        
        Args:
            landmarks: List of 21 (x, y) landmark positions
            
        Returns:
            Recognized Gesture enum value
        """
        if not landmarks or len(landmarks) < 21:
            return Gesture.NONE
        
        # Check finger states
        index_extended = self._is_finger_extended(
            landmarks, self.INDEX_TIP, self.INDEX_PIP
        )
        middle_extended = self._is_finger_extended(
            landmarks, self.MIDDLE_TIP, self.MIDDLE_PIP
        )
        ring_extended = self._is_finger_extended(
            landmarks, self.RING_TIP, self.RING_PIP
        )
        pinky_extended = self._is_finger_extended(
            landmarks, self.PINKY_TIP, self.PINKY_PIP
        )
        thumb_extended = self._is_thumb_extended(landmarks)
        
        # Count extended fingers
        extended_count = sum([
            index_extended, middle_extended, 
            ring_extended, pinky_extended, thumb_extended
        ])
        
        # Check for pinch (thumb and index close together)
        if landmarks[self.THUMB_TIP] and landmarks[self.INDEX_TIP]:
            pinch_distance = self._distance(
                landmarks[self.THUMB_TIP],
                landmarks[self.INDEX_TIP]
            )
            if pinch_distance < self.pinch_threshold:
                return Gesture.PINCH
        
        # Open palm (all fingers extended)
        if extended_count >= 4:
            return Gesture.OPEN_PALM
        
        # Victory sign (index and middle extended, others folded)
        if index_extended and middle_extended and not ring_extended and not pinky_extended:
            return Gesture.VICTORY
        
        # Fist (no fingers extended)
        if extended_count == 0:
            return Gesture.FIST
        
        # Point (only index extended)
        if index_extended and not middle_extended and not ring_extended and not pinky_extended:
            return Gesture.POINT
        
        return Gesture.NONE
    
    def should_click(self, gesture: Gesture) -> bool:
        """
        Check if a click should be triggered based on gesture and cooldown.
        
        Args:
            gesture: Current detected gesture
            
        Returns:
            True if click should be triggered
        """
        current_time = time.time()
        
        if gesture == Gesture.PINCH:
            if current_time - self.last_click_time > self.click_cooldown:
                self.last_click_time = current_time
                return True
                
        return False
    
    def should_right_click(self, gesture: Gesture) -> bool:
        """
        Check if right-click should be triggered (open palm hold).
        
        Args:
            gesture: Current detected gesture
            
        Returns:
            True if right-click should be triggered
        """
        current_time = time.time()
        
        if gesture == Gesture.OPEN_PALM:
            if self.last_gesture != Gesture.OPEN_PALM:
                self.open_palm_hold_time = current_time
            elif current_time - self.open_palm_hold_time >= self.open_palm_threshold:
                self.open_palm_hold_time = current_time  # Reset to prevent repeated triggers
                return True
        
        self.last_gesture = gesture
        return False
    
    def is_scroll_mode(self, gesture: Gesture) -> bool:
        """Check if in scroll mode (victory gesture)."""
        return gesture == Gesture.VICTORY
    
    def set_pinch_threshold(self, threshold: int):
        """Update pinch detection threshold."""
        self.pinch_threshold = threshold
    
    def set_click_cooldown(self, cooldown: float):
        """Update click cooldown time."""
        self.click_cooldown = cooldown
    
    def should_double_click(self, gesture: Gesture) -> bool:
        """
        Check if double-click should be triggered (two pinches in quick succession).
        
        Args:
            gesture: Current detected gesture
            
        Returns:
            True if double-click should be triggered
        """
        current_time = time.time()
        
        # Only count when transitioning TO pinch
        if gesture == Gesture.PINCH and self.last_gesture != Gesture.PINCH:
            if self.click_count == 0:
                self.first_click_time = current_time
                self.click_count = 1
            elif current_time - self.first_click_time <= self.double_click_threshold:
                self.click_count = 0
                return True
            else:
                # Too slow, start over
                self.first_click_time = current_time
                self.click_count = 1
        
        # Reset if too much time passed
        if current_time - self.first_click_time > self.double_click_threshold:
            self.click_count = 0
            
        return False
    
    def should_start_drag(self, gesture: Gesture) -> bool:
        """
        Check if drag should start (hold pinch for threshold).
        
        Args:
            gesture: Current detected gesture
            
        Returns:
            True if drag should start
        """
        current_time = time.time()
        
        if gesture == Gesture.PINCH:
            if not self.is_dragging:
                if self.last_gesture != Gesture.PINCH:
                    self.drag_start_time = current_time
                elif current_time - self.drag_start_time >= self.pinch_hold_threshold:
                    self.is_dragging = True
                    return True
        else:
            self.drag_start_time = 0
            
        return False
    
    def should_end_drag(self, gesture: Gesture) -> bool:
        """
        Check if drag should end (release pinch).
        
        Args:
            gesture: Current detected gesture
            
        Returns:
            True if drag should end
        """
        if self.is_dragging and gesture != Gesture.PINCH:
            self.is_dragging = False
            return True
        return False
    
    def get_drag_state(self) -> bool:
        """Return current drag state."""
        return self.is_dragging

