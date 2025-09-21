"""Interactive Tracker - Student Lesson Sign-In Application

This application uses object-oriented patterns for better separation of 
responsibility and clarity.
"""

import sys
import os

# Add the parent directory to sys.path to allow importing from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from application import Application


def main() -> None:
    """Main entry point for the application."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
else:
    # When run by streamlit, directly execute main
    main()
