#!/bin/bash
# Setup script for Interactive Tracker Xcode Development Environment
# This script sets up everything needed to develop the Swift macOS application
#
# What this script does:
# - Verifies macOS and Xcode installation
# - Checks project structure and Swift source files
# - Builds the project to validate everything works
# - Creates the app bundle for testing
# - Provides clear next steps for development

set -e

# Show help if requested
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Interactive Tracker Xcode Environment Setup"
    echo ""
    echo "Usage: $0"
    echo ""
    echo "This script sets up the Xcode development environment for the Interactive Tracker Swift macOS application."
    echo ""
    echo "Requirements:"
    echo "  - macOS"
    echo "  - Xcode (available from Mac App Store or Apple Developer)"
    echo ""
    echo "What this script does:"
    echo "  - Verifies macOS and Xcode installation"
    echo "  - Checks project structure and Swift source files"
    echo "  - Builds the project to validate everything works"
    echo "  - Creates the app bundle for testing"
    echo "  - Provides clear next steps for development"
    echo ""
    exit 0
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project paths
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
XCODE_PROJECT_DIR="$REPO_ROOT/InteractiveTrackerXcode"
XCODE_PROJECT="$XCODE_PROJECT_DIR/InteractiveTracker.xcodeproj"
BUILD_DIR="$XCODE_PROJECT_DIR/build"

echo -e "${BLUE}=== Interactive Tracker Xcode Environment Setup ===${NC}"
echo ""

# Function to print status messages
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS only."
    print_info "The Interactive Tracker native Swift app requires macOS and Xcode."
    exit 1
fi

# Get macOS version for compatibility check
MACOS_VERSION=$(sw_vers -productVersion)
print_info "macOS version: $MACOS_VERSION"

# Check minimum macOS version (10.13)
if [[ $(echo "$MACOS_VERSION 10.13" | tr ' ' '\n' | sort -V | head -n1) != "10.13" ]]; then
    print_warning "macOS 10.13 or later is recommended for the best experience"
fi

# Check for Xcode installation
if ! command -v xcodebuild &> /dev/null; then
    print_error "Xcode is not installed or xcodebuild is not in PATH."
    echo ""
    print_info "Please install Xcode from:"
    echo "  1. Mac App Store: https://apps.apple.com/us/app/xcode/id497799835"
    echo "  2. Apple Developer: https://developer.apple.com/xcode/"
    echo ""
    print_info "After installation, run:"
    echo "  sudo xcode-select --install"
    echo "  sudo xcode-select -s /Applications/Xcode.app/Contents/Developer"
    exit 1
fi

print_status "Xcode is installed"

# Check Xcode version
XCODE_VERSION=$(xcodebuild -version | head -n 1 | sed 's/Xcode //')
print_info "Xcode version: $XCODE_VERSION"

# Check Swift version
if command -v swift &> /dev/null; then
    SWIFT_VERSION=$(swift --version | head -n 1)
    print_status "Swift is available: $SWIFT_VERSION"
else
    print_warning "Swift command line tools not found"
    print_info "This is usually included with Xcode, but you may need to install command line tools:"
    echo "  xcode-select --install"
fi

# Verify project structure
echo ""
print_info "Verifying project structure..."

if [[ ! -d "$XCODE_PROJECT_DIR" ]]; then
    print_error "Xcode project directory not found: $XCODE_PROJECT_DIR"
    exit 1
fi

if [[ ! -d "$XCODE_PROJECT" ]]; then
    print_error "Xcode project not found: $XCODE_PROJECT"
    exit 1
fi

# Also verify the project.pbxproj file exists
if [[ ! -f "$XCODE_PROJECT/project.pbxproj" ]]; then
    print_error "Xcode project.pbxproj file not found: $XCODE_PROJECT/project.pbxproj"
    exit 1
fi

print_status "Project structure verified"

# List Swift source files
SWIFT_FILES=(
    "AppDelegate.swift"
    "MainViewController.swift"
    "MainViewController+Pages.swift"
    "Student.swift"
    "StudentRepository.swift"
)

