"""
Unit Tests for Gesture Recognizer Module

Tests the gesture detection logic with simulated landmark data.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gesture_recognizer import GestureRecognizer, Gesture


class TestGestureRecognizer:
    """Test suite for GestureRecognizer class."""
    
    @pytest.fixture
    def recognizer(self):
        """Create a fresh GestureRecognizer for each test."""
        return GestureRecognizer(pinch_threshold=40, click_cooldown=0.3)
    
    @pytest.fixture
    def base_landmarks(self):
        """
        Create base hand landmarks (21 points).
        All fingers folded by default (including thumb).
        Thumb is folded but far from index (no pinch).
        """
        # Basic hand structure with all fingers folded
        # Format: (x, y) for each of 21 landmarks
        # Thumb folded: TIP is CLOSER to wrist than IP (in x-axis)
        # Thumb and index must be >40px apart to avoid pinch detection
        landmarks = [
            (300, 400),  # 0: Wrist
            (250, 380),  # 1: Thumb CMC
            (200, 350),  # 2: Thumb MCP
            (180, 320),  # 3: Thumb IP (further from wrist in x)
            (200, 310),  # 4: Thumb TIP (closer to wrist in x = folded, far from index)
            (300, 280),  # 5: Index MCP
            (300, 240),  # 6: Index PIP
            (300, 210),  # 7: Index DIP
            (300, 250),  # 8: Index TIP (below PIP = folded)
            (320, 280),  # 9: Middle MCP
            (320, 240),  # 10: Middle PIP
            (320, 210),  # 11: Middle DIP
            (320, 250),  # 12: Middle TIP (below PIP = folded)
            (340, 290),  # 13: Ring MCP
            (340, 250),  # 14: Ring PIP
            (340, 220),  # 15: Ring DIP
            (340, 260),  # 16: Ring TIP (below PIP = folded)
            (360, 300),  # 17: Pinky MCP
            (360, 270),  # 18: Pinky PIP
            (360, 250),  # 19: Pinky DIP
            (360, 280),  # 20: Pinky TIP (below PIP = folded)
        ]
        return landmarks
    
    def _extend_index(self, landmarks):
        """Modify landmarks to extend index finger."""
        landmarks = list(landmarks)
        landmarks[8] = (300, 180)  # Index TIP above PIP
        return landmarks
    
    def _extend_middle(self, landmarks):
        """Modify landmarks to extend middle finger."""
        landmarks = list(landmarks)
        landmarks[12] = (320, 180)  # Middle TIP above PIP
        return landmarks
    
    def _extend_all(self, landmarks):
        """Modify landmarks to extend all fingers (open palm)."""
        landmarks = list(landmarks)
        landmarks[4] = (180, 230)   # Thumb extended outward
        landmarks[8] = (300, 180)   # Index TIP above PIP
        landmarks[12] = (320, 180)  # Middle TIP above PIP
        landmarks[16] = (340, 180)  # Ring TIP above PIP
        landmarks[20] = (360, 180)  # Pinky TIP above PIP
        return landmarks
    
    def _create_pinch(self, landmarks):
        """Modify landmarks to create pinch gesture (thumb + index close)."""
        landmarks = list(landmarks)
        landmarks[4] = (290, 200)   # Thumb TIP
        landmarks[8] = (300, 195)   # Index TIP - very close to thumb
        return landmarks
    
    # ===== TESTS =====
    
    def test_recognize_none_no_landmarks(self, recognizer):
        """Test that None/empty landmarks returns NONE gesture."""
        assert recognizer.recognize(None) == Gesture.NONE
        assert recognizer.recognize([]) == Gesture.NONE
        assert recognizer.recognize([(0, 0)] * 10) == Gesture.NONE  # Too few
    
    def test_recognize_fist(self, recognizer, base_landmarks):
        """Test that all fingers folded returns FIST gesture."""
        gesture = recognizer.recognize(base_landmarks)
        assert gesture == Gesture.FIST
    
    def test_recognize_point(self, recognizer, base_landmarks):
        """Test that only index extended returns POINT gesture."""
        landmarks = self._extend_index(base_landmarks)
        gesture = recognizer.recognize(landmarks)
        assert gesture == Gesture.POINT
    
    def test_recognize_victory(self, recognizer, base_landmarks):
        """Test that index + middle extended returns VICTORY gesture."""
        landmarks = self._extend_index(base_landmarks)
        landmarks = self._extend_middle(landmarks)
        gesture = recognizer.recognize(landmarks)
        assert gesture == Gesture.VICTORY
    
    def test_recognize_open_palm(self, recognizer, base_landmarks):
        """Test that all fingers extended returns OPEN_PALM gesture."""
        landmarks = self._extend_all(base_landmarks)
        gesture = recognizer.recognize(landmarks)
        assert gesture == Gesture.OPEN_PALM
    
    def test_recognize_pinch(self, recognizer, base_landmarks):
        """Test that thumb + index close together returns PINCH gesture."""
        landmarks = self._create_pinch(base_landmarks)
        gesture = recognizer.recognize(landmarks)
        assert gesture == Gesture.PINCH
    
    def test_pinch_below_threshold(self, recognizer, base_landmarks):
        """Test that fingers must be within threshold for pinch."""
        landmarks = list(base_landmarks)
        # Set thumb and index far apart (beyond threshold)
        landmarks[4] = (200, 200)  # Thumb TIP
        landmarks[8] = (350, 200)  # Index TIP - far from thumb
        gesture = recognizer.recognize(landmarks)
        assert gesture != Gesture.PINCH
    
    def test_should_click_with_cooldown(self, recognizer):
        """Test that click respects cooldown period."""
        # First click should work
        assert recognizer.should_click(Gesture.PINCH) == True
        
        # Immediate second click should be blocked
        assert recognizer.should_click(Gesture.PINCH) == False
    
    def test_scroll_mode_detection(self, recognizer):
        """Test scroll mode detection."""
        assert recognizer.is_scroll_mode(Gesture.VICTORY) == True
        assert recognizer.is_scroll_mode(Gesture.POINT) == False
        assert recognizer.is_scroll_mode(Gesture.PINCH) == False
    
    def test_set_pinch_threshold(self, recognizer):
        """Test updating pinch threshold."""
        recognizer.set_pinch_threshold(100)
        assert recognizer.pinch_threshold == 100
    
    def test_set_click_cooldown(self, recognizer):
        """Test updating click cooldown."""
        recognizer.set_click_cooldown(0.5)
        assert recognizer.click_cooldown == 0.5


class TestMouseController:
    """Test suite for MouseController class."""
    
    @pytest.fixture
    def controller(self):
        """Create MouseController for testing."""
        from mouse_controller import MouseController
        return MouseController(sensitivity=1.5, smoothing=0.5)
    
    def test_map_to_screen_basic(self, controller):
        """Test basic coordinate mapping."""
        screen_x, screen_y = controller.map_to_screen(
            x=640, y=360,
            frame_width=1280, frame_height=720
        )
        # Should return valid screen coordinates
        assert 0 <= screen_x < controller.screen_width
        assert 0 <= screen_y < controller.screen_height
    
    def test_map_to_screen_clamped(self, controller):
        """Test that coordinates are clamped to screen bounds."""
        # Test extreme values
        screen_x, screen_y = controller.map_to_screen(
            x=10000, y=10000,
            frame_width=1280, frame_height=720
        )
        assert screen_x < controller.screen_width
        assert screen_y < controller.screen_height
    
    def test_sensitivity_update(self, controller):
        """Test sensitivity setter."""
        controller.set_sensitivity(2.0)
        assert controller.sensitivity == 2.0
    
    def test_smoothing_update(self, controller):
        """Test smoothing setter with clamping."""
        controller.set_smoothing(0.8)
        assert controller.smoothing == 0.8
        
        controller.set_smoothing(1.5)  # Should clamp to 1
        assert controller.smoothing == 1.0
        
        controller.set_smoothing(-0.5)  # Should clamp to 0
        assert controller.smoothing == 0.0
    
    def test_reset_history(self, controller):
        """Test position history reset."""
        # Simulate some movements
        controller.prev_x = 100
        controller.prev_y = 200
        
        controller.reset_history()
        
        assert controller.prev_x is None
        assert controller.prev_y is None
        assert len(controller.position_history) == 0
    
    def test_roi_bounds(self, controller):
        """Test ROI setter with bounds checking."""
        controller.set_roi(0.1, 0.9, 0.2, 0.8)
        
        assert controller.roi_x_min == 0.1
        assert controller.roi_x_max == 0.9
        assert controller.roi_y_min == 0.2
        assert controller.roi_y_max == 0.8


class TestCalibrationManager:
    """Test suite for CalibrationManager class."""
    
    @pytest.fixture
    def manager(self, tmp_path):
        """Create CalibrationManager with temp config path."""
        from calibration import CalibrationManager
        config_path = tmp_path / "test_settings.json"
        return CalibrationManager(str(config_path))
    
    def test_get_default_values(self, manager):
        """Test that default values are returned."""
        assert manager.get("cursor_sensitivity") is not None
        assert manager.get("pinch_threshold") is not None
    
    def test_set_and_get(self, manager):
        """Test setting and getting values."""
        manager.set("test_key", "test_value")
        assert manager.get("test_key") == "test_value"
    
    def test_save_and_load(self, manager, tmp_path):
        """Test saving and loading settings."""
        from calibration import CalibrationManager
        
        manager.set("custom_setting", 42)
        manager.save_settings()
        
        # Create new manager with same path
        new_manager = CalibrationManager(str(tmp_path / "test_settings.json"))
        assert new_manager.get("custom_setting") == 42
    
    def test_reset_to_defaults(self, manager):
        """Test reset to defaults."""
        manager.set("cursor_sensitivity", 99)
        manager.reset_to_defaults()
        
        # Should be back to default (1.5)
        assert manager.get("cursor_sensitivity") == 1.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
