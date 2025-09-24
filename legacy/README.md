# Legacy Python Implementation

This directory contains the original Python/tkinter and Streamlit implementations of the Interactive Tracker application. **This code is no longer maintained and should not be used.**

## What's Here

- `src/` - Original Python source code with tkinter GUI and Streamlit web interface
- `Interactive Tracker.app/` - Legacy macOS app bundle using Python/tkinter
- `run_gui.py` - Original Python GUI launcher
- `test_gui_functionality.py` - Tests for the Python implementation
- `requirements.txt` - Python dependencies
- `create_app_icon.py` - App icon generation script
- `install_macos.sh` - Legacy installation script

## Migration to Swift

The entire application has been rewritten in Swift using native macOS frameworks:

- **Native macOS App**: `/InteractiveTrackerXcode/` - Complete Xcode project
- **Console Version**: `/InteractiveTrackerSwift/` - Swift Package for testing
- **Full Feature Parity**: All functionality preserved in native Swift
- **Better Performance**: Compiled code, native UI components, lower memory usage
- **No Dependencies**: Self-contained macOS application

## Important Notes

- ❌ **Do not use this legacy code** - it is preserved only for reference
- ❌ **No maintenance** - bugs will not be fixed in the Python version
- ❌ **No interaction** - this code does not interact with the Swift version
- ✅ **Use the Swift version** - located in the root directory

For the current Swift implementation, see the main README.md in the root directory.