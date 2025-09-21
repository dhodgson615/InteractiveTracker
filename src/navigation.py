import datetime

import streamlit


def go_to_welcome() -> None:
    """Navigate back to the welcome page."""
    streamlit.session_state.page = "welcome"


def go_to_new_student() -> None:
    """Navigate to the new student registration page."""
    streamlit.session_state.page = "new_student"


def go_to_letter_select() -> None:
    """Navigate to the letter selection page for returning students."""
    streamlit.session_state.page = "letter_select"


def go_to_student_select() -> None:
    """Navigate to the student selection page based on the selected
    letter."""
    streamlit.session_state.page = "student_select"


def go_to_success(student_data: dict[str, str]) -> None:
    """Navigate to the success page after signing in a student."""
    streamlit.session_state.success_data = student_data
    streamlit.session_state.countdown_start = datetime.datetime.now()
    streamlit.session_state.page = "success"
