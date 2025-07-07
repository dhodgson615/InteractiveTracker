from datetime import datetime

from streamlit import session_state


def go_to_welcome():
    """
    Navigate back to the welcome page.
    """
    session_state.page = "welcome"


def go_to_new_student():
    """
    Navigate to the new student registration page.
    """
    session_state.page = "new_student"


def go_to_letter_select():
    """
    Navigate to the letter selection page for returning students.
    """
    session_state.page = "letter_select"


def go_to_student_select():
    """
    Navigate to the student selection page based on the selected
    letter.
    """
    session_state.page = "student_select"


def go_to_success(student_data):
    """
    Navigate to the success page after signing in a student.
    """
    session_state.success_data = student_data
    session_state.countdown_start = datetime.now()
    session_state.page = "success"
