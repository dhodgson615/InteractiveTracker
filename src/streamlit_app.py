"""Interactive Tracker - Student Lesson Sign-In Application

This application uses object-oriented patterns for better separation of 
responsibility and clarity.
"""

from src.application import Application


def main() -> None:
    """Main entry point for the application."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()

"""TODO: Add shortcuts command to get the Streamlit link and save it to
clipboard, flip the Focus mode across iCloud devices, make iPad have an
automation to open the URL based on the Focus mode."""

# Configure it so that the default student pays monthly
# and the default lesson frequency is 1 per week.
# Make it send the student a message when the bill is due.
