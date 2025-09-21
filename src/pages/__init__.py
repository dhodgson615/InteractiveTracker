"""Page display functions for the Interactive Tracker application."""

from .welcome import show_welcome_page
from .new_student import show_new_student_page
from .letter_select import show_letter_select_page
from .student_select import show_student_select_page
from .success import show_success_page
from .footer import show_footer

__all__ = [
    "show_welcome_page",
    "show_new_student_page", 
    "show_letter_select_page",
    "show_student_select_page",
    "show_success_page",
    "show_footer",
]