"""Core models for the Interactive Tracker application."""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:
    """Represents a student with all their lesson and billing information."""

    name: str
    frequency_per_week: int = 1
    last_lesson_date: str = ""
    lesson_number_taken_so_far: int = 0
    status: str = "New"
    is_online: bool = False

    billing_cycle: str = (
        "Monthly"  # Changed default from "Per Lesson" to "Monthly"
    )

    note: str = ""
    content: str = ""

    def __post_init__(self) -> None:
        """Initialize default values after creation."""
        if not self.last_lesson_date:
            self.last_lesson_date = datetime.datetime.now().strftime(
                "%Y-%m-%d"
            )

    def increment_lesson(self) -> None:
        """Increment the lesson count and update the last lesson date."""
        self.lesson_number_taken_so_far += 1
        self.last_lesson_date = datetime.datetime.now().strftime("%Y-%m-%d")

    def get_billing_message(self) -> Optional[str]:
        """Calculate and return the appropriate billing message based on billing cycle."""
        if self.billing_cycle == "Per Lesson":
            return "Payment due for this lesson"

        elif (
            self.billing_cycle == "Monthly"
            and self.lesson_number_taken_so_far > 4
        ):
            return "Monthly billing cycle completed (4 lessons)"

        elif (
            self.billing_cycle == "Quarterly"
            and self.lesson_number_taken_so_far > 12
        ):

            return "Quarterly billing cycle completed (12 lessons)"

        return None

    def update_note(self, note: str) -> None:
        """Update the student's note."""
        self.note = note

    def to_dict(self) -> dict[str, str]:
        """Convert student to dictionary format for session state."""
        billing_message = self.get_billing_message()

        result = {
            "name": self.name,
            "frequency_per_week": str(self.frequency_per_week),
            "last_lesson_date": self.last_lesson_date,
            "lesson_number_taken_so_far": str(self.lesson_number_taken_so_far),
            "status": self.status,
            "is_online": str(self.is_online),
            "billing_cycle": self.billing_cycle,
            "note": self.note,
            "content": self.content,
        }

        if billing_message:
            result["billing_message"] = billing_message

        return result

    @classmethod
    def from_series(cls, series) -> Student:
        """Create a Student from a pandas Series."""
        return cls(
            name=str(series["name"]),
            frequency_per_week=int(series["frequency_per_week"]),
            last_lesson_date=str(series["last_lesson_date"]),
            lesson_number_taken_so_far=int(
                series["lesson_number_taken_so_far"]
            ),
            status=str(series["status"]),
            is_online=bool(series["is_online"]),
            billing_cycle=str(series["billing_cycle"]),
            note=str(series["note"]) if series["note"] else "",
            content=str(series["content"]) if series["content"] else "",
        )
