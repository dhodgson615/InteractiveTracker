import os
from datetime import datetime

from pandas import DataFrame, concat, read_csv
from streamlit import cache_data


def get_csv_path():
    """
    Read the CSV path from the csvpath.txt file. Returns the path as a
    string.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path_file = os.path.join(script_dir, "csvpath.txt")

    try:
        with open(csv_path_file, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        # Default path if a file is not found
        return "students.csv"


# Set the CSV path from the text file
CSV_PATH = get_csv_path()


@cache_data(ttl=5)  # Cache data for 5 seconds
def load_student_data():
    """
    Load student data from CSV file. If the file does not exist,
    create an empty DataFrame with the required columns.
    """
    try:
        return read_csv(CSV_PATH)
    except FileNotFoundError:
        # Create empty dataframe with required columns if the file doesn't exist
        df = DataFrame(
            columns=[
                "name",
                "frequency_per_week",
                "last_lesson_date",
                "lesson_number_taken_so_far",
                "status",
                "is_online",
                "billing_cycle",
                "note",
            ]
        )
        # Save the empty dataframe to create the file
        df.to_csv(CSV_PATH, index=False)
        return df


def update_student_record(student_name, note=""):
    """
    Update the student's record with the latest lesson information.
    Check if the billing threshold has been reached.
    """
    # Read current data
    df = read_csv(CSV_PATH)

    # Find the student and update their record
    student_index = df[df["name"] == student_name].index[0]

    # Increment lesson count
    df.at[student_index, "lesson_number_taken_so_far"] += 1

    # Update last lesson date
    df.at[student_index, "last_lesson_date"] = datetime.now().strftime("%Y-%m-%d")

    # Update note
    df.at[student_index, "note"] = note

    # Save updated data back to CSV
    df.to_csv(CSV_PATH, index=False)

    return df.loc[student_index]


def add_new_student(student_name):
    """
    Add a new student to the CSV file.
    """
    # Read current data
    try:
        df = read_csv(CSV_PATH)
    except FileNotFoundError:
        df = DataFrame(
            columns=[
                "name",
                "frequency_per_week",
                "last_lesson_date",
                "lesson_number_taken_so_far",
                "status",
                "is_online",
                "billing_cycle",
                "note",
            ]
        )

    # Check if the student already exists
    if student_name in df["name"].values:
        return False, "Student already exists"

    # Create new student record
    new_student = {
        "name": student_name,
        "frequency_per_week": 1,
        "last_lesson_date": datetime.now().strftime("%Y-%m-%d"),
        "lesson_number_taken_so_far": 1,
        "status": "New",
        "is_online": False,
        "billing_cycle": "Per Lesson",
        "note": "",
    }

    # Add to dataframe
    df = concat([df, DataFrame([new_student])], ignore_index=True)

    # Save updated data back to CSV
    df.to_csv(CSV_PATH, index=False)

    return True, df[df["name"] == student_name].iloc[0]
