import streamlit

from src import data_mgmt, navigation


def show_student_select_page() -> None:
    """Display the student selection page based on the selected
    letter.
    """
    streamlit.title("Student Selection")

    # Safety check - if no letter is selected, go back to letter selection
    if not streamlit.session_state.selected_letter:
        streamlit.warning("No letter selected. Please select a letter first.")

        streamlit.button(
            "Back to Letter Selection", on_click=navigation.go_to_letter_select
        )

        return

    streamlit.markdown(
        f"### Students with names starting with "
        f"'{streamlit.session_state.selected_letter}'"
    )

    # Load student data
    df = data_mgmt.load_student_data()

    # Make sure the DataFrame isn't empty and has the 'name' column
    if df.empty or "name" not in df.columns:
        streamlit.warning("No student data available.")

        streamlit.button(
            "Back to Letter Selection", on_click=navigation.go_to_letter_select
        )

        return

    # Safe filtering - first remove any rows with missing names
    df_valid = df.dropna(subset=["name"])

    # Then filter by starting letter
    filtered_students = df_valid[
        df_valid["name"].astype(str).str.lower().str[0]
        == streamlit.session_state.selected_letter.lower()
    ]

    if filtered_students.empty:
        streamlit.warning(
            f"No students found with names starting with "
            f"'{streamlit.session_state.selected_letter}'"
        )

        streamlit.button(
            "Back to Letter Selection", on_click=navigation.go_to_letter_select
        )

        return

    student_names = filtered_students["name"].tolist()

    selected_student = streamlit.selectbox(
        "Please select your name:", student_names
    )

    note = streamlit.text_area("Add a note (optional):", "")

    # Sign-in button
    if streamlit.button("Sign In", type="primary", use_container_width=True):
        try:
            updated_record = data_mgmt.update_student_record(
                selected_student, note
            )

            navigation.go_to_success(
                {str(k): str(v) for k, v in updated_record.to_dict().items()}
            )

            streamlit.rerun()

        except Exception as e:
            streamlit.error(f"An error occurred: {e}")

    streamlit.button(
        "Back to Letter Selection", on_click=navigation.go_to_letter_select
    )
