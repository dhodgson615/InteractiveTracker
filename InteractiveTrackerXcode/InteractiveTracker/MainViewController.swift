import Cocoa

enum Page {
    case welcome
    case newStudent
    case letterSelect
    case studentSelect
    case success
}

class MainViewController: NSViewController {
    let repository = StudentRepository()
    private var currentPage: Page = .welcome
    private var selectedLetter: String = ""
    private var successData: Student?
    private var countdownTimer: Timer?
    
    // UI Components
    private var containerView: NSView!
    private var titleLabel: NSTextField!
    private var contentStackView: NSStackView!
    private var footerView: NSView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        showCurrentPage()
    }
    
    private func setupUI() {
        view.wantsLayer = true
        view.layer?.backgroundColor = NSColor.controlBackgroundColor.cgColor
        
        // Create container view
        containerView = NSView()
        containerView.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(containerView)
        
        // Create title label
        titleLabel = NSTextField(labelWithString: "Student Lesson Tracker")
        titleLabel.font = NSFont.systemFont(ofSize: 24, weight: .bold)
        titleLabel.alignment = .center
        titleLabel.translatesAutoresizingMaskIntoConstraints = false
        containerView.addSubview(titleLabel)
        
        // Create content stack view
        contentStackView = NSStackView()
        contentStackView.orientation = .vertical
        contentStackView.alignment = .centerX
        contentStackView.spacing = 20
        contentStackView.translatesAutoresizingMaskIntoConstraints = false
        containerView.addSubview(contentStackView)
        
        // Create footer
        footerView = createFooter()
        containerView.addSubview(footerView)
        
        // Set up constraints
        NSLayoutConstraint.activate([
            containerView.topAnchor.constraint(equalTo: view.topAnchor, constant: 20),
            containerView.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
            containerView.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20),
            containerView.bottomAnchor.constraint(equalTo: view.bottomAnchor, constant: -20),
            
            titleLabel.topAnchor.constraint(equalTo: containerView.topAnchor),
            titleLabel.leadingAnchor.constraint(equalTo: containerView.leadingAnchor),
            titleLabel.trailingAnchor.constraint(equalTo: containerView.trailingAnchor),
            
            contentStackView.topAnchor.constraint(equalTo: titleLabel.bottomAnchor, constant: 30),
            contentStackView.leadingAnchor.constraint(equalTo: containerView.leadingAnchor),
            contentStackView.trailingAnchor.constraint(equalTo: containerView.trailingAnchor),
            
            footerView.bottomAnchor.constraint(equalTo: containerView.bottomAnchor),
            footerView.leadingAnchor.constraint(equalTo: containerView.leadingAnchor),
            footerView.trailingAnchor.constraint(equalTo: containerView.trailingAnchor),
            footerView.heightAnchor.constraint(equalToConstant: 60)
        ])
    }
    
    private func createFooter() -> NSView {
        let footer = NSView()
        footer.translatesAutoresizingMaskIntoConstraints = false
        
        let separator = NSBox()
        separator.boxType = .separator
        separator.translatesAutoresizingMaskIntoConstraints = false
        footer.addSubview(separator)
        
        let versionLabel = NSTextField(labelWithString: "Student Lesson Tracker v1.0")
        versionLabel.font = NSFont.systemFont(ofSize: 10)
        versionLabel.textColor = .secondaryLabelColor
        versionLabel.alignment = .center
        versionLabel.translatesAutoresizingMaskIntoConstraints = false
        footer.addSubview(versionLabel)
        
        let authorLabel = NSTextField(labelWithString: "Created by Dylan Hodgson")
        authorLabel.font = NSFont.systemFont(ofSize: 10)
        authorLabel.textColor = .secondaryLabelColor
        authorLabel.alignment = .center
        authorLabel.translatesAutoresizingMaskIntoConstraints = false
        footer.addSubview(authorLabel)
        
        NSLayoutConstraint.activate([
            separator.topAnchor.constraint(equalTo: footer.topAnchor),
            separator.leadingAnchor.constraint(equalTo: footer.leadingAnchor),
            separator.trailingAnchor.constraint(equalTo: footer.trailingAnchor),
            
            versionLabel.topAnchor.constraint(equalTo: separator.bottomAnchor, constant: 10),
            versionLabel.leadingAnchor.constraint(equalTo: footer.leadingAnchor),
            versionLabel.trailingAnchor.constraint(equalTo: footer.trailingAnchor),
            
            authorLabel.topAnchor.constraint(equalTo: versionLabel.bottomAnchor, constant: 5),
            authorLabel.leadingAnchor.constraint(equalTo: footer.leadingAnchor),
            authorLabel.trailingAnchor.constraint(equalTo: footer.trailingAnchor)
        ])
        
        return footer
    }
    
    private func clearContent() {
        contentStackView.arrangedSubviews.forEach { $0.removeFromSuperview() }
    }
    
    func showCurrentPage() {
        clearContent()
        
        switch currentPage {
        case .welcome:
            showWelcomePage()
        case .newStudent:
            showNewStudentPage()
        case .letterSelect:
            showLetterSelectPage()
        case .studentSelect:
            showStudentSelectPage()
        case .success:
            showSuccessPage()
        }
    }
    
    // MARK: - Page Navigation
    
    func goToWelcome() {
        currentPage = .welcome
        showCurrentPage()
    }
    
    func goToNewStudent() {
        currentPage = .newStudent
        showCurrentPage()
    }
    
    func goToLetterSelect() {
        currentPage = .letterSelect
        showCurrentPage()
    }
    
    func goToStudentSelect() {
        currentPage = .studentSelect
        showCurrentPage()
    }
    
    func goToSuccess(with student: Student) {
        successData = student
        currentPage = .success
        showCurrentPage()
        startCountdownTimer()
    }
    
    func selectLetter(_ letter: String) {
        selectedLetter = letter
        goToStudentSelect()
    }
}