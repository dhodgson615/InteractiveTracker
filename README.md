# InteractiveTracker

A native macOS application for tracking student lessons and managing lesson sign-ins.

## Features

- **Native macOS App**: Beautiful, native GUI using tkinter with macOS-optimized styling
- **Student Management**: Add new students and track returning students
- **Lesson Tracking**: Automatic lesson counting and date tracking
- **Billing Integration**: Multiple billing cycles (Monthly, Quarterly, Per Lesson)
- **Letter-based Navigation**: Quick student lookup by first letter
- **CSV Data Storage**: Simple, portable data storage format

## Installation

### Option 1: Quick Install (Recommended)

1. Run the installation script:
   ```bash
   ./install_macos.sh
   ```

2. Double-click on `Interactive Tracker.app` to launch

### Option 2: Manual Install

1. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python3 run_gui.py
   ```

## Usage

### First Time Setup

1. Ensure you have a `students.csv` file in the same directory, or create one with the following format:

```csv
name,frequency_per_week,last_lesson_date,lesson_number_taken_so_far,status,is_online,billing_cycle,note,content
John Doe,2,2023-10-01,5,active,yes,monthly,Out of town next week,
Jane Smith,1,2023-10-02,3,inactive,no,yearly,Needs to reschedule,
```

2. You can also specify a custom CSV path by editing `src/csvpath.txt` with the path to your CSV file.

### Using the App

1. **New Students**: Click "New Student" to register a new student
2. **Returning Students**: Click "Returning Student", then select the first letter of the student's name
3. **Sign In**: Select the student and optionally add a note, then click "Sign In"
4. **Success**: View lesson information and billing details

## Development

### Web Version (Legacy)

The original Streamlit web version is still available:

```bash
streamlit run src/streamlit_app.py
```

### Architecture

The application uses object-oriented design patterns:

- **Application Controller**: Manages the overall app flow
- **Page Manager**: Handles navigation and state management  
- **Student Repository**: Manages data persistence to CSV
- **Student Model**: Encapsulates student data and behavior

## Requirements

- **macOS**: 10.13 or later
- **Python**: 3.8 or later
- **Dependencies**: pandas (automatically installed)

## File Structure

```
Interactive Tracker.app/          # macOS application bundle
├── Contents/
│   ├── Info.plist               # App metadata
│   ├── MacOS/
│   │   └── Interactive Tracker  # Launch script
│   └── Resources/
│       ├── src/                 # Application source code
│       └── students.csv         # Student data
```
