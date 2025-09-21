import streamlit

from src import data_mgmt, navigation


def select_letter(letter: str) -> None:
    """Callback function for when a letter is selected"""
    streamlit.session_state.selected_letter = letter
    navigation.go_to_student_select()


def show_letter_select_page() -> None:
    """Display the letter selection page for returning students."""
    streamlit.title("Returning Student")
    streamlit.markdown("### What's the first letter of your first name?")

    # Get unique first letters from student names
    df = data_mgmt.load_student_data()
    first_letters = sorted(set([name[0].upper() for name in df["name"]]))

    # Create a grid of letter buttons
    cols = streamlit.columns(5)

    for i, letter in enumerate(first_letters):
        with cols[i % 5]:
            streamlit.button(
                letter,
                key=f"letter_{letter}",
                on_click=select_letter,
                args=(letter,),
                use_container_width=True,
            )

    streamlit.button("Back", on_click=navigation.go_to_welcome)
