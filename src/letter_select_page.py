from streamlit import button, columns, markdown, session_state, title

from data_mgmt import load_student_data
from navigation import go_to_student_select, go_to_welcome


def select_letter(letter):
    """Callback function for when a letter is selected"""
    session_state.selected_letter = letter
    go_to_student_select()


def show_letter_select_page():
    """
    Display the letter selection page for returning students.
    """
    title("Returning Student")
    markdown("### What's the first letter of your first name?")

    # Get unique first letters from student names
    df = load_student_data()
    first_letters = sorted(set([name[0].upper() for name in df["name"]]))

    # Create a grid of letter buttons
    cols = columns(5)
    for i, letter in enumerate(first_letters):
        with cols[i % 5]:
            button(
                letter,
                key=f"letter_{letter}",
                on_click=select_letter,
                args=(letter,),
                use_container_width=True
            )

    button("Back", on_click=go_to_welcome)