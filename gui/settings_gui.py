"""
Calibration GUI Module

Provides a modern settings interface using CustomTkinter.
Allows users to adjust sensitivity, gestures, and control modes.
"""

import customtkinter as ctk
from typing import Callable, Optional, Dict, Any
import json
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from calibration import CalibrationManager
except ImportError:
    CalibrationManager = None


class SettingsWindow(ctk.CTk):
    """
    Modern settings window for the HCI application.
    
    Features:
    - Cursor sensitivity slider
    - Smoothing control
    - Gesture threshold adjustment
    - Mode selection (hand/eye/hybrid)
    - Real-time preview feedback
    """
    
    def __init__(
        self,
        config_manager: Optional[Any] = None,
        on_settings_change: Optional[Callable[[Dict[str, Any]], None]] = None
    ):
        """
        Initialize the settings window.
        
        Args:
            config_manager: CalibrationManager instance (optional)
            on_settings_change: Callback when settings change
        """
        super().__init__()
        
        # Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Window setup
        self.title("HCI Settings & Calibration")
        self.geometry("500x700")
        self.minsize(450, 600)
        
        # Config
        self.config_manager = config_manager
        self.on_settings_change = on_settings_change
        
        # Load current settings
        if self.config_manager:
            self.settings = self.config_manager.get_all()
        else:
            self.settings = self._get_default_settings()
        
        # Create UI
        self._create_widgets()
        
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default settings."""
        return {
            "cursor_sensitivity": 1.0,
            "cursor_smoothing": 0.7,
            "pinch_threshold": 45,
            "click_cooldown": 0.5,
            "scroll_speed": 3,
            "enable_eye_tracking": True,
            "enable_hand_tracking": True,
            "show_landmarks": True,
            "show_fps": True,
            "control_mode": "hand"
        }
    
    def _create_widgets(self):
        """Create all UI widgets."""
        # Main scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(self, label_text="Settings")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title = ctk.CTkLabel(
            self.main_frame,
            text="🖐️ Hand & Eye HCI Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # ===== CONTROL MODE SECTION =====
        self._create_section_header("Control Mode")
        
        self.mode_var = ctk.StringVar(value=self.settings.get("control_mode", "hybrid"))
        mode_frame = ctk.CTkFrame(self.main_frame)
        mode_frame.pack(fill="x", padx=10, pady=5)
        
        modes = [("🖐️ Hand Only", "hand"), ("👁️ Eye Only", "eye"), ("🔄 Hybrid", "hybrid")]
        for i, (text, value) in enumerate(modes):
            rb = ctk.CTkRadioButton(
                mode_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                command=self._on_mode_change
            )
            rb.grid(row=0, column=i, padx=10, pady=10)
        
        # ===== CURSOR SETTINGS =====
        self._create_section_header("Cursor Settings")
        
        # Sensitivity slider
        self.sensitivity_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Sensitivity: {self.settings.get('cursor_sensitivity', 1.5):.1f}"
        )
        self.sensitivity_label.pack(anchor="w", padx=20)
        
        self.sensitivity_slider = ctk.CTkSlider(
            self.main_frame,
            from_=0.5,
            to=3.0,
            number_of_steps=25,
            command=self._on_sensitivity_change
        )
        self.sensitivity_slider.set(self.settings.get("cursor_sensitivity", 1.5))
        self.sensitivity_slider.pack(fill="x", padx=20, pady=(0, 10))
        
        # Smoothing slider
        self.smoothing_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Smoothing: {self.settings.get('cursor_smoothing', 0.5):.1%}"
        )
        self.smoothing_label.pack(anchor="w", padx=20)
        
        self.smoothing_slider = ctk.CTkSlider(
            self.main_frame,
            from_=0.0,
            to=0.9,
            number_of_steps=18,
            command=self._on_smoothing_change
        )
        self.smoothing_slider.set(self.settings.get("cursor_smoothing", 0.5))
        self.smoothing_slider.pack(fill="x", padx=20, pady=(0, 10))
        
        # ===== GESTURE SETTINGS =====
        self._create_section_header("Gesture Settings")
        
        # Pinch threshold
        self.pinch_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Pinch Threshold: {self.settings.get('pinch_threshold', 40)} px"
        )
        self.pinch_label.pack(anchor="w", padx=20)
        
        self.pinch_slider = ctk.CTkSlider(
            self.main_frame,
            from_=20,
            to=80,
            number_of_steps=60,
            command=self._on_pinch_change
        )
        self.pinch_slider.set(self.settings.get("pinch_threshold", 40))
        self.pinch_slider.pack(fill="x", padx=20, pady=(0, 10))
        
        # Click cooldown
        self.cooldown_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Click Cooldown: {self.settings.get('click_cooldown', 0.3):.1f}s"
        )
        self.cooldown_label.pack(anchor="w", padx=20)
        
        self.cooldown_slider = ctk.CTkSlider(
            self.main_frame,
            from_=0.1,
            to=1.0,
            number_of_steps=18,
            command=self._on_cooldown_change
        )
        self.cooldown_slider.set(self.settings.get("click_cooldown", 0.3))
        self.cooldown_slider.pack(fill="x", padx=20, pady=(0, 10))
        
        # Scroll speed
        self.scroll_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Scroll Speed: {self.settings.get('scroll_speed', 5)}"
        )
        self.scroll_label.pack(anchor="w", padx=20)
        
        self.scroll_slider = ctk.CTkSlider(
            self.main_frame,
            from_=1,
            to=15,
            number_of_steps=14,
            command=self._on_scroll_change
        )
        self.scroll_slider.set(self.settings.get("scroll_speed", 5))
        self.scroll_slider.pack(fill="x", padx=20, pady=(0, 10))
        
        # ===== DISPLAY OPTIONS =====
        self._create_section_header("Display Options")
        
        options_frame = ctk.CTkFrame(self.main_frame)
        options_frame.pack(fill="x", padx=10, pady=5)
        
        self.show_fps_var = ctk.BooleanVar(value=self.settings.get("show_fps", True))
        fps_check = ctk.CTkCheckBox(
            options_frame,
            text="Show FPS",
            variable=self.show_fps_var,
            command=self._on_checkbox_change
        )
        fps_check.pack(anchor="w", padx=10, pady=5)
        
        self.show_landmarks_var = ctk.BooleanVar(value=self.settings.get("show_landmarks", True))
        landmarks_check = ctk.CTkCheckBox(
            options_frame,
            text="Show Landmarks",
            variable=self.show_landmarks_var,
            command=self._on_checkbox_change
        )
        landmarks_check.pack(anchor="w", padx=10, pady=5)
        
        self.eye_tracking_var = ctk.BooleanVar(value=self.settings.get("enable_eye_tracking", True))
        eye_check = ctk.CTkCheckBox(
            options_frame,
            text="Enable Eye Tracking",
            variable=self.eye_tracking_var,
            command=self._on_checkbox_change
        )
        eye_check.pack(anchor="w", padx=10, pady=5)
        
        # ===== ACTION BUTTONS =====
        self._create_section_header("Actions")
        
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save Settings",
            command=self._save_settings,
            fg_color="#28a745",
            hover_color="#218838"
        )
        save_btn.pack(side="left", padx=10, pady=10, expand=True)
        
        reset_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Reset to Defaults",
            command=self._reset_settings,
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        reset_btn.pack(side="right", padx=10, pady=10, expand=True)
        
        # Start app button
        start_btn = ctk.CTkButton(
            self.main_frame,
            text="▶️ Start Application",
            command=self._start_app,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            fg_color="#007bff",
            hover_color="#0056b3"
        )
        start_btn.pack(fill="x", padx=10, pady=20)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Ready",
            text_color="gray"
        )
        self.status_label.pack(pady=5)
        
    def _create_section_header(self, text: str):
        """Create a section header."""
        header = ctk.CTkLabel(
            self.main_frame,
            text=text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4da6ff"
        )
        header.pack(anchor="w", padx=10, pady=(15, 5))
        
        separator = ctk.CTkFrame(self.main_frame, height=2, fg_color="#4da6ff")
        separator.pack(fill="x", padx=10, pady=(0, 5))
    
    def _on_mode_change(self):
        """Handle control mode change."""
        self.settings["control_mode"] = self.mode_var.get()
        self._notify_change()
        self._update_status(f"Mode: {self.mode_var.get().upper()}")
    
    def _on_sensitivity_change(self, value: float):
        """Handle sensitivity slider change."""
        self.settings["cursor_sensitivity"] = value
        self.sensitivity_label.configure(text=f"Sensitivity: {value:.1f}")
        self._notify_change()
    
    def _on_smoothing_change(self, value: float):
        """Handle smoothing slider change."""
        self.settings["cursor_smoothing"] = value
        self.smoothing_label.configure(text=f"Smoothing: {value:.1%}")
        self._notify_change()
    
    def _on_pinch_change(self, value: float):
        """Handle pinch threshold change."""
        self.settings["pinch_threshold"] = int(value)
        self.pinch_label.configure(text=f"Pinch Threshold: {int(value)} px")
        self._notify_change()
    
    def _on_cooldown_change(self, value: float):
        """Handle click cooldown change."""
        self.settings["click_cooldown"] = value
        self.cooldown_label.configure(text=f"Click Cooldown: {value:.1f}s")
        self._notify_change()
    
    def _on_scroll_change(self, value: float):
        """Handle scroll speed change."""
        self.settings["scroll_speed"] = int(value)
        self.scroll_label.configure(text=f"Scroll Speed: {int(value)}")
        self._notify_change()
    
    def _on_checkbox_change(self):
        """Handle checkbox changes."""
        self.settings["show_fps"] = self.show_fps_var.get()
        self.settings["show_landmarks"] = self.show_landmarks_var.get()
        self.settings["enable_eye_tracking"] = self.eye_tracking_var.get()
        self._notify_change()
    
    def _notify_change(self):
        """Notify listener of settings change."""
        if self.on_settings_change:
            self.on_settings_change(self.settings)
    
    def _save_settings(self):
        """Save settings to config file."""
        if self.config_manager:
            for key, value in self.settings.items():
                self.config_manager.set(key, value)
            self.config_manager.save_settings()
            self._update_status("✅ Settings saved!")
        else:
            # Save directly to file
            config_path = Path(__file__).parent.parent / "config" / "settings.json"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(self.settings, f, indent=2)
            self._update_status("✅ Settings saved!")
    
    def _reset_settings(self):
        """Reset all settings to defaults."""
        self.settings = self._get_default_settings()
        
        # Update all sliders/checkboxes
        self.sensitivity_slider.set(self.settings["cursor_sensitivity"])
        self.smoothing_slider.set(self.settings["cursor_smoothing"])
        self.pinch_slider.set(self.settings["pinch_threshold"])
        self.cooldown_slider.set(self.settings["click_cooldown"])
        self.scroll_slider.set(self.settings["scroll_speed"])
        
        self.show_fps_var.set(self.settings["show_fps"])
        self.show_landmarks_var.set(self.settings["show_landmarks"])
        self.eye_tracking_var.set(self.settings["enable_eye_tracking"])
        self.mode_var.set(self.settings.get("control_mode", "hybrid"))
        
        # Update labels
        self._on_sensitivity_change(self.settings["cursor_sensitivity"])
        self._on_smoothing_change(self.settings["cursor_smoothing"])
        self._on_pinch_change(self.settings["pinch_threshold"])
        self._on_cooldown_change(self.settings["click_cooldown"])
        self._on_scroll_change(self.settings["scroll_speed"])
        
        self._update_status("🔄 Reset to defaults")
    
    def _start_app(self):
        """Save settings and start the main application."""
        self._save_settings()
        self._update_status("▶️ Starting application...")
        self.destroy()
    
    def _update_status(self, text: str):
        """Update status label."""
        self.status_label.configure(text=text)
        self.update()


def run_settings():
    """Run the settings GUI standalone."""
    app = SettingsWindow()
    app.mainloop()
    return app.settings


if __name__ == "__main__":
    settings = run_settings()
    print(f"Final settings: {settings}")
