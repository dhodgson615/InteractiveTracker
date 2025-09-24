"""Page navigation and state management for the GUI application."""

from __future__ import annotations

import datetime
from typing import Optional


class GUIPageManager:
    """Manages page navigation and session state for the GUI
    application.
    """

    # Page constants
    WELCOME = "welcome"
    NEW_STUDENT = "new_student"
    LETTER_SELECT = "letter_select"
    STUDENT_SELECT = "student_select"
    SUCCESS = "success"

    def __init__(self) -> None:
        """Initialize the page manager and set up state."""
        self._current_page = self.WELCOME
        self._selected_letter = ""
        self._success_data: Optional[dict] = None
        self._countdown_start: Optional[datetime.datetime] = None

    @property
    def current_page(self) -> str:
        """Get the current page."""
        return self._current_page

    @property
    def selected_letter(self) -> str:
        """Get the currently selected letter."""
        return self._selected_letter

    @property
    def success_data(self) -> Optional[dict]:
        """Get the success page data."""
        return self._success_data

    @property
    def countdown_start(self) -> Optional[datetime.datetime]:
        """Get the countdown start time."""
        return self._countdown_start

    def go_to_welcome(self) -> None:
        """Navigate to the welcome page."""
        self._current_page = self.WELCOME

    def go_to_new_student(self) -> None:
        """Navigate to the new student registration page."""
        self._current_page = self.NEW_STUDENT

    def go_to_letter_select(self) -> None:
        """Navigate to the letter selection page for returning students."""
        self._current_page = self.LETTER_SELECT

    def go_to_student_select(self) -> None:
        """Navigate to the student selection page."""
        self._current_page = self.STUDENT_SELECT

    def go_to_success(self, student_data: dict[str, str]) -> None:
        """Navigate to the success page with student data."""
        self._success_data = student_data
        self._countdown_start = datetime.datetime.now()
        self._current_page = self.SUCCESS

    def set_selected_letter(self, letter: str) -> None:
        """Set the selected letter for student filtering."""
        self._selected_letter = letter

    def clear_success_data(self) -> None:
        """Clear the success page data."""
        self._success_data = None
        self._countdown_start = None
