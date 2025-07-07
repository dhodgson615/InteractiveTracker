import time
from datetime import datetime

from streamlit import markdown, rerun, session_state, success, title

from navigation import go_to_welcome


def show_success_page():
    """
    Display the success page after signing in a student.
    """
    title("Successful Sign-In")

    if session_state.success_data is None:
        # If no data, go back to welcome
        go_to_welcome()
        rerun()

    student_name = session_state.success_data["name"]
    lesson_number = session_state.success_data["lesson_number_taken_so_far"]

    success(f"Thank you, {student_name}! You've been signed in for lesson #{lesson_number}.")

    # Show student information
    markdown(f"**Lesson frequency:** {session_state.success_data['frequency_per_week']} per week")
    markdown(f"**Billing cycle:** {session_state.success_data['billing_cycle']}")

    # Calculate remaining time
    elapsed = (datetime.now() - session_state.countdown_start).total_seconds()
    remaining = 5 - elapsed

    markdown(f"Returning to welcome screen in **{int(remaining + 1)}** seconds...")

    # When time is up, redirect to welcome
    if remaining <= 0:
        session_state.success_data = None
        go_to_welcome()
        rerun()
    else:
        time.sleep(0.1)  # Small delay to prevent too many reruns
        rerun()
