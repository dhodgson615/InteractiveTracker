"""Student selection page for returning students."""

import streamlit

from page_manager import PageManager
from repository import StudentRepository


def show_student_select_page(page_manager: PageManager, repository: StudentRepository) -> None:
    """Display the student selection page based on the selected letter."""
    streamlit.title("Student Selection")
    
    # Safety check - if no letter is selected, go back to letter selection
    if not page_manager.selected_letter:
        streamlit.warning("No letter selected. Please select a letter first.")
        streamlit.button(
            "Back to Letter Selection", on_click=page_manager.go_to_letter_select
        )
        return
    
    streamlit.markdown(
        f"### Students with names starting with '{page_manager.selected_letter}'"
    )
    
    # Get students filtered by the selected letter
    students = repository.get_students_by_first_letter(page_manager.selected_letter)
    
    if not students:
        streamlit.warning(
            f"No students found with names starting with "
            f"'{page_manager.selected_letter}'"
        )
        streamlit.button(
            "Back to Letter Selection", on_click=page_manager.go_to_letter_select
        )
        return
    
    # Create selectbox with student names
    student_names = [student.name for student in students]
    selected_student_name = streamlit.selectbox(
        "Please select your name:", student_names
    )
    
    note = streamlit.text_area("Add a note (optional):", "")
    
    # Sign-in button
    if streamlit.button("Sign In", type="primary", use_container_width=True):
        try:
            updated_student = repository.update_student_lesson(
                selected_student_name, note
            )
            
            if updated_student:
                page_manager.go_to_success(updated_student.to_dict())
                streamlit.rerun()
                
        except Exception as e:
            streamlit.error(f"An error occurred: {e}")
    
    streamlit.button(
        "Back to Letter Selection", on_click=page_manager.go_to_letter_select
    )