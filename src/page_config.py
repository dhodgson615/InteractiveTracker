import streamlit


def set_page_configuration():
    """
    Set up the Streamlit page configuration.
    """
    streamlit.set_page_config(
        page_title="Student Lesson Tracker",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