print_info "Checking Swift source files..."
for file in "${SWIFT_FILES[@]}"; do
    if [[ -f "$XCODE_PROJECT_DIR/InteractiveTracker/$file" ]]; then
        print_status "$file found"
    else
        print_warning "$file not found"
    fi
done

# Check for Assets
if [[ -d "$XCODE_PROJECT_DIR/InteractiveTracker/Assets.xcassets" ]]; then
    print_status "Assets.xcassets found"
else
    print_warning "Assets.xcassets not found"
fi

# Build the project to validate setup
echo ""
print_info "Building project to validate setup..."

cd "$XCODE_PROJECT_DIR"

# Clean any previous builds
if [[ -d "$BUILD_DIR" ]]; then
    print_info "Cleaning previous build..."
    rm -rf "$BUILD_DIR"
fi

# Build the project
print_info "Building InteractiveTracker..."
if xcodebuild -project InteractiveTracker.xcodeproj -scheme InteractiveTracker -configuration Debug build CONFIGURATION_BUILD_DIR="$BUILD_DIR" > /dev/null 2>&1; then
    print_status "Project built successfully!"
else
    print_error "Build failed. Attempting with verbose output..."
    echo ""
    xcodebuild -project InteractiveTracker.xcodeproj -scheme InteractiveTracker -configuration Debug build CONFIGURATION_BUILD_DIR="$BUILD_DIR"
    exit 1
fi

# Check if app bundle was created
APP_BUNDLE="$BUILD_DIR/InteractiveTracker.app"
if [[ -d "$APP_BUNDLE" ]]; then
    print_status "App bundle created: $APP_BUNDLE"
    
    # Get app info
    if [[ -f "$APP_BUNDLE/Contents/Info.plist" ]]; then
        BUNDLE_ID=$(/usr/libexec/PlistBuddy -c "Print CFBundleIdentifier" "$APP_BUNDLE/Contents/Info.plist" 2>/dev/null || echo "N/A")
        VERSION=$(/usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" "$APP_BUNDLE/Contents/Info.plist" 2>/dev/null || echo "N/A") 
        print_info "Bundle ID: $BUNDLE_ID"
        print_info "Version: $VERSION"
    fi
else
    print_error "App bundle not found after build"
    exit 1
fi

# Create Documents directory test CSV path (where the app will store data)
DOCUMENTS_DIR="$HOME/Documents"
CSV_FILE="$DOCUMENTS_DIR/students.csv"

if [[ ! -d "$DOCUMENTS_DIR" ]]; then
    print_warning "Documents directory not found: $DOCUMENTS_DIR"
else
    print_status "Documents directory found"
    if [[ -f "$CSV_FILE" ]]; then
        print_info "Existing students.csv found at: $CSV_FILE"
    else
        print_info "students.csv will be created at: $CSV_FILE"
    fi
fi

# Setup complete
echo ""
print_status "Setup completed successfully!"
echo ""
print_info "Next steps:"
echo "  1. Open the project in Xcode:"
echo -e "     ${BLUE}open '$XCODE_PROJECT'${NC}"
echo ""
echo "  2. Build and run the project in Xcode (⌘+R)"
echo ""
echo "  3. Or run the built app directly:"
echo -e "     ${BLUE}open '$APP_BUNDLE'${NC}"
echo ""
echo "  4. For command-line building:"
echo -e "     ${BLUE}cd '$XCODE_PROJECT_DIR'${NC}"
echo -e "     ${BLUE}xcodebuild -project InteractiveTracker.xcodeproj -scheme InteractiveTracker -configuration Release build${NC}"
echo ""

print_info "The app will automatically create a students.csv file in your Documents folder."
print_info "For more development information, see: InteractiveTrackerXcode/README.md"

# Offer to open the project
echo ""
read -p "Would you like to open the project in Xcode now? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Opening project in Xcode..."
    open "$XCODE_PROJECT"
fi

print_status "Xcode environment setup complete!"
echo ""
print_info "Troubleshooting:"
echo "  - If you get signing errors, configure your Apple Developer account in Xcode"
echo "  - If builds fail, try cleaning the project: Product → Clean Build Folder (⇧⌘K)"
echo "  - For distribution builds, see: InteractiveTrackerXcode/README.md"
echo "  - If the app won't run, check your macOS version (requires 10.13+)"