import Foundation

/// Represents a student with all their lesson and billing information
struct Student: Codable, Identifiable {
    var id = UUID()
    var name: String
    var frequencyPerWeek: Int = 1
    var lastLessonDate: String = ""
    var lessonNumberTakenSoFar: Int = 0
    var status: String = "New"
    var isOnline: Bool = false
    var billingCycle: String = "Monthly"
    var note: String = ""
    var content: String = ""
    
    // Computed property for CSV header
    static let csvHeader = "name,frequency_per_week,last_lesson_date,lesson_number_taken_so_far,status,is_online,billing_cycle,note,content"
    
    /// Initialize with default values
    init(name: String) {
        self.name = name
        self.lastLessonDate = Self.currentDateString()
    }
    
    /// Initialize from CSV row
    init?(csvRow: String) {
        let components = csvRow.components(separatedBy: ",")
        guard components.count >= 8 else { return nil }
        
        self.name = components[0]
        self.frequencyPerWeek = Int(components[1]) ?? 1
        self.lastLessonDate = components[2]
        self.lessonNumberTakenSoFar = Int(components[3]) ?? 0
        self.status = components[4]
        self.isOnline = components[5].lowercased() == "yes" || components[5].lowercased() == "true"
        self.billingCycle = components[6]
        self.note = components.count > 7 ? components[7] : ""
        self.content = components.count > 8 ? components[8] : ""
    }
    
    /// Convert to CSV row
    var csvRow: String {
        let onlineStr = isOnline ? "yes" : "no"
        return "\(name),\(frequencyPerWeek),\(lastLessonDate),\(lessonNumberTakenSoFar),\(status),\(onlineStr),\(billingCycle),\(note),\(content)"
    }
    
    /// Increment lesson count and update date
    mutating func incrementLesson() {
        lessonNumberTakenSoFar += 1
        lastLessonDate = Self.currentDateString()
    }
    
    /// Update student note
    mutating func updateNote(_ newNote: String) {
        note = newNote
    }
    
    /// Get billing message based on billing cycle
    var billingMessage: String? {
        switch billingCycle {
        case "Per Lesson":
            return "Payment due for this lesson"
        case "Monthly" where lessonNumberTakenSoFar > 4:
            return "Monthly billing cycle completed (4 lessons)"
        case "Quarterly" where lessonNumberTakenSoFar > 12:
            return "Quarterly billing cycle completed (12 lessons)"
        default:
            return nil
        }
    }
    
    /// Get current date as string
    private static func currentDateString() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.string(from: Date())
    }
}