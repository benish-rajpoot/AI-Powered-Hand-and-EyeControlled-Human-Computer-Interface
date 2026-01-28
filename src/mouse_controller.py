"""
Mouse Controller Module

Controls the system mouse cursor using PyAutoGUI.
Handles cursor movement, clicking, and scrolling actions.
Features ROI-based mapping and advanced smoothing.
"""

import pyautogui
from typing import Tuple, Optional
from collections import deque
import numpy as np


# Disable PyAutoGUI's fail-safe (move mouse to corner to abort)
# Enable this in production for safety
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0  # Remove delay between PyAutoGUI calls


class MouseController:
    """
    System mouse controller with ROI mapping and advanced smoothing.
    
    Attributes:
        screen_width: Screen width in pixels
        screen_height: Screen height in pixels
        sensitivity: Movement sensitivity multiplier
        smoothing: Smoothing factor (0-1, higher = smoother)
    """
    
    def __init__(
        self,
        sensitivity: float = 1.5,
        smoothing: float = 0.5,
        history_size: int = 5
    ):
        """
        Initialize the mouse controller.
        
        Args:
            sensitivity: Movement sensitivity (default: 1.5)
            smoothing: Smoothing factor for cursor movement (default: 0.5)
            history_size: Number of positions to average for smoothing (default: 5)
        """
        self.screen_width, self.screen_height = pyautogui.size()
        self.sensitivity = sensitivity
        self.smoothing = smoothing
        
        # Position history for advanced smoothing
        self.history_size = history_size
        self.position_history: deque = deque(maxlen=history_size)
        
        self.prev_x: Optional[float] = None
        self.prev_y: Optional[float] = None
        
        # ROI (Region of Interest) - define active area in webcam frame
        # These are percentages (0.0 to 1.0) of the frame
        self.roi_x_min = 0.2  # Left boundary (20% from left)
        self.roi_x_max = 0.8  # Right boundary (80% from left)
        self.roi_y_min = 0.1  # Top boundary (10% from top)
        self.roi_y_max = 0.7  # Bottom boundary (70% from top)
        
    def set_roi(
        self,
        x_min: float = 0.2,
        x_max: float = 0.8,
        y_min: float = 0.1,
        y_max: float = 0.7
    ):
        """
        Set the Region of Interest for cursor mapping.
        
        Args:
            x_min: Left boundary (0.0-1.0)
            x_max: Right boundary (0.0-1.0)
            y_min: Top boundary (0.0-1.0)
            y_max: Bottom boundary (0.0-1.0)
        """
        self.roi_x_min = max(0.0, min(1.0, x_min))
        self.roi_x_max = max(0.0, min(1.0, x_max))
        self.roi_y_min = max(0.0, min(1.0, y_min))
        self.roi_y_max = max(0.0, min(1.0, y_max))
        
    def map_to_screen(
        self,
        x: int,
        y: int,
        frame_width: int,
        frame_height: int
    ) -> Tuple[int, int]:
        """
        Map webcam coordinates to screen coordinates using ROI.
        
        Args:
            x: X position in webcam frame
            y: Y position in webcam frame
            frame_width: Width of webcam frame
            frame_height: Height of webcam frame
            
        Returns:
            Tuple of (screen_x, screen_y)
        """
        # Flip x-axis for natural mirror movement
        x = frame_width - x
        
        # Calculate ROI boundaries in pixels
        roi_left = int(frame_width * self.roi_x_min)
        roi_right = int(frame_width * self.roi_x_max)
        roi_top = int(frame_height * self.roi_y_min)
        roi_bottom = int(frame_height * self.roi_y_max)
        
        # Clamp to ROI
        x = max(roi_left, min(x, roi_right))
        y = max(roi_top, min(y, roi_bottom))
        
        # Map ROI to full screen
        roi_width = roi_right - roi_left
        roi_height = roi_bottom - roi_top
        
        if roi_width > 0 and roi_height > 0:
            # Normalize to 0-1 within ROI
            norm_x = (x - roi_left) / roi_width
            norm_y = (y - roi_top) / roi_height
            
            # Map to screen with sensitivity
            screen_x = int(norm_x * self.screen_width * self.sensitivity)
            screen_y = int(norm_y * self.screen_height * self.sensitivity)
        else:
            screen_x = int((x / frame_width) * self.screen_width)
            screen_y = int((y / frame_height) * self.screen_height)
        
        # Clamp to screen bounds
        screen_x = max(0, min(screen_x, self.screen_width - 1))
        screen_y = max(0, min(screen_y, self.screen_height - 1))
        
        return screen_x, screen_y
    
    def _smooth_position(self, x: int, y: int) -> Tuple[int, int]:
        """
        Apply smoothing using position history (moving average).
        
        Args:
            x: Raw x position
            y: Raw y position
            
        Returns:
            Smoothed (x, y) position
        """
        self.position_history.append((x, y))
        
        if len(self.position_history) < 2:
            return x, y
        
        # Calculate weighted moving average (more recent = higher weight)
        total_weight = 0
        weighted_x = 0
        weighted_y = 0
        
        for i, (px, py) in enumerate(self.position_history):
            weight = i + 1  # Linear weighting
            weighted_x += px * weight
            weighted_y += py * weight
            total_weight += weight
        
        avg_x = int(weighted_x / total_weight)
        avg_y = int(weighted_y / total_weight)
        
        # Additional exponential smoothing
        if self.prev_x is not None and self.prev_y is not None:
            avg_x = int(self.prev_x + (avg_x - self.prev_x) * (1 - self.smoothing))
            avg_y = int(self.prev_y + (avg_y - self.prev_y) * (1 - self.smoothing))
        
        return avg_x, avg_y
    
    def move_cursor(
        self,
        x: int,
        y: int,
        frame_width: int,
        frame_height: int
    ):
        """
        Move the cursor to a position with advanced smoothing.
        
        Args:
            x: X position in webcam frame
            y: Y position in webcam frame
            frame_width: Width of webcam frame
            frame_height: Height of webcam frame
        """
        screen_x, screen_y = self.map_to_screen(x, y, frame_width, frame_height)
        
        # Apply smoothing
        screen_x, screen_y = self._smooth_position(screen_x, screen_y)
        
        self.prev_x = screen_x
        self.prev_y = screen_y
        
        # Keep cursor away from edges to prevent fail-safe
        edge_padding = 5
        safe_x = max(edge_padding, min(screen_x, self.screen_width - edge_padding))
        safe_y = max(edge_padding, min(screen_y, self.screen_height - edge_padding))
        
        try:
            pyautogui.moveTo(safe_x, safe_y)
        except pyautogui.FailSafeException:
            # Skip movement if fail-safe is triggered
            pass
    
    def left_click(self):
        """Perform a left mouse click."""
        pyautogui.click()
    
    def right_click(self):
        """Perform a right mouse click."""
        pyautogui.rightClick()
    
    def double_click(self):
        """Perform a double left click."""
        pyautogui.doubleClick()
    
    def scroll(self, amount: int):
        """
        Scroll the mouse wheel.
        
        Args:
            amount: Scroll amount (positive = up, negative = down)
        """
        pyautogui.scroll(amount)
    
    def drag_start(self):
        """Start a drag operation by pressing mouse button."""
        pyautogui.mouseDown()
    
    def drag_end(self):
        """End a drag operation by releasing mouse button."""
        pyautogui.mouseUp()
    
    def set_sensitivity(self, sensitivity: float):
        """Update cursor sensitivity."""
        self.sensitivity = sensitivity
    
    def set_smoothing(self, smoothing: float):
        """Update cursor smoothing factor."""
        self.smoothing = max(0, min(1, smoothing))
        
    def reset_history(self):
        """Clear position history (useful when hand re-enters frame)."""
        self.position_history.clear()
        self.prev_x = None
        self.prev_y = None

