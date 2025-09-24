"""Page navigation and state management for the application."""

from __future__ import annotations

import datetime
from typing import Optional

import streamlit


class PageManager:
    """Manages page navigation and session state for the application."""

    # Page constants
    WELCOME = "welcome"
    NEW_STUDENT = "new_student"
    LETTER_SELECT = "letter_select"
    STUDENT_SELECT = "student_select"
    SUCCESS = "success"

    def __init__(self) -> None:
        """Initialize the page manager and set up session state."""
        self._initialize_session_state()

    def _initialize_session_state(self) -> None:
        """Initialize all required session state variables."""
        if "page" not in streamlit.session_state:
            streamlit.session_state.page = self.WELCOME

        if "selected_letter" not in streamlit.session_state:
            streamlit.session_state.selected_letter = ""

        if "success_data" not in streamlit.session_state:
            streamlit.session_state.success_data = None

        if "countdown_start" not in streamlit.session_state:
            streamlit.session_state.countdown_start = None

    @property
    def current_page(self) -> str:
        """Get the current page."""
        return streamlit.session_state.page

    @property
    def selected_letter(self) -> str:
        """Get the currently selected letter."""
        return streamlit.session_state.selected_letter

    @property
    def success_data(self) -> Optional[dict]:
        """Get the success page data."""
        return streamlit.session_state.success_data

    @property
    def countdown_start(self) -> Optional[datetime.datetime]:
        """Get the countdown start time."""
        return streamlit.session_state.countdown_start

    def go_to_welcome(self) -> None:
        """Navigate to the welcome page."""
        streamlit.session_state.page = self.WELCOME

    def go_to_new_student(self) -> None:
        """Navigate to the new student registration page."""
        streamlit.session_state.page = self.NEW_STUDENT

    def go_to_letter_select(self) -> None:
        """Navigate to the letter selection page for returning students."""
        streamlit.session_state.page = self.LETTER_SELECT

    def go_to_student_select(self) -> None:
        """Navigate to the student selection page."""
        streamlit.session_state.page = self.STUDENT_SELECT

    def go_to_success(self, student_data: dict[str, str]) -> None:
        """Navigate to the success page with student data."""
        streamlit.session_state.success_data = student_data
        streamlit.session_state.countdown_start = datetime.datetime.now()
        streamlit.session_state.page = self.SUCCESS

    def set_selected_letter(self, letter: str) -> None:
        """Set the selected letter for student filtering."""
        streamlit.session_state.selected_letter = letter

    def clear_success_data(self) -> None:
        """Clear the success page data."""
        streamlit.session_state.success_data = None
        streamlit.session_state.countdown_start = None
