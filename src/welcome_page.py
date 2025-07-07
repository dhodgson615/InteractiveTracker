from streamlit import button, columns, markdown, title

from navigation import go_to_letter_select, go_to_new_student


def show_welcome_page():
    """
    Display the welcome page with options for new and returning
    students.
    """
    title("Lesson Sign-In")
    markdown("### Welcome!")

    col1, col2 = columns(2)
    with col1:
        button(
            "New Student",
            on_click=go_to_new_student,
            type="primary",
            use_container_width=True,
        )
    with col2:
        button(
            "Returning Student",
            on_click=go_to_letter_select,
            type="primary",
            use_container_width=True,
        )
