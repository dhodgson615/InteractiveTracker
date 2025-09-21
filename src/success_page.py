import datetime
import time

import streamlit

from src import navigation


def show_success_page() -> None:
    """Display the success page after signing in a student."""
    streamlit.title("Successful Sign-In")

    if streamlit.session_state.success_data is None:
        navigation.go_to_welcome()
        streamlit.rerun()

    student_name = streamlit.session_state.success_data["name"]

    lesson_number = streamlit.session_state.success_data[
        "lesson_number_taken_so_far"
    ]

    streamlit.success(
        f"Thank you, {student_name}! You've been signed in for lesson #"
        f"{lesson_number}."
    )

    streamlit.markdown(
        f"**Lesson frequency:** "
        f"{streamlit.session_state.success_data['frequency_per_week']} "
        f"per week"
    )

    streamlit.markdown(
        f"**Billing cycle:** "
        f"{streamlit.session_state.success_data['billing_cycle']}"
    )

    # Calculate remaining time
    elapsed = (
        datetime.datetime.now() - streamlit.session_state.countdown_start
    ).total_seconds()

    remaining = 5 - elapsed

    streamlit.markdown(
        f"Returning to welcome screen in **{int(remaining + 1)}** seconds..."
    )

    # When time is up, redirect to welcome
    if remaining <= 0:
        streamlit.session_state.success_data = None
        navigation.go_to_welcome()
        streamlit.rerun()

    else:
        time.sleep(0.1)  # Small delay to prevent too many reruns
        streamlit.rerun()
