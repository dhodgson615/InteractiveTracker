import Foundation

/// Error types for student repository operations
enum StudentRepositoryError: Error {
    case studentAlreadyExists
    case studentNotFound
    case fileError(String)
}

/// Handles all student data persistence operations using CSV files
class StudentRepository {
    var students: [Student] = []
    private let csvFileName = "students.csv"
    private var csvURL: URL {
        let documentsPath = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
        return documentsPath.appendingPathComponent(csvFileName)
    }
    
    init() {
        loadStudents()
    }
    
    /// Load all students from CSV file
    func loadStudents() {
        guard FileManager.default.fileExists(atPath: csvURL.path) else {
            // Create empty CSV file with header if it doesn't exist
            createEmptyCSV()
            return
        }
        
        do {
            let csvContent = try String(contentsOf: csvURL)
            let lines = csvContent.components(separatedBy: .newlines)
            
            // Skip header and empty lines
            students = lines.dropFirst().compactMap { line in
                guard !line.trimmingCharacters(in: .whitespaces).isEmpty else { return nil }
                return Student(csvRow: line)
            }
        } catch {
            print("Error loading students: \(error)")
            createEmptyCSV()
        }
    }
    
    /// Save all students to CSV file
    func saveStudents() {
        var csvContent = Student.csvHeader + "\n"
        for student in students {
            csvContent += student.csvRow + "\n"
        }
        
        do {
            try csvContent.write(to: csvURL, atomically: true, encoding: .utf8)
        } catch {
            print("Error saving students: \(error)")
        }
    }
    
    /// Create empty CSV file with header
    private func createEmptyCSV() {
        do {
            try Student.csvHeader.write(to: csvURL, atomically: true, encoding: .utf8)
            students = []
        } catch {
            print("Error creating empty CSV: \(error)")
        }
    }
    
    /// Add a new student
    func addStudent(name: String) -> Result<Student, StudentRepositoryError> {
        // Check if student already exists
        if students.contains(where: { $0.name.lowercased() == name.lowercased() }) {
            return .failure(.studentAlreadyExists)
        }
        
        var newStudent = Student(name: name)
        newStudent.lessonNumberTakenSoFar = 1 // Start with 1 since they're signing in
        
        students.append(newStudent)
        saveStudents()
        
        return .success(newStudent)
    }
    
    /// Update student lesson
    func updateStudentLesson(studentName: String, note: String = "") -> Student? {
        guard let index = students.firstIndex(where: { $0.name == studentName }) else {
            return nil
        }
        
        students[index].incrementLesson()
        students[index].updateNote(note)
        saveStudents()
        
        return students[index]
    }
    
    /// Find student by name
    func findStudent(name: String) -> Student? {
        return students.first { $0.name.lowercased() == name.lowercased() }
    }
    
    /// Get students whose names start with the given letter
    func studentsStartingWith(letter: String) -> [Student] {
        return students.filter { 
            $0.name.lowercased().hasPrefix(letter.lowercased()) 
        }.sorted { $0.name < $1.name }
    }
    
    /// Get unique first letters from all student names
    var uniqueFirstLetters: [String] {
        let letters = Set(students.compactMap { student in
            student.name.first?.uppercased()
        })
        return Array(letters).sorted()
    }
    
    /// Check if student exists
    func studentExists(name: String) -> Bool {
        return students.contains { $0.name.lowercased() == name.lowercased() }
    }
}