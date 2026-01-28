# Contributing to AI-Powered Hand & Eye Controlled HCI

Thank you for your interest in contributing to this project! 🎉

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

---

## 📜 Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to:
- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other contributors

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- Webcam for testing

### Fork and Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface.git
cd AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface
```

---

## 🤝 How to Contribute

### Types of Contributions

| Type | Description |
|------|-------------|
| 🐛 **Bug Reports** | Found a bug? Open an issue! |
| 💡 **Feature Requests** | Have an idea? We'd love to hear it! |
| 📝 **Documentation** | Help improve our docs |
| 🔧 **Code** | Submit bug fixes or new features |
| 🧪 **Testing** | Help test on different systems |

### Reporting Bugs

When reporting bugs, please include:
1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: How to trigger the bug
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **System Info**: OS, Python version, webcam type
6. **Screenshots/Logs**: If applicable

### Suggesting Features

For feature requests, please describe:
1. **Problem**: What problem does this solve?
2. **Solution**: Your proposed solution
3. **Alternatives**: Any alternatives considered
4. **Additional Context**: Any other relevant info

---

## 💻 Development Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install pytest  # For testing
```

### 3. Verify Setup
```bash
python -c "import cv2; import mediapipe; print('Setup complete!')"
```

### 4. Run the Application
```bash
python launcher.py
```

### 5. Run Tests
```bash
pytest tests/ -v
```

---

## 📏 Coding Standards

### Python Style Guide

We follow [PEP 8](https://peps.python.org/pep-0008/) with these specifics:

| Aspect | Convention |
|--------|------------|
| **Indentation** | 4 spaces (no tabs) |
| **Line Length** | Maximum 100 characters |
| **Imports** | Sorted, grouped (stdlib → third-party → local) |
| **Naming** | `snake_case` for functions/variables, `PascalCase` for classes |
| **Docstrings** | Google style |

### Docstring Example
```python
def process_frame(self, frame: np.ndarray) -> np.ndarray:
    """
    Process a video frame for hand detection.
    
    Args:
        frame: BGR image from webcam
        
    Returns:
        Processed frame with landmarks drawn
        
    Raises:
        ValueError: If frame is empty or invalid
    """
    pass
```

### Type Hints
Always use type hints for function parameters and return values:
```python
def calculate_distance(point1: Tuple[int, int], point2: Tuple[int, int]) -> float:
    """Calculate Euclidean distance between two points."""
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
```

---

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_gestures.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Writing Tests
- Place tests in `tests/` directory
- Name test files as `test_*.py`
- Name test functions as `test_*`
- Use fixtures for setup

### Test Example
```python
import pytest
from gesture_recognizer import GestureRecognizer, Gesture

class TestGestureRecognizer:
    @pytest.fixture
    def recognizer(self):
        return GestureRecognizer(pinch_threshold=40)
    
    def test_recognize_pinch(self, recognizer):
        landmarks = create_pinch_landmarks()
        assert recognizer.recognize(landmarks) == Gesture.PINCH
```

---

## 🔄 Pull Request Process

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes
- Write clean, documented code
- Add/update tests as needed
- Update documentation if applicable

### 3. Commit Changes
Use clear commit messages:
```bash
git commit -m "feat: add blink detection for eye tracker"
git commit -m "fix: resolve fail-safe error in mouse controller"
git commit -m "docs: update README with new gestures"
```

Commit message prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `test:` - Tests
- `refactor:` - Code refactoring
- `style:` - Formatting changes

### 4. Push and Create PR
```bash
git push origin feature/your-feature-name
```
Then open a Pull Request on GitHub.

### 5. PR Checklist
Before submitting, ensure:
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New code has tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] PR description explains changes

---

## 📞 Questions?

If you have questions, feel free to:
1. Open a [GitHub Issue](https://github.com/FAbdullah17/AI-Powered-Hand-and-EyeControlled-Human-Computer-Interface/issues)
2. Contact the team

---

Thank you for contributing! 🙏
