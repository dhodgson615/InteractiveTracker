from streamlit import (button, error, form, form_submit_button, markdown,
                       rerun, text_input, title)

from data_mgmt import add_new_student
from navigation import go_to_success, go_to_welcome


def show_new_student_page():
    """
    Display the new student registration page.
    """
    title("New Student Registration")
    markdown("### Welcome! Please enter your name")

    with form("new_student_form"):
        new_name = text_input("Full Name:")
        submitted = form_submit_button("Register", type="primary", use_container_width=True)

        if submitted and new_name:
            success, result = add_new_student(new_name)
            if success:
                go_to_success(result)
                rerun()
            else:
                error(result)

    button("Back", on_click=go_to_welcome)
