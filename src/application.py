"""Main application controller for the Interactive Tracker."""

from __future__ import annotations

import streamlit

from .models import Student
from .page_manager import PageManager
from .repository import StudentRepository
from . import pages


class Application:
    """Main application controller that coordinates all components."""
    
    def __init__(self) -> None:
        """Initialize the application with all required components."""
        self.page_manager = PageManager()
        self.student_repository = StudentRepository()
        
        # Initialize page configuration
        self._configure_page()
    
    def _configure_page(self) -> None:
        """Set up the Streamlit page configuration."""
        streamlit.set_page_config(
            page_title="Student Lesson Tracker",
            layout="centered",
            initial_sidebar_state="collapsed",
        )
    
    def run(self) -> None:
        """Main application entry point that handles page routing."""
        current_page = self.page_manager.current_page
        
        if current_page == PageManager.WELCOME:
            self._show_welcome_page()
        elif current_page == PageManager.NEW_STUDENT:
            self._show_new_student_page()
        elif current_page == PageManager.LETTER_SELECT:
            self._show_letter_select_page()
        elif current_page == PageManager.STUDENT_SELECT:
            self._show_student_select_page()
        elif current_page == PageManager.SUCCESS:
            self._show_success_page()
        
        # Show footer on all pages
        self._show_footer()
    
    def _show_welcome_page(self) -> None:
        """Display the welcome page."""
        pages.show_welcome_page(self.page_manager)
    
    def _show_new_student_page(self) -> None:
        """Display the new student registration page."""
        pages.show_new_student_page(self.page_manager, self.student_repository)
    
    def _show_letter_select_page(self) -> None:
        """Display the letter selection page."""
        pages.show_letter_select_page(self.page_manager, self.student_repository)
    
    def _show_student_select_page(self) -> None:
        """Display the student selection page."""
        pages.show_student_select_page(self.page_manager, self.student_repository)
    
    def _show_success_page(self) -> None:
        """Display the success page."""
        pages.show_success_page(self.page_manager)
    
    def _show_footer(self) -> None:
        """Display the application footer."""
        pages.show_footer()