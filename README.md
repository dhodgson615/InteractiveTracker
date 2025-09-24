# InteractiveTracker

A **native Swift macOS application** for tracking student lessons and managing lesson sign-ins.

## Features

- **Native macOS App**: Beautiful, truly native GUI using AppKit/Cocoa
- **Student Management**: Add new students and track returning students
- **Lesson Tracking**: Automatic lesson counting and date tracking
- **Billing Integration**: Multiple billing cycles (Monthly, Quarterly, Per Lesson)
- **Letter-based Navigation**: Quick student lookup by first letter
- **CSV Data Storage**: Simple, portable data storage format in Documents folder
- **Zero Dependencies**: Self-contained macOS application bundle

## Installation & Usage

### Xcode Project (Recommended for Development)

1. Open `InteractiveTrackerXcode/InteractiveTracker.xcodeproj` in Xcode
2. Build and run (⌘+R) 
3. The app will create a `students.csv` file in your Documents folder automatically

### Swift Package (Console Testing)

```bash
cd InteractiveTrackerSwift
swift run
```

### Pre-built App (Coming Soon)

A pre-built `.app` bundle will be available for download in future releases.

## Usage

1. **New Students**: Click "New Student" to register a new student
2. **Returning Students**: Click "Returning Student", then select the first letter of the student's name
3. **Sign In**: Select the student and optionally add a note, then click "Sign In"
4. **Success**: View lesson information and billing details

The application automatically manages CSV data storage in your Documents folder with the format:

```csv
name,frequency_per_week,last_lesson_date,lesson_number_taken_so_far,status,is_online,billing_cycle,note,content
John Doe,2,2023-10-01,5,active,yes,monthly,Out of town next week,
Jane Smith,1,2023-10-02,3,inactive,no,yearly,Needs to reschedule,
```

## Architecture

The Swift application uses modern macOS development patterns:

- **AppDelegate**: Manages application lifecycle and window creation
- **MainViewController**: Handles UI navigation and page display
- **Student**: Data model representing student information
- **StudentRepository**: Manages CSV file persistence in Documents folder
- **Pages**: Individual UI pages for different app functions

## Requirements

- **macOS**: 10.13 or later
- **Xcode**: For development and building
- **No Runtime Dependencies**: Self-contained Swift application

## Project Structure

```
InteractiveTrackerXcode/              # Native macOS Xcode project
├── InteractiveTracker.xcodeproj/     # Xcode project file
└── InteractiveTracker/               # Swift source code
    ├── AppDelegate.swift             # App lifecycle management
    ├── MainViewController.swift      # Main UI controller
    ├── MainViewController+Pages.swift # Page implementations
    ├── Student.swift                 # Data model
    ├── StudentRepository.swift       # CSV persistence
    └── Assets.xcassets              # App icons and colors

InteractiveTrackerSwift/              # Swift Package for testing
├── Package.swift                     # Package configuration
└── Sources/InteractiveTracker/       # Shared Swift code

legacy/                               # Legacy Python implementation
└── (Original Python/tkinter code - not maintained)
```

## Legacy Python Version

The original Python/tkinter implementation has been moved to the `legacy/` directory and is **no longer maintained**. The Swift version provides superior performance, native macOS integration, and requires no external dependencies.

For details about the conversion from Python to Swift, see [SWIFT_CONVERSION_SUMMARY.md](SWIFT_CONVERSION_SUMMARY.md).
