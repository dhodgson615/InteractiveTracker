"""Footer component for the application."""

import streamlit


def show_footer() -> None:
    """Display the footer with version information."""
    streamlit.markdown("---")
    streamlit.caption("Student Lesson Tracker v1.0")
    streamlit.caption("Created by Dylan Hodgson")
