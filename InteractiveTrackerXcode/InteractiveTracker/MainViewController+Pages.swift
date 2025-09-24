import Cocoa

extension MainViewController {
    
    // MARK: - Welcome Page
    
    func showWelcomePage() {
        titleLabel.stringValue = "Lesson Sign-In"
        
        let welcomeLabel = NSTextField(labelWithString: "Welcome!")
        welcomeLabel.font = NSFont.systemFont(ofSize: 16, weight: .medium)
        welcomeLabel.alignment = .center
        
        let buttonStackView = NSStackView()
        buttonStackView.orientation = .horizontal
        buttonStackView.spacing = 20
        
        let newStudentButton = NSButton(title: "New Student", target: self, action: #selector(newStudentTapped))
        newStudentButton.bezelStyle = .rounded
        newStudentButton.controlSize = .large
        
        let returningStudentButton = NSButton(title: "Returning Student", target: self, action: #selector(returningStudentTapped))
        returningStudentButton.bezelStyle = .rounded
        returningStudentButton.controlSize = .large
        
        buttonStackView.addArrangedSubview(newStudentButton)
        buttonStackView.addArrangedSubview(returningStudentButton)
        
        contentStackView.addArrangedSubview(welcomeLabel)
        contentStackView.addArrangedSubview(buttonStackView)
    }
    
    @objc private func newStudentTapped() {
        goToNewStudent()
    }
    
    @objc private func returningStudentTapped() {
        goToLetterSelect()
    }
    
    // MARK: - New Student Page
    
    func showNewStudentPage() {
        titleLabel.stringValue = "New Student Registration"
        
        let welcomeLabel = NSTextField(labelWithString: "Welcome! Please enter your name")
        welcomeLabel.font = NSFont.systemFont(ofSize: 16, weight: .medium)
        welcomeLabel.alignment = .center
        
        let nameLabel = NSTextField(labelWithString: "Full Name:")
        nameLabel.font = NSFont.systemFont(ofSize: 12)
        
        let nameField = NSTextField()
        nameField.font = NSFont.systemFont(ofSize: 12)
        nameField.placeholderString = "Enter your full name"
        
        let registerButton = NSButton(title: "Register", target: self, action: #selector(registerButtonTapped(_:)))
        registerButton.bezelStyle = .rounded
        registerButton.controlSize = .large
        registerButton.keyEquivalent = "\r" // Enter key
        
        let backButton = NSButton(title: "Back", target: self, action: #selector(backToWelcomeTapped))
        backButton.bezelStyle = .rounded
        
        // Store reference to name field for later access
        nameField.tag = 1001
        
        contentStackView.addArrangedSubview(welcomeLabel)
        contentStackView.addArrangedSubview(nameLabel)
        contentStackView.addArrangedSubview(nameField)
        contentStackView.addArrangedSubview(registerButton)
        contentStackView.addArrangedSubview(backButton)
        
        // Set initial focus
        DispatchQueue.main.async {
            nameField.becomeFirstResponder()
        }
    }
    
    @objc private func registerButtonTapped(_ sender: NSButton) {
        guard let nameField = contentStackView.viewWithTag(1001) as? NSTextField else { return }
        let name = nameField.stringValue.trimmingCharacters(in: .whitespacesAndNewlines)
        
        guard !name.isEmpty else {
            showAlert(title: "Error", message: "Please enter a name.")
            return
        }
        
        let result = repository.addStudent(name: name)
        switch result {
        case .success(let student):
            goToSuccess(with: student)
        case .failure(_):
            showAlert(title: "Error", message: "Student already exists")
        }
    }
    
    @objc private func backToWelcomeTapped() {
        goToWelcome()
    }
    
    // MARK: - Letter Select Page
    
    func showLetterSelectPage() {
        titleLabel.stringValue = "Returning Student"
        
        let questionLabel = NSTextField(labelWithString: "What's the first letter of your first name?")
        questionLabel.font = NSFont.systemFont(ofSize: 16, weight: .medium)
        questionLabel.alignment = .center
        
        let letters = repository.uniqueFirstLetters
        
        guard !letters.isEmpty else {
            let warningLabel = NSTextField(labelWithString: "No students found in the system.")
            warningLabel.font = NSFont.systemFont(ofSize: 12)
            warningLabel.alignment = .center
            
            let backButton = NSButton(title: "Back", target: self, action: #selector(backToWelcomeTapped))
            backButton.bezelStyle = .rounded
            
            contentStackView.addArrangedSubview(warningLabel)
            contentStackView.addArrangedSubview(backButton)
            return
        }
        
        // Create grid of letter buttons
        let gridView = NSView()
        gridView.translatesAutoresizingMaskIntoConstraints = false
        
        let buttonsPerRow = 5
        let rows = (letters.count + buttonsPerRow - 1) / buttonsPerRow
        
        for (index, letter) in letters.enumerated() {
            let button = NSButton(title: letter, target: self, action: #selector(letterButtonTapped(_:)))
            button.bezelStyle = .rounded
            button.tag = index
            button.translatesAutoresizingMaskIntoConstraints = false
            gridView.addSubview(button)
            
            let row = index / buttonsPerRow
            let col = index % buttonsPerRow
            
            NSLayoutConstraint.activate([
                button.widthAnchor.constraint(equalToConstant: 60),
                button.heightAnchor.constraint(equalToConstant: 30),
                button.leadingAnchor.constraint(equalTo: gridView.leadingAnchor, constant: CGFloat(col * 70)),
                button.topAnchor.constraint(equalTo: gridView.topAnchor, constant: CGFloat(row * 40))
            ])
        }
        
        // Set grid view size
        NSLayoutConstraint.activate([
            gridView.widthAnchor.constraint(equalToConstant: CGFloat(min(buttonsPerRow, letters.count) * 70)),
            gridView.heightAnchor.constraint(equalToConstant: CGFloat(rows * 40))
        ])
        
        let backButton = NSButton(title: "Back", target: self, action: #selector(backToWelcomeTapped))
        backButton.bezelStyle = .rounded
        
        contentStackView.addArrangedSubview(questionLabel)
        contentStackView.addArrangedSubview(gridView)
        contentStackView.addArrangedSubview(backButton)
    }
    
    @objc private func letterButtonTapped(_ sender: NSButton) {
        let letters = repository.uniqueFirstLetters
        guard sender.tag < letters.count else { return }
        let letter = letters[sender.tag]
        selectLetter(letter)
    }
    
    // MARK: - Student Select Page
    
    func showStudentSelectPage() {
        titleLabel.stringValue = "Student Selection"
        
        guard !selectedLetter.isEmpty else {
            let warningLabel = NSTextField(labelWithString: "No letter selected. Please select a letter first.")
            warningLabel.font = NSFont.systemFont(ofSize: 12)
            warningLabel.alignment = .center
            
            let backButton = NSButton(title: "Back to Letter Selection", target: self, action: #selector(backToLetterSelectTapped))
            backButton.bezelStyle = .rounded
            
            contentStackView.addArrangedSubview(warningLabel)
            contentStackView.addArrangedSubview(backButton)
            return
        }
        
        let studentsLabel = NSTextField(labelWithString: "Students with names starting with '\(selectedLetter)'")
        studentsLabel.font = NSFont.systemFont(ofSize: 16, weight: .medium)
        studentsLabel.alignment = .center
        
        let students = repository.studentsStartingWith(letter: selectedLetter)
        
        guard !students.isEmpty else {
            let warningLabel = NSTextField(labelWithString: "No students found with names starting with '\(selectedLetter)'")
            warningLabel.font = NSFont.systemFont(ofSize: 12)
            warningLabel.alignment = .center
            
            let backButton = NSButton(title: "Back to Letter Selection", target: self, action: #selector(backToLetterSelectTapped))
            backButton.bezelStyle = .rounded
            
            contentStackView.addArrangedSubview(warningLabel)
            contentStackView.addArrangedSubview(backButton)
            return
        }
        
        let selectLabel = NSTextField(labelWithString: "Please select your name:")
        selectLabel.font = NSFont.systemFont(ofSize: 12)
        
        let studentPopup = NSPopUpButton()
        studentPopup.removeAllItems()
        for student in students {
            studentPopup.addItem(withTitle: student.name)
        }
        studentPopup.tag = 2001
        
        let noteLabel = NSTextField(labelWithString: "Add a note (optional):")
        noteLabel.font = NSFont.systemFont(ofSize: 12)
        
        let noteField = NSTextField()
        noteField.font = NSFont.systemFont(ofSize: 12)
        noteField.placeholderString = "Optional note"
        noteField.tag = 2002
        
        let signInButton = NSButton(title: "Sign In", target: self, action: #selector(signInButtonTapped))
        signInButton.bezelStyle = .rounded
        signInButton.controlSize = .large
        signInButton.keyEquivalent = "\r"
        
        let backButton = NSButton(title: "Back to Letter Selection", target: self, action: #selector(backToLetterSelectTapped))
        backButton.bezelStyle = .rounded
        
        contentStackView.addArrangedSubview(studentsLabel)
        contentStackView.addArrangedSubview(selectLabel)
        contentStackView.addArrangedSubview(studentPopup)
        contentStackView.addArrangedSubview(noteLabel)
        contentStackView.addArrangedSubview(noteField)
        contentStackView.addArrangedSubview(signInButton)
        contentStackView.addArrangedSubview(backButton)
    }
    
    @objc private func signInButtonTapped() {
        guard let popup = contentStackView.viewWithTag(2001) as? NSPopUpButton,
              let noteField = contentStackView.viewWithTag(2002) as? NSTextField else { return }
        
        guard let selectedTitle = popup.selectedItem?.title else {
            showAlert(title: "Error", message: "Please select a student.")
            return
        }
        
        let note = noteField.stringValue
        
        guard let updatedStudent = repository.updateStudentLesson(studentName: selectedTitle, note: note) else {
            showAlert(title: "Error", message: "Failed to update student record.")
            return
        }
        
        goToSuccess(with: updatedStudent)
    }
    
    @objc private func backToLetterSelectTapped() {
        goToLetterSelect()
    }
    
    // MARK: - Success Page
    
    func showSuccessPage() {
        titleLabel.stringValue = "Successful Sign-In"
        
        guard let student = successData else {
            goToWelcome()
            return
        }
        
        let successLabel = NSTextField(labelWithString: "Thank you, \(student.name)! You've been signed in for lesson #\(student.lessonNumberTakenSoFar).")
        successLabel.font = NSFont.systemFont(ofSize: 16, weight: .medium)
        successLabel.alignment = .center
        successLabel.isSelectable = false
        successLabel.maximumNumberOfLines = 0
        successLabel.lineBreakMode = .byWordWrapping
        
        let freqLabel = NSTextField(labelWithString: "Lesson frequency: \(student.frequencyPerWeek) per week")
        freqLabel.font = NSFont.systemFont(ofSize: 12)
        freqLabel.alignment = .center
        
        let billingLabel = NSTextField(labelWithString: "Billing cycle: \(student.billingCycle)")
        billingLabel.font = NSFont.systemFont(ofSize: 12)
        billingLabel.alignment = .center
        
        contentStackView.addArrangedSubview(successLabel)
        contentStackView.addArrangedSubview(freqLabel)
        contentStackView.addArrangedSubview(billingLabel)
        
        // Add billing message if available
        if let billingMessage = student.billingMessage {
            let billingInfoLabel = NSTextField(labelWithString: "💰 \(billingMessage)")
            billingInfoLabel.font = NSFont.systemFont(ofSize: 12)
            billingInfoLabel.alignment = .center
            contentStackView.addArrangedSubview(billingInfoLabel)
        }
        
        // Countdown label
        let countdownLabel = NSTextField(labelWithString: "Returning to welcome screen in 5 seconds...")
        countdownLabel.font = NSFont.systemFont(ofSize: 12)
        countdownLabel.alignment = .center
        countdownLabel.tag = 3001
        contentStackView.addArrangedSubview(countdownLabel)
    }
    
    private func startCountdownTimer() {
        var remainingTime = 5
        
        countdownTimer?.invalidate()
        countdownTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] timer in
            remainingTime -= 1
            
            if let countdownLabel = self?.contentStackView.viewWithTag(3001) as? NSTextField {
                if remainingTime > 0 {
                    countdownLabel.stringValue = "Returning to welcome screen in \(remainingTime) seconds..."
                } else {
                    timer.invalidate()
                    self?.goToWelcome()
                }
            }
        }
    }
    
    // MARK: - Helper Methods
    
    private func showAlert(title: String, message: String) {
        let alert = NSAlert()
        alert.messageText = title
        alert.informativeText = message
        alert.alertStyle = .warning
        alert.addButton(withTitle: "OK")
        
        if let window = view.window {
            alert.beginSheetModal(for: window)
        } else {
            alert.runModal()
        }
    }
}