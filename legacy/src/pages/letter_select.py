"""Letter selection page for returning students."""

import streamlit

from page_manager import PageManager
from repository import StudentRepository


def select_letter(page_manager: PageManager, letter: str) -> None:
    """Callback function for when a letter is selected."""
    page_manager.set_selected_letter(letter)
    page_manager.go_to_student_select()


def show_letter_select_page(
    page_manager: PageManager, repository: StudentRepository
) -> None:
    """Display the letter selection page for returning students."""
    streamlit.title("Returning Student")
    streamlit.markdown("### What's the first letter of your first name?")

    # Get unique first letters from student names
    first_letters = repository.get_unique_first_letters()

    if not first_letters:
        streamlit.warning("No students found in the system.")
        streamlit.button("Back", on_click=page_manager.go_to_welcome)
        return

    # Create a grid of letter buttons
    cols = streamlit.columns(5)

    for i, letter in enumerate(first_letters):
        with cols[i % 5]:
            streamlit.button(
                letter,
                key=f"letter_{letter}",
                on_click=select_letter,
                args=(page_manager, letter),
                use_container_width=True,
            )

    streamlit.button("Back", on_click=page_manager.go_to_welcome)
