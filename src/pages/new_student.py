"""New student registration page."""

import streamlit

from ..page_manager import PageManager
from ..repository import StudentRepository


def show_new_student_page(page_manager: PageManager, repository: StudentRepository) -> None:
    """Display the new student registration page."""
    streamlit.title("New Student Registration")
    streamlit.markdown("### Welcome! Please enter your name")
    
    with streamlit.form("new_student_form"):
        new_name = streamlit.text_input("Full Name:")
        
        submitted = streamlit.form_submit_button(
            "Register", type="primary", use_container_width=True
        )
        
        if submitted and new_name:
            success, result = repository.add_new_student(new_name)
            
            if success:
                # result is a Student object
                page_manager.go_to_success(result.to_dict())
                streamlit.rerun()
            else:
                # result is an error message
                streamlit.error(result)
    
    streamlit.button("Back", on_click=page_manager.go_to_welcome)