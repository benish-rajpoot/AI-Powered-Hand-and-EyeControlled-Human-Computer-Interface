# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2024-01-25

### 🎉 Initial Release

The first stable release of the AI-Powered Hand & Eye Controlled Human-Computer Interface.

### Added

#### Core Features
- **Hand Tracking**: Real-time 21-landmark hand detection using MediaPipe
- **Eye Tracking**: 468-point face mesh with iris tracking for gaze estimation
- **Gesture Recognition**: 7 distinct gestures for complete mouse control
  - Point (cursor movement)
  - Pinch (left click)
  - Double Pinch (double click)
  - Hold Pinch (drag start)
  - Open Palm (right click)
  - Victory (scroll mode)
  - Fist (no action)

#### Control Modes
- **Hand-only mode**: Pure hand gesture control
- **Eye-only mode**: Cursor follows eye gaze
- **Hybrid mode**: Combined hand and eye control with automatic switching

#### User Interface
- **Settings GUI**: Modern dark-themed CustomTkinter interface
  - Sensitivity slider (0.5-3.0)
  - Smoothing slider (0-90%)
  - Pinch threshold adjustment
  - Click cooldown control
  - Scroll speed setting
  - Display options toggles

#### Technical Features
- **ROI-based mapping**: Active zone for precise cursor control
- **Advanced smoothing**: Position history with weighted moving average
- **Fail-safe protection**: Prevents cursor corner issues
- **Persistent settings**: JSON-based configuration
- **Logging system**: Color-coded console and file logging

#### Deployment
- **Standalone executable**: Single .exe file via PyInstaller
- **Build scripts**: Automated build process with `build.bat`
- **Quick launch**: `run.bat` for easy starting

#### Documentation
- Comprehensive README
- User Guide
- Technical Documentation
- API Reference
- FAQ
- Deployment Guide
- Contributing Guidelines

#### Testing
- 21 unit tests for core modules
- Gesture recognition tests
- Mouse controller tests
- Calibration manager tests

### Known Issues
- Eye tracking accuracy varies with lighting conditions
- High CPU usage on lower-end hardware
- Requires MediaPipe 0.10.9 (newer versions have API changes)

---

## [Unreleased]

### Planned Features
- [ ] Blink-to-click functionality
- [ ] Voice command integration
- [ ] Custom gesture macros
- [ ] Calibration wizard
- [ ] User profile management
- [ ] GPU acceleration support
- [ ] macOS/Linux support

### Improvements Under Consideration
- [ ] Reduced memory footprint
- [ ] Lower latency processing
- [ ] Multi-language support
- [ ] Accessibility improvements
- [ ] Tutorial mode for new users

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2024-01-25 | Initial stable release |

---

## Migration Guide

### Upgrading to 1.0.0
If you had an earlier development version:

1. **Backup settings**: Copy `config/settings.json`
2. **Install new version**: Follow installation instructions
3. **Restore settings**: Copy back your settings file
4. **Verify**: Run the application and test all features

### Breaking Changes
None (initial release)

---

## Contributors

- Sundas Safder (079884)
- Benish Batool (079888)
- Pakiza Imran (079889)

### Supervisor
Sir Marsad Akbar

### Institution
University of Punjab, Faculty of Computing & Information Technology
