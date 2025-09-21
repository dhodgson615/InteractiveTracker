import streamlit

from src import data_mgmt, navigation


def show_new_student_page() -> None:
    """Display the new student registration page."""
    streamlit.title("New Student Registration")
    streamlit.markdown("### Welcome! Please enter your name")

    with streamlit.form("new_student_form"):
        new_name = streamlit.text_input("Full Name:")

        submitted = streamlit.form_submit_button(
            "Register", type="primary", use_container_width=True
        )

        if submitted and new_name:
            success, result = data_mgmt.add_new_student(new_name)

            if success:
                if hasattr(result, "to_dict"):
                    navigation.go_to_success(
                        {str(k): str(v) for k, v in result.to_dict().items()}
                    )

                else:
                    navigation.go_to_success({})

                streamlit.rerun()

            else:
                streamlit.error(result)


streamlit.button("Back", on_click=navigation.go_to_welcome)
