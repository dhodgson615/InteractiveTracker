from streamlit import (button, error, markdown, rerun, selectbox,
                       session_state, text_area, title, warning)

from data_mgmt import load_student_data, update_student_record
from navigation import go_to_letter_select, go_to_success


# Page: Student Select
def show_student_select_page():
    """
    Display the student selection page based on the selected letter.
    """
    title("Student Selection")

    # Safety check - if no letter is selected, go back to letter selection
    if not session_state.selected_letter:
        warning("No letter selected. Please select a letter first.")
        button("Back to Letter Selection", on_click=go_to_letter_select)
        return

    markdown(f"### Students with names starting with '{session_state.selected_letter}'")

    # Load student data
    df = load_student_data()

    # Make sure the DataFrame isn't empty and has the 'name' column
    if df.empty or "name" not in df.columns:
        warning("No student data available.")
        button("Back to Letter Selection", on_click=go_to_letter_select)
        return

    # Safe filtering - first remove any rows with missing names
    df_valid = df.dropna(subset=["name"])

    # Then filter by starting letter
    filtered_students = df_valid[df_valid["name"].astype(str).str.lower().str[0] == session_state.selected_letter.lower()]

    if filtered_students.empty:
        warning(f"No students found with names starting with '{session_state.selected_letter}'")
        button("Back to Letter Selection", on_click=go_to_letter_select)
        return

    # Rest of function continues as before
    student_names = filtered_students["name"].tolist()
    selected_student = selectbox("Please select your name:", student_names)

    note = text_area("Add a note (optional):", "")

    # Sign-in button
    if button("Sign In", type="primary", use_container_width=True):
        try:
            updated_record = update_student_record(selected_student, note)
            go_to_success(updated_record)
            rerun()
        except Exception as e:
            error(f"An error occurred: {e}")

    button("Back to Letter Selection", on_click=go_to_letter_select)
