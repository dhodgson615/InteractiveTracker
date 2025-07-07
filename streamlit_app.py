import time
from datetime import datetime

from streamlit import (button, caption, columns, error, form,
                       form_submit_button, markdown, rerun, selectbox,
                       session_state, success, text_area, text_input, title,
                       warning)

from data_mgmt import add_new_student, load_student_data, update_student_record
from navigation import (go_to_letter_select, go_to_new_student,
                        go_to_student_select, go_to_success, go_to_welcome)
from page_config import set_page_configuration


set_page_configuration()

# Initialize session state for navigation
if "page" not in session_state:
    session_state.page = "welcome"
if "selected_letter" not in session_state:
    session_state.selected_letter = ""
if "success_data" not in session_state:
    session_state.success_data = None
if "countdown_start" not in session_state:
    session_state.countdown_start = None


# Page: Welcome
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


# Page: New Student
def show_new_student_page():
    """
    Display the new student registration page.
    """
    title("New Student Registration")
    markdown("### Welcome! Please enter your name")

    with form("new_student_form"):
        new_name = text_input("Full Name:")
        submitted = form_submit_button("Register", type="primary", use_container_width=True)

        if submitted and new_name:
            success, result = add_new_student(new_name)
            if success:
                go_to_success(result)
                rerun()
            else:
                error(result)

    button("Back", on_click=go_to_welcome)


# Page: Letter Select
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
            if button(letter, key=f"letter_{letter}", use_container_width=True):
                session_state.selected_letter = letter
                go_to_student_select()

    button("Back", on_click=go_to_welcome)


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


# Success page
def show_success_page():
    """
    Display the success page after signing in a student.
    """
    title("Successful Sign-In")

    if session_state.success_data is None:
        # If no data, go back to welcome
        go_to_welcome()
        rerun()
        return

    student_name = session_state.success_data["name"]
    lesson_number = session_state.success_data["lesson_number_taken_so_far"]

    success(f"Thank you, {student_name}! You've been signed in for lesson #{lesson_number}.")

    # Show student information
    markdown(f"**Lesson frequency:** {session_state.success_data['frequency_per_week']} per week")
    markdown(f"**Billing cycle:** {session_state.success_data['billing_cycle']}")

    # Calculate remaining time
    elapsed = (datetime.now() - session_state.countdown_start).total_seconds()
    remaining = 5 - elapsed

    # Show countdown
    markdown(f"Returning to welcome screen in **{int(remaining + 1)}** seconds...")

    # If time is up, redirect to welcome
    if remaining <= 0:
        session_state.success_data = None
        go_to_welcome()
        rerun()
    else:
        time.sleep(0.1)  # Small delay to prevent too many reruns
        rerun()


# Render the appropriate page
if session_state.page == "welcome":
    show_welcome_page()
elif session_state.page == "new_student":
    show_new_student_page()
elif session_state.page == "letter_select":
    show_letter_select_page()
elif session_state.page == "student_select":
    show_student_select_page()
elif session_state.page == "success":
    show_success_page()

markdown("---")
caption("Student Lesson Tracker v1.0")
caption("Created by Dylan Hodgson")
