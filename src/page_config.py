from streamlit import set_page_config


def set_page_configuration():
    """
    Set up the Streamlit page configuration.
    """
    set_page_config(
        page_title="Student Lesson Tracker",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
