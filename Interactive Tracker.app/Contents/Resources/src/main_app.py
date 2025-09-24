#!/usr/bin/env python3
"""Interactive Tracker - Student Lesson Sign-In Application (Native GUI)

A native macOS application for tracking student lessons using a modern GUI interface.
This application uses object-oriented patterns for better separation of
responsibility and clarity.
"""

import os
import sys

# Add the current directory to sys.path to allow importing from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui_application import GUIApplication


def main() -> None:
    """Main entry point for the native GUI application."""
    try:
        app = GUIApplication()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
