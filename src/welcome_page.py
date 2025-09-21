import streamlit

from src import navigation


def show_welcome_page() -> None:
    """Display the welcome page with options for new and returning
    students.
    """
    streamlit.title("Lesson Sign-In")
    streamlit.markdown("### Welcome!")
    col1, col2 = streamlit.columns(2)

    with col1:
        streamlit.button(
            "New Student",
            on_click=navigation.go_to_new_student,
            type="primary",
            use_container_width=True,
        )

    with col2:
        streamlit.button(
            "Returning Student",
            on_click=navigation.go_to_letter_select,
            type="primary",
            use_container_width=True,
        )
