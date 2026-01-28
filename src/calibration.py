"""
Calibration Module

Handles user calibration for sensitivity settings and gesture customization.
"""

import json
import os
from typing import Dict, Any
from pathlib import Path


class CalibrationManager:
    """
    Manages user calibration settings and persistence.
    
    Attributes:
        config_path: Path to settings JSON file
        settings: Current settings dictionary
    """
    
    DEFAULT_SETTINGS = {
        "cursor_sensitivity": 1.5,
        "cursor_smoothing": 0.5,
        "pinch_threshold": 40,
        "click_cooldown": 0.3,
        "scroll_speed": 5,
        "enable_eye_tracking": False,
        "enable_hand_tracking": True,
        "show_landmarks": True,
        "show_fps": True,
    }
    
    def __init__(self, config_path: str = None):
        """
        Initialize calibration manager.
        
        Args:
            config_path: Path to config file (default: config/settings.json)
        """
        if config_path is None:
            base_dir = Path(__file__).parent.parent
            config_path = base_dir / "config" / "settings.json"
            
        self.config_path = Path(config_path)
        self.settings: Dict[str, Any] = self.DEFAULT_SETTINGS.copy()
        
        self._load_settings()
    
    def _load_settings(self):
        """Load settings from config file if it exists."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    loaded = json.load(f)
                    self.settings.update(loaded)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load settings: {e}")
    
    def save_settings(self):
        """Save current settings to config file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a setting value."""
        self.settings[key] = value
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save_settings()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all settings as dictionary."""
        return self.settings.copy()
