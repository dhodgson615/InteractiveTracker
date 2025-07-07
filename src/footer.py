from streamlit import caption, markdown


def show_footer():
    """
    Display the footer with version information.
    """
    markdown("---")
    caption("Student Lesson Tracker v1.0")
    caption("Created by Dylan Hodgson")
