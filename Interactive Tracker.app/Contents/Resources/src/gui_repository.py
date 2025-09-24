"""Repository pattern for managing student data persistence (GUI version)."""

from __future__ import annotations

import os
import time
from typing import Optional

import pandas

from models import Student


class GUIStudentRepository:
    """Handles all student data persistence operations for GUI application."""

    def __init__(self) -> None:
        """Initialize the repository with CSV path configuration."""
        self._csv_path = self._get_csv_path()
        self._cache = None
        self._cache_time = 0
        self._cache_ttl = 5  # Cache for 5 seconds

    def _get_csv_path(self) -> str:
        """Read the CSV path from the csvpath.txt file."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path_file = os.path.join(script_dir, "csvpath.txt")

        try:
            with open(csv_path_file, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return "students.csv"  # Default path if file is not found

    def load_all_students(self) -> pandas.DataFrame:
        """Load all student data from CSV file with simple caching."""
        current_time = time.time()

        # Check if cache is still valid
        if (
            self._cache is not None
            and (current_time - self._cache_time) < self._cache_ttl
        ):
            return self._cache.copy()

        try:
            df = pandas.read_csv(self._csv_path)
            self._cache = df.copy()
            self._cache_time = current_time
            return df
        except FileNotFoundError:
            # Create empty dataframe with required columns if file doesn't exist
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
            df.to_csv(self._csv_path, index=False)
            self._cache = df.copy()
            self._cache_time = current_time
            return df

    def find_student_by_name(self, student_name: str) -> Optional[Student]:
        """Find a student by name and return Student object."""
        df = self.load_all_students()
        student_rows = df[df["name"] == student_name]

        if student_rows.empty:
            return None

        return Student.from_series(student_rows.iloc[0])

    def student_exists(self, student_name: str) -> bool:
        """Check if a student with the given name exists."""
        return self.find_student_by_name(student_name) is not None

    def save_student(self, student: Student) -> None:
        """Save or update a student record."""
        df = self.load_all_students()

        # Convert student to dict for DataFrame operations
        student_data = {
            "name": student.name,
            "frequency_per_week": student.frequency_per_week,
            "last_lesson_date": student.last_lesson_date,
            "lesson_number_taken_so_far": student.lesson_number_taken_so_far,
            "status": student.status,
            "is_online": student.is_online,
            "billing_cycle": student.billing_cycle,
            "note": student.note,
            "content": student.content,
        }

        # Check if student exists
        student_idx = df.index[df["name"] == student.name]

        if len(student_idx) > 0:
            # Update existing student
            for key, value in student_data.items():
                df.at[student_idx[0], key] = value
        else:
            # Add new student
            df = pandas.concat(
                [df, pandas.DataFrame([student_data])], ignore_index=True
            )

        # Save updated data back to CSV
        df.to_csv(self._csv_path, index=False)

        # Clear cache to ensure fresh data on next load
        self._clear_cache()

    def _clear_cache(self) -> None:
        """Clear the internal cache."""
        self._cache = None
        self._cache_time = 0

    def add_new_student(self, student_name: str) -> tuple[bool, str | Student]:
        """Add a new student to the repository."""
        if self.student_exists(student_name):
            return False, "Student already exists"

        # Create new student with default values
        new_student = Student(
            name=student_name,
            frequency_per_week=1,
            lesson_number_taken_so_far=1,  # Start with 1 since they're signing in
            status="New",
            is_online=False,
            billing_cycle="Monthly",  # Default to monthly billing
        )

        self.save_student(new_student)
        return True, new_student

    def update_student_lesson(
        self, student_name: str, note: str = ""
    ) -> Optional[Student]:
        """Update a student's lesson information."""
        student = self.find_student_by_name(student_name)
        if not student:
            raise ValueError(f"Student not found: {student_name}")

        student.increment_lesson()
        student.update_note(note)

        self.save_student(student)
        return student

    def get_students_by_first_letter(self, letter: str) -> list[Student]:
        """Get all students whose names start with the given letter."""
        df = self.load_all_students()

        # Filter out rows with missing names and filter by starting letter
        df_valid = df.dropna(subset=["name"])
        filtered_df = df_valid[
            df_valid["name"].astype(str).str.lower().str[0] == letter.lower()
        ]

        return [Student.from_series(row) for _, row in filtered_df.iterrows()]

    def get_unique_first_letters(self) -> list[str]:
        """Get sorted list of unique first letters from all student names."""
        df = self.load_all_students()
        if df.empty or "name" not in df.columns:
            return []

        df_valid = df.dropna(subset=["name"])
        first_letters = set(
            [name[0].upper() for name in df_valid["name"] if name]
        )
        return sorted(first_letters)
