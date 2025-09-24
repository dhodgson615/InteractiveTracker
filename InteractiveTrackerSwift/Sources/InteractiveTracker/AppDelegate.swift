#if canImport(Cocoa)
import Cocoa

@main
class AppDelegate: NSObject, NSApplicationDelegate {
    var window: NSWindow!
    var mainViewController: MainViewController!
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Create the main window
        window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 600, height: 500),
            styleMask: [.titled, .closable, .miniaturizable, .resizable],
            backing: .buffered,
            defer: false
        )
        
        window.title = "Student Lesson Tracker"
        window.center()
        window.setFrameAutosaveName("MainWindow")
        
        // Create and set the main view controller
        mainViewController = MainViewController()
        window.contentViewController = mainViewController
        
        window.makeKeyAndOrderFront(nil)
        
        // Bring app to front
        NSApp.setActivationPolicy(.regular)
        NSApp.activate(ignoringOtherApps: true)
    }
    
    func applicationWillTerminate(_ notification: Notification) {
        // Save any pending changes
        mainViewController.repository.saveStudents()
    }
    
    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        return true
    }
}
#endif