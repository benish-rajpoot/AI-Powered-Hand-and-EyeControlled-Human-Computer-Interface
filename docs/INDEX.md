# 📚 Documentation Index

Welcome to the AI-Powered Hand & Eye Controlled HCI documentation.

---

## Quick Links

| Document | Description |
|----------|-------------|
| [📖 README](../README.md) | Project overview and quick start |
| [🚀 Installation](INSTALLATION.md) | Complete installation guide |
| [📘 User Guide](USER_GUIDE.md) | How to use the application |
| [❓ FAQ](FAQ.md) | Frequently asked questions |

---

## Documentation Files

### For Users

| File | Description |
|------|-------------|
| **[USER_GUIDE.md](USER_GUIDE.md)** | Complete user manual with gesture commands, keyboard shortcuts, and tips |
| **[INSTALLATION.md](INSTALLATION.md)** | Step-by-step installation for all methods |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Building executable and deploying to other computers |
| **[FAQ.md](FAQ.md)** | Common questions and answers |

### For Developers

| File | Description |
|------|-------------|
| **[TECHNICAL.md](TECHNICAL.md)** | Architecture, algorithms, and implementation details |
| **[API_REFERENCE.md](API_REFERENCE.md)** | Complete API documentation for all modules |
| **[CHANGELOG.md](CHANGELOG.md)** | Version history and changes |
| **[../CONTRIBUTING.md](../CONTRIBUTING.md)** | How to contribute to the project |

---

## Document Descriptions

### USER_GUIDE.md
Comprehensive user manual covering:
- Quick start instructions
- All 7 hand gestures with detailed instructions
- Eye tracking controls
- Control modes (hand/eye/hybrid)
- Keyboard shortcuts
- Settings configuration
- Troubleshooting tips

### INSTALLATION.md
Complete installation guide including:
- Quick install (executable)
- Python installation from source
- Development setup
- Dependency details
- Troubleshooting common issues
- System requirements

### DEPLOYMENT.md
Deployment instructions for:
- Creating standalone executable with PyInstaller
- Deploying to other computers
- Build scripts usage
- Target system requirements

### FAQ.md
Answers to common questions about:
- General usage
- Installation issues
- Performance optimization
- Eye tracking
- Gesture recognition
- Technical details

### TECHNICAL.md
In-depth technical documentation:
- System architecture diagrams
- MediaPipe configuration
- Gesture recognition algorithms
- Smoothing algorithms
- Performance optimization
- Error handling

### API_REFERENCE.md
Complete API documentation:
- HandTracker class
- EyeTracker class
- GestureRecognizer class
- MouseController class
- CalibrationManager class
- Logger utilities

### CHANGELOG.md
Version history documenting:
- Release notes
- New features
- Bug fixes
- Breaking changes
- Migration guides

---

## Quick Reference

### Gesture Commands
| Gesture | Action |
|---------|--------|
| ☝️ Point | Move cursor |
| 🤏 Pinch | Left click |
| 🤏🤏 Double Pinch | Double click |
| 🤏⏱️ Hold Pinch | Start drag |
| ✋ Open Palm | Right click |
| ✌️ Victory | Scroll mode |

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `h` | Hand mode |
| `e` | Eye mode |
| `b` | Hybrid mode |
| `q` | Quit |

### File Structure
```
docs/
├── INDEX.md          ← You are here
├── USER_GUIDE.md     ← User manual
├── INSTALLATION.md   ← Install guide
├── DEPLOYMENT.md     ← Build & deploy
├── FAQ.md            ← Common questions
├── TECHNICAL.md      ← Architecture
├── API_REFERENCE.md  ← API docs
└── CHANGELOG.md      ← Version history
```

---

## Getting Help

1. **Check FAQ**: Most common issues are covered
2. **Read User Guide**: Detailed usage instructions
3. **View Logs**: Check `logs/hci.log` for errors
4. **Open Issue**: Report bugs on GitHub

---

## Contributing to Documentation

Found an error or want to improve the docs?

1. Fork the repository
2. Edit the relevant `.md` file
3. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
