from streamlit import session_state

from footer import show_footer
from letter_select_page import show_letter_select_page
from new_student_page import show_new_student_page
from page_config import set_page_configuration
from student_select_page import show_student_select_page
from success_page import show_success_page
from welcome_page import show_welcome_page

set_page_configuration()

# Initialize session state for navigation
if "page" not in session_state:
    session_state.page = "welcome"
if "selected_letter" not in session_state:
    session_state.selected_letter = ""
if "success_data" not in session_state:
    session_state.success_data = None
if "countdown_start" not in session_state:
    session_state.countdown_start = None

# Render the correct page
if session_state.page == "welcome":
    show_welcome_page()
elif session_state.page == "new_student":
    show_new_student_page()
elif session_state.page == "letter_select":
    show_letter_select_page()
elif session_state.page == "student_select":
    show_student_select_page()
elif session_state.page == "success":
    show_success_page()

show_footer()
