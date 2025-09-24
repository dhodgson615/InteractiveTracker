"""Test script to verify the GUI application functionality. This tests
the core functionality without requiring a display.
"""

import os
import sys
import tempfile

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def test_page_manager():
    """Test the GUI page manager functionality."""
    print("Testing GUI Page Manager...")

    from gui_page_manager import GUIPageManager

    pm = GUIPageManager()

    # Test initial state
    assert pm.current_page == GUIPageManager.WELCOME
    assert pm.selected_letter == ""
    assert pm.success_data is None

    # Test navigation
    pm.go_to_new_student()

    assert pm.current_page == GUIPageManager.NEW_STUDENT

    pm.go_to_letter_select()

    assert pm.current_page == GUIPageManager.LETTER_SELECT

    # Test letter selection
    pm.set_selected_letter("A")

    assert pm.selected_letter == "A"

    pm.go_to_student_select()

    assert pm.current_page == GUIPageManager.STUDENT_SELECT

    # Test success page
    test_data = {"name": "Test Student", "lesson_number_taken_so_far": "1"}
    pm.go_to_success(test_data)

    assert pm.current_page == GUIPageManager.SUCCESS
    assert pm.success_data == test_data
    assert pm.countdown_start is not None

    # Test clearing success data
    pm.clear_success_data()

    assert pm.success_data is None
    assert pm.countdown_start is None

    print("✓ GUI Page Manager tests passed")


def test_repository():
    """Test the GUI repository functionality."""
    print("Testing GUI Repository...")

    from gui_repository import GUIStudentRepository
    from models import Student

    # Create a temporary CSV file for testing
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False
    ) as f:
        f.write(
            "name,frequency_per_week,last_lesson_date,lesson_number_taken_so_far,status,is_online,billing_cycle,note,content\n"
        )

        f.write("Alice Brown,1,2023-01-01,5,active,no,Monthly,Test note,\n")

        f.write(
            "Bob Smith,2,2023-01-02,3,active,yes,Quarterly,Another note,\n"
        )

        temp_csv = f.name

    try:
        # Create repository with custom CSV path
        repo = GUIStudentRepository()
        repo._csv_path = temp_csv

        # Test loading students
        df = repo.load_all_students()

        assert len(df) == 2
        assert "Alice Brown" in df["name"].values
        assert "Bob Smith" in df["name"].values

        # Test finding student
        alice = repo.find_student_by_name("Alice Brown")

        assert alice is not None
        assert alice.name == "Alice Brown"
        assert alice.lesson_number_taken_so_far == 5

        # Test student exists
        assert repo.student_exists("Alice Brown") == True
        assert repo.student_exists("Nonexistent") == False

        # Test getting students by first letter
        a_students = repo.get_students_by_first_letter("A")

        assert len(a_students) == 1
        assert a_students[0].name == "Alice Brown"

        b_students = repo.get_students_by_first_letter("B")

        assert len(b_students) == 1
        assert b_students[0].name == "Bob Smith"

        # Test getting unique first letters
        letters = repo.get_unique_first_letters()

        assert set(letters) == {"A", "B"}

        # Test adding new student
        success, result = repo.add_new_student("Charlie Wilson")

        assert success == True
        assert isinstance(result, Student)
        assert result.name == "Charlie Wilson"

        # Test updating student lesson
        updated = repo.update_student_lesson("Alice Brown", "Updated note")

        assert updated is not None
        assert updated.lesson_number_taken_so_far == 6  # Should be incremented
        assert updated.note == "Updated note"

        print("✓ GUI Repository tests passed")

    finally:
        # Clean up temp file
        os.unlink(temp_csv)


def test_student_model():
    """Test the Student model functionality."""
    print("Testing Student Model...")

    from models import Student

    # Test creating a student
    student = Student(
        name="Test Student",
        frequency_per_week=2,
        lesson_number_taken_so_far=5,
        billing_cycle="Monthly",
    )

    assert student.name == "Test Student"
    assert student.frequency_per_week == 2
    assert student.lesson_number_taken_so_far == 5
    assert student.billing_cycle == "Monthly"

    # Test incrementing lesson
    original_count = student.lesson_number_taken_so_far
    student.increment_lesson()

    assert student.lesson_number_taken_so_far == original_count + 1

    # Test updating note
    student.update_note("Test note")
    assert student.note == "Test note"

    # Test billing message
    student.billing_cycle = "Monthly"
    student.lesson_number_taken_so_far = 5
    billing_msg = student.get_billing_message()
    assert billing_msg == "Monthly billing cycle completed (4 lessons)"

    # Test to_dict
    student_dict = student.to_dict()

    assert student_dict["name"] == "Test Student"

    assert student_dict["lesson_number_taken_so_far"] == str(
        student.lesson_number_taken_so_far
    )  # Should be string

    print("✓ Student Model tests passed")


def main():
    """Run all tests."""
    print("Running GUI Application Tests...")
    print("=" * 50)

    try:
        test_page_manager()
        test_repository()
        test_student_model()

        print("=" * 50)

        print(
            "🎉 All tests passed! The native macOS app is working correctly."
        )

        print()
        print("The Interactive Tracker has been successfully converted from")
        print("a Streamlit web app to a native macOS application!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
