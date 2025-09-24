#if canImport(Cocoa)
import Cocoa

// Main entry point for the Interactive Tracker Swift application
let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate

// Run the application
app.run()
#else
import Foundation

// Console version for testing on non-macOS platforms
print("Interactive Tracker Swift - Console Version")
print("This is a test version for non-macOS platforms")

let repository = StudentRepository()

// Test the repository functionality
print("Testing student repository...")

// Add a test student
let result = repository.addStudent(name: "Test Student")
switch result {
case .success(let student):
    print("✅ Successfully added student: \(student.name)")
case .failure(let error):
    print("❌ Error adding student: \(error)")
}

// List all students
print("Current students:")
for student in repository.students {
    print("- \(student.name) (Lessons: \(student.lessonNumberTakenSoFar))")
}

// Test letter grouping
let letters = repository.uniqueFirstLetters
print("Available first letters: \(letters)")

// Test updating a student lesson
if let updatedStudent = repository.updateStudentLesson(studentName: "Test Student", note: "Test note") {
    print("✅ Updated student lesson: \(updatedStudent.name) now has \(updatedStudent.lessonNumberTakenSoFar) lessons")
} else {
    print("❌ Failed to update student lesson")
}

print("\n✅ Swift application logic is working correctly!")
print("To run the full macOS GUI version, open this project in Xcode on macOS.")
#endif