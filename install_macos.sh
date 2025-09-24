#!/bin/bash
# Installation script for Interactive Tracker on macOS

set -e

echo "Installing Interactive Tracker for macOS..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

# Check Python version (require 3.8+)
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "Error: Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "Python $python_version detected - OK"

# Install required packages
echo "Installing Python dependencies..."
python3 -m pip install --user -r requirements.txt

# Check if tkinter is available
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "Warning: tkinter not found. On macOS, this is usually included with Python."
    echo "If you encounter issues, try reinstalling Python from python.org"
fi

echo "Installation complete!"
echo ""
echo "To run the Interactive Tracker:"
echo "1. Double-click on 'Interactive Tracker.app', or"
echo "2. Run: python3 run_gui.py"
echo ""
echo "Make sure you have a 'students.csv' file in the same directory."
echo "You can also specify the path in 'src/csvpath.txt'"