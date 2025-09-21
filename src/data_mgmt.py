from __future__ import annotations

import datetime
import os
import typing

import pandas
import streamlit


def get_csv_path() -> str:
    """Read the CSV path from the csvpath.txt file. Returns the path as
    a string.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path_file = os.path.join(script_dir, "csvpath.txt")

    try:
        with open(csv_path_file, "r") as file:
            return file.read().strip()

    except FileNotFoundError:
        return "students.csv"  # Default path if a file is not found


# Set the CSV path from the text file
CSV_PATH = get_csv_path()


@streamlit.cache_data(ttl=5)  # Cache data for 5 seconds
def load_student_data() -> pandas.DataFrame:
    """Load student data from CSV file. If the file does not exist,
    create an empty DataFrame with the required columns.
    """
    try:
        return pandas.read_csv(CSV_PATH)

    except FileNotFoundError:
        # Create empty dataframe with required columns
        # if the file doesn't exist
        df = pandas.DataFrame(
            columns=[
                "name",
                "frequency_per_week",
                "last_lesson_date",
                "lesson_number_taken_so_far",
                "status",
                "is_online",
                "billing_cycle",
                "note",
                "content",
            ]
        )

        # Save the empty dataframe to create the file
        df.to_csv(CSV_PATH, index=False)

        return df


def update_student_record(
    student_name: str, note: str = ""
) -> pandas.Series[typing.Any] | pandas.DataFrame:
    """Update the student's record with the latest lesson information.
    Check if the billing threshold has been reached.
    """
    # Read current data
    df = pandas.read_csv(CSV_PATH)

    # Find the student and update their record
    student_index = df[df["name"] == student_name].index[0]

    # Increment lesson count
    df.at[student_index, "lesson_number_taken_so_far"] += 1
    current_lesson = df.at[student_index, "lesson_number_taken_so_far"]

    # TODO: Test this more thoroughly
    ##########################################################################

    billing_cycle = df.at[student_index, "billing_cycle"]
    # frequency = df.at[student_index, "frequency_per_week"]

    # Check billing cycle thresholds
    billing_message = None

    if billing_cycle == "Per Lesson":
        billing_message = "Payment due for this lesson"
        # TODO: don't send message for single lesson

    elif billing_cycle == "Monthly" and current_lesson > 4:
        billing_message = "Monthly billing cycle completed (4 lessons)"

    elif billing_cycle == "Quarterly" and current_lesson > 12:
        billing_message = "Quarterly billing cycle completed (12 lessons)"

    print(f"Billing message: {billing_message}")
    # TODO: Send this as a message with shortcuts CLI
    ##########################################################################

    # Update last lesson date
    df.at[student_index, "last_lesson_date"] = (
        datetime.datetime.now().strftime("%Y-%m-%d")
    )

    # Update note
    df.at[student_index, "note"] = note

    # Save updated data back to CSV
    df.to_csv(CSV_PATH, index=False)

    # Return both student record and billing message
    student_record = df.loc[student_index].copy()
    student_record["billing_message"] = billing_message

    return student_record


def add_new_student(
    student_name: str,
) -> tuple[bool, str] | tuple[bool, pandas.Series[typing.Any]]:
    """Add a new student to the CSV file."""
    try:
        df = pandas.read_csv(CSV_PATH)

    except FileNotFoundError:
        df = pandas.DataFrame(
            columns=[
                "name",
                "frequency_per_week",
                "last_lesson_date",
                "lesson_number_taken_so_far",
                "status",
                "is_online",
                "billing_cycle",
                "note",
                "content",
            ]
        )

    # Check if the student already exists
    if student_name in df["name"].values:
        return False, "Student already exists"

    # Create new student record
    new_student = {
        "name": student_name,
        "frequency_per_week": 1,
        "last_lesson_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "lesson_number_taken_so_far": 1,
        "status": "New",
        "is_online": False,
        "billing_cycle": "Per Lesson",  # TODO: change to monthly by default
        "note": "",
        "content": "",
    }

    # Add to dataframe
    df = pandas.concat(
        [df, pandas.DataFrame([new_student])], ignore_index=True
    )

    df.to_csv(CSV_PATH, index=False)  # Save updated data back to CSV

    return True, df[df["name"] == student_name].iloc[0]
