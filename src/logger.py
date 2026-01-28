"""
Logger Utility

Provides consistent logging across the application.
Logs to both console and file for debugging.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class HCILogger:
    """
    Centralized logging for the HCI application.
    
    Features:
    - Console output with color coding
    - File logging for debugging
    - Performance metrics logging
    """
    
    # ANSI color codes for console
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    _instance: Optional['HCILogger'] = None
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(
        self,
        name: str = "HCI",
        log_file: Optional[str] = None,
        level: int = logging.INFO
    ):
        """
        Initialize the logger.
        
        Args:
            name: Logger name
            log_file: Optional path to log file
            level: Logging level
        """
        if self._initialized:
            return
            
        self._initialized = True
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.handlers = []  # Clear any existing handlers
        
        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_formatter = self._ColoredFormatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (optional)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        
        # Performance metrics
        self._perf_samples = []
        self._last_fps_time = datetime.now()
    
    class _ColoredFormatter(logging.Formatter):
        """Custom formatter with color support."""
        
        def format(self, record):
            colors = HCILogger.COLORS
            levelname = record.levelname
            if levelname in colors:
                record.levelname = f"{colors[levelname]}{levelname}{colors['RESET']}"
            return super().format(record)
    
    def debug(self, msg: str):
        """Log debug message."""
        self.logger.debug(msg)
    
    def info(self, msg: str):
        """Log info message."""
        self.logger.info(msg)
    
    def warning(self, msg: str):
        """Log warning message."""
        self.logger.warning(msg)
    
    def error(self, msg: str):
        """Log error message."""
        self.logger.error(msg)
    
    def critical(self, msg: str):
        """Log critical message."""
        self.logger.critical(msg)
    
    def log_fps(self, fps: float):
        """Log FPS metric."""
        self._perf_samples.append(fps)
        
        # Log average every 5 seconds
        now = datetime.now()
        if (now - self._last_fps_time).seconds >= 5:
            if self._perf_samples:
                avg_fps = sum(self._perf_samples) / len(self._perf_samples)
                self.debug(f"Average FPS: {avg_fps:.1f}")
                self._perf_samples.clear()
            self._last_fps_time = now
    
    def log_gesture(self, gesture: str):
        """Log gesture detection."""
        self.debug(f"Gesture detected: {gesture}")
    
    def log_mode_change(self, mode: str):
        """Log control mode change."""
        self.info(f"Control mode changed to: {mode.upper()}")
    
    def log_startup(self):
        """Log application startup."""
        self.info("=" * 40)
        self.info("HCI Application Starting")
        self.info("=" * 40)
    
    def log_shutdown(self):
        """Log application shutdown."""
        self.info("=" * 40)
        self.info("HCI Application Closed")
        self.info("=" * 40)


# Global logger instance
def get_logger(
    name: str = "HCI",
    log_file: Optional[str] = None,
    level: int = logging.INFO
) -> HCILogger:
    """Get or create the global logger instance."""
    return HCILogger(name, log_file, level)
