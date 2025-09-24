# Interactive Tracker - Native Swift macOS Application

A native macOS application for tracking student lessons, built using Swift and AppKit.

## Features

- **Native macOS Interface**: Built with AppKit/Cocoa for true macOS experience
- **Student Management**: Add new students and track returning students
- **Letter-based Navigation**: Quick student lookup by first letter of name
- **Lesson Tracking**: Automatic lesson counting and date tracking
- **CSV Data Persistence**: Stores data in CSV format in Documents folder
- **Billing Cycles**: Support for Monthly, Quarterly, and Per Lesson billing
- **Note Taking**: Add optional notes when students sign in
- **Auto-return**: Success page automatically returns to welcome after 5 seconds

## Requirements

- **macOS**: 10.15 (Catalina) or later
- **Xcode**: 14.0 or later
- **Swift**: 5.0 or later

## Installation & Usage

### Quick Setup (Recommended)

Run the automated setup script from the repository root:
```bash
./setup_xcode.sh
```

This script will:
- Verify Xcode installation and version
- Check project structure and Swift source files
- Build the project to validate setup
- Provide next steps for development

### Option 1: Xcode Project

1. Open `InteractiveTracker.xcodeproj` in Xcode
2. Build and run the project (⌘+R)
3. The app will create a `students.csv` file in your Documents folder

### Option 2: Build from Command Line

```bash
# Build the project
xcodebuild -project InteractiveTracker.xcodeproj -scheme InteractiveTracker -configuration Release build

# Run the built app
open build/Release/InteractiveTracker.app
```

## Project Structure

```
InteractiveTracker.xcodeproj/
├── InteractiveTracker/
│   ├── AppDelegate.swift              # Application delegate
│   ├── MainViewController.swift       # Main view controller
│   ├── MainViewController+Pages.swift # Page implementations
│   ├── Student.swift                  # Student data model
│   ├── StudentRepository.swift        # CSV data persistence
│   ├── Assets.xcassets               # App icons and colors
│   └── Info.plist                    # App configuration
```

## Architecture

### Clean Architecture with Native Components

- **AppDelegate**: Manages application lifecycle and window creation
- **MainViewController**: Handles UI navigation and page display
- **Student**: Data model representing student information
- **StudentRepository**: Manages CSV file persistence in Documents folder
- **Pages**: Individual UI pages for different app functions

### Data Flow

1. **Welcome Page**: Choose between new or returning student
2. **New Student**: Register new student with name validation
3. **Letter Selection**: Choose first letter of returning student's name
4. **Student Selection**: Pick specific student and add optional note
5. **Success Page**: Display confirmation with lesson details and countdown

## CSV File Format

The application stores student data in `~/Documents/students.csv`:

```csv
name,frequency_per_week,last_lesson_date,lesson_number_taken_so_far,status,is_online,billing_cycle,note,content
John Doe,2,2023-10-01,5,active,yes,Monthly,Test note,
Jane Smith,1,2023-10-02,3,active,no,Quarterly,Another note,
```

## Building for Distribution

To create a distributable app:

1. **Archive**: Product → Archive in Xcode
2. **Export**: Choose "Export" and select distribution method
3. **Notarization**: For distribution outside Mac App Store, enable notarization

## Differences from Python Version

### Advantages of Native Swift Version

- **True Native Experience**: Uses AppKit for authentic macOS look and feel
- **Better Performance**: Compiled Swift code runs faster than interpreted Python
- **System Integration**: Proper macOS app bundle, dock integration, native alerts
- **No Dependencies**: No need to install Python or additional packages
- **Memory Efficient**: Lower memory footprint than Python/tkinter version
- **Distribution**: Easier to distribute as a single .app bundle

### Technical Improvements

- **Proper Error Handling**: Uses Swift's Result type for robust error handling
- **Memory Management**: Automatic Reference Counting prevents memory leaks
- **Type Safety**: Swift's strong typing prevents common runtime errors
- **Modern Concurrency**: Uses proper Timer and async patterns
- **Native UI Components**: Real NSButton, NSTextField, NSStackView components

## Development

To modify the application:

1. Open in Xcode
2. Make changes to Swift files
3. Build and test (⌘+R)
4. Use Xcode's Interface Builder for UI changes if needed

The application uses programmatic UI (no Storyboards) for better version control and flexibility.

## Testing

The application includes comprehensive error handling:

- **Input Validation**: Checks for empty names and invalid selections
- **File Handling**: Creates CSV file if missing, handles read/write errors
- **State Management**: Prevents invalid navigation states
- **UI Feedback**: Native alert dialogs for user feedback

## Deployment

For deployment to other Macs:

1. **Code Signing**: Configure signing certificate in Xcode
2. **Archive & Export**: Use Xcode's organizer
3. **Notarization**: Required for distribution outside Mac App Store
4. **DMG Creation**: Use tools like create-dmg for installer creation

This native Swift version provides the best possible macOS experience while maintaining all functionality from the original Python application.