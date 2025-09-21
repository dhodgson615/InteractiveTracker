import streamlit

from src import (footer, letter_select_page, new_student_page, page_config,
                 student_select_page, success_page, welcome_page)

page_config.set_page_configuration()

# Initialize session state for navigation
if "page" not in streamlit.session_state:
    streamlit.session_state.page = "welcome"

if "selected_letter" not in streamlit.session_state:
    streamlit.session_state.selected_letter = ""

if "success_data" not in streamlit.session_state:
    streamlit.session_state.success_data = None

if "countdown_start" not in streamlit.session_state:
    streamlit.session_state.countdown_start = None

# Render the correct page
if streamlit.session_state.page == "welcome":
    welcome_page.show_welcome_page()

elif streamlit.session_state.page == "new_student":
    new_student_page.show_new_student_page()

elif streamlit.session_state.page == "letter_select":
    letter_select_page.show_letter_select_page()

elif streamlit.session_state.page == "student_select":
    student_select_page.show_student_select_page()

elif streamlit.session_state.page == "success":
    success_page.show_success_page()

footer.show_footer()

"""TODO: Add shortcuts command to get the Streamlit link and save it to
clipboard, flip the Focus mode across iCloud devices, make iPad have an
automation to open the URL based on the Focus mode."""

# Configure it so that the default student pays monthly
# and the default lesson frequency is 1 per week.
# Make it send the student a message when the bill is due.
