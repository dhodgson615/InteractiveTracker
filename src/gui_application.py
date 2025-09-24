"""Main GUI application controller for the Interactive Tracker."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import threading
import time

from models import Student
from gui_page_manager import GUIPageManager
from gui_repository import GUIStudentRepository


class GUIApplication:
    """Main GUI application controller that coordinates all components."""
    
    def __init__(self) -> None:
        """Initialize the application with all required components."""
        self.page_manager = GUIPageManager()
        self.student_repository = GUIStudentRepository()
        
        # Initialize GUI
        self.root = tk.Tk()
        self.root.title("Student Lesson Tracker")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Center the window
        self._center_window()
        
        # Configure styles for better macOS appearance
        self._configure_styles()
        
        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        
        # Variables for form inputs
        self.student_name_var = tk.StringVar()
        self.note_var = tk.StringVar()
        self.selected_student_var = tk.StringVar()
        
        # Success page countdown timer
        self.countdown_timer = None
        
    def _center_window(self) -> None:
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_reqwidth()
        height = self.root.winfo_reqheight()
        pos_x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    def _configure_styles(self) -> None:
        """Configure TTK styles for better appearance."""
        style = ttk.Style()
        
        # Configure button styles
        style.configure("Primary.TButton", font=("SF Pro Display", 12))
        style.configure("Large.TButton", font=("SF Pro Display", 14), padding=(20, 10))
        
        # Configure label styles
        style.configure("Title.TLabel", font=("SF Pro Display", 24, "bold"))
        style.configure("Heading.TLabel", font=("SF Pro Display", 16, "bold"))
        style.configure("Body.TLabel", font=("SF Pro Display", 12))
        style.configure("Footer.TLabel", font=("SF Pro Display", 10), foreground="gray")
    
    def run(self) -> None:
        """Main application entry point that starts the GUI loop."""
        self._update_display()
        self.root.mainloop()
    
    def _update_display(self) -> None:
        """Update the display based on the current page."""
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        current_page = self.page_manager.current_page
        
        if current_page == GUIPageManager.WELCOME:
            self._show_welcome_page()
        elif current_page == GUIPageManager.NEW_STUDENT:
            self._show_new_student_page()
        elif current_page == GUIPageManager.LETTER_SELECT:
            self._show_letter_select_page()
        elif current_page == GUIPageManager.STUDENT_SELECT:
            self._show_student_select_page()
        elif current_page == GUIPageManager.SUCCESS:
            self._show_success_page()
        
        # Show footer on all pages
        self._show_footer()
    
    def _show_welcome_page(self) -> None:
        """Display the welcome page with options for new and returning students."""
        # Title
        title_label = ttk.Label(self.main_frame, text="Lesson Sign-In", style="Title.TLabel")
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Welcome message
        welcome_label = ttk.Label(self.main_frame, text="Welcome!", style="Heading.TLabel")
        welcome_label.grid(row=1, column=0, pady=(0, 30))
        
        # Button frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, pady=20)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        # New Student button
        new_student_btn = ttk.Button(
            button_frame, 
            text="New Student",
            style="Large.TButton",
            command=self._go_to_new_student
        )
        new_student_btn.grid(row=0, column=0, padx=(0, 10), sticky=(tk.W, tk.E))
        
        # Returning Student button
        returning_student_btn = ttk.Button(
            button_frame,
            text="Returning Student", 
            style="Large.TButton",
            command=self._go_to_letter_select
        )
        returning_student_btn.grid(row=0, column=1, padx=(10, 0), sticky=(tk.W, tk.E))
    
    def _show_new_student_page(self) -> None:
        """Display the new student registration page."""
        # Title
        title_label = ttk.Label(self.main_frame, text="New Student Registration", style="Title.TLabel")
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Welcome message
        welcome_label = ttk.Label(self.main_frame, text="Welcome! Please enter your name", style="Heading.TLabel")
        welcome_label.grid(row=1, column=0, pady=(0, 30))
        
        # Name input
        name_label = ttk.Label(self.main_frame, text="Full Name:", style="Body.TLabel")
        name_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        name_entry = ttk.Entry(self.main_frame, textvariable=self.student_name_var, font=("SF Pro Display", 12), width=30)
        name_entry.grid(row=3, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        name_entry.focus()
        
        # Register button
        register_btn = ttk.Button(
            self.main_frame,
            text="Register",
            style="Large.TButton", 
            command=self._register_new_student
        )
        register_btn.grid(row=4, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # Back button
        back_btn = ttk.Button(
            self.main_frame,
            text="Back",
            command=self._go_to_welcome
        )
        back_btn.grid(row=5, column=0, pady=10)
        
        # Bind Enter key to register
        name_entry.bind('<Return>', lambda e: self._register_new_student())
    
    def _show_letter_select_page(self) -> None:
        """Display the letter selection page for returning students."""
        # Title
        title_label = ttk.Label(self.main_frame, text="Returning Student", style="Title.TLabel")
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Question
        question_label = ttk.Label(self.main_frame, text="What's the first letter of your first name?", style="Heading.TLabel")
        question_label.grid(row=1, column=0, pady=(0, 30))
        
        # Get unique first letters from student names
        first_letters = self.student_repository.get_unique_first_letters()
        
        if not first_letters:
            warning_label = ttk.Label(self.main_frame, text="No students found in the system.", style="Body.TLabel")
            warning_label.grid(row=2, column=0, pady=20)
            
            back_btn = ttk.Button(self.main_frame, text="Back", command=self._go_to_welcome)
            back_btn.grid(row=3, column=0, pady=10)
            return
        
        # Create grid of letter buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, pady=20)
        
        cols = 5
        for i, letter in enumerate(first_letters):
            row = i // cols
            col = i % cols
            
            letter_btn = ttk.Button(
                button_frame,
                text=letter,
                command=lambda l=letter: self._select_letter(l),
                width=8
            )
            letter_btn.grid(row=row, column=col, padx=5, pady=5)
        
        # Back button
        back_btn = ttk.Button(self.main_frame, text="Back", command=self._go_to_welcome)
        back_btn.grid(row=3, column=0, pady=20)
    
    def _show_student_select_page(self) -> None:
        """Display the student selection page based on the selected letter."""
        # Title
        title_label = ttk.Label(self.main_frame, text="Student Selection", style="Title.TLabel")
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Safety check - if no letter is selected, go back to letter selection
        if not self.page_manager.selected_letter:
            warning_label = ttk.Label(self.main_frame, text="No letter selected. Please select a letter first.", style="Body.TLabel")
            warning_label.grid(row=1, column=0, pady=20)
            
            back_btn = ttk.Button(self.main_frame, text="Back to Letter Selection", command=self._go_to_letter_select)
            back_btn.grid(row=2, column=0, pady=10)
            return
        
        # Students heading
        heading_label = ttk.Label(
            self.main_frame, 
            text=f"Students with names starting with '{self.page_manager.selected_letter}'",
            style="Heading.TLabel"
        )
        heading_label.grid(row=1, column=0, pady=(0, 20))
        
        # Get students filtered by the selected letter
        students = self.student_repository.get_students_by_first_letter(self.page_manager.selected_letter)
        
        if not students:
            warning_label = ttk.Label(
                self.main_frame, 
                text=f"No students found with names starting with '{self.page_manager.selected_letter}'",
                style="Body.TLabel"
            )
            warning_label.grid(row=2, column=0, pady=20)
            
            back_btn = ttk.Button(self.main_frame, text="Back to Letter Selection", command=self._go_to_letter_select)
            back_btn.grid(row=3, column=0, pady=10)
            return
        
        # Student selection
        select_label = ttk.Label(self.main_frame, text="Please select your name:", style="Body.TLabel")
        select_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        student_names = [student.name for student in students]
        student_combo = ttk.Combobox(
            self.main_frame, 
            textvariable=self.selected_student_var, 
            values=student_names,
            state="readonly",
            font=("SF Pro Display", 12),
            width=30
        )
        student_combo.grid(row=3, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        if student_names:
            student_combo.current(0)
        
        # Note input
        note_label = ttk.Label(self.main_frame, text="Add a note (optional):", style="Body.TLabel")
        note_label.grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        
        note_text = tk.Text(self.main_frame, height=3, width=30, font=("SF Pro Display", 12))
        note_text.grid(row=5, column=0, pady=(0, 20), sticky=(tk.W, tk.E))
        
        # Sign In button
        signin_btn = ttk.Button(
            self.main_frame,
            text="Sign In",
            style="Large.TButton",
            command=lambda: self._sign_in_student(note_text.get("1.0", tk.END).strip())
        )
        signin_btn.grid(row=6, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # Back button
        back_btn = ttk.Button(self.main_frame, text="Back to Letter Selection", command=self._go_to_letter_select)
        back_btn.grid(row=7, column=0, pady=10)
    
    def _show_success_page(self) -> None:
        """Display the success page after signing in a student."""
        # Check if we have success data
        if self.page_manager.success_data is None:
            self._go_to_welcome()
            return
        
        student_name = self.page_manager.success_data["name"]
        lesson_number = self.page_manager.success_data["lesson_number_taken_so_far"]
        
        # Title
        title_label = ttk.Label(self.main_frame, text="Successful Sign-In", style="Title.TLabel")
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Success message
        success_label = ttk.Label(
            self.main_frame,
            text=f"Thank you, {student_name}! You've been signed in for lesson #{lesson_number}.",
            style="Heading.TLabel",
            wraplength=500
        )
        success_label.grid(row=1, column=0, pady=(0, 20))
        
        # Lesson info
        freq_label = ttk.Label(
            self.main_frame,
            text=f"Lesson frequency: {self.page_manager.success_data['frequency_per_week']} per week",
            style="Body.TLabel"
        )
        freq_label.grid(row=2, column=0, pady=5)
        
        billing_label = ttk.Label(
            self.main_frame,
            text=f"Billing cycle: {self.page_manager.success_data['billing_cycle']}",
            style="Body.TLabel"
        )
        billing_label.grid(row=3, column=0, pady=5)
        
        # Display billing message if available
        if "billing_message" in self.page_manager.success_data:
            billing_msg = self.page_manager.success_data["billing_message"]
            if billing_msg:
                billing_info_label = ttk.Label(
                    self.main_frame,
                    text=f"💰 {billing_msg}",
                    style="Body.TLabel"
                )
                billing_info_label.grid(row=4, column=0, pady=10)
        
        # Countdown message
        self.countdown_label = ttk.Label(
            self.main_frame,
            text="Returning to welcome screen in 5 seconds...",
            style="Body.TLabel"
        )
        self.countdown_label.grid(row=5, column=0, pady=20)
        
        # Start countdown timer
        self._start_countdown_timer()
    
    def _show_footer(self) -> None:
        """Display the footer with version information."""
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.grid(row=10, column=0, pady=(20, 0), sticky=(tk.W, tk.E))
        
        # Separator
        separator = ttk.Separator(footer_frame, orient='horizontal')
        separator.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Version info
        version_label = ttk.Label(footer_frame, text="Student Lesson Tracker v1.0", style="Footer.TLabel")
        version_label.grid(row=1, column=0)
        
        author_label = ttk.Label(footer_frame, text="Created by Dylan Hodgson", style="Footer.TLabel")
        author_label.grid(row=2, column=0)
    
    def _go_to_welcome(self) -> None:
        """Navigate to welcome page and refresh display."""
        self.page_manager.go_to_welcome()
        self._update_display()
    
    def _go_to_new_student(self) -> None:
        """Navigate to new student page and refresh display."""
        self.student_name_var.set("")
        self.page_manager.go_to_new_student()
        self._update_display()
    
    def _go_to_letter_select(self) -> None:
        """Navigate to letter selection page and refresh display."""
        self.page_manager.go_to_letter_select()
        self._update_display()
    
    def _go_to_student_select(self) -> None:
        """Navigate to student selection page and refresh display."""
        self.page_manager.go_to_student_select()
        self._update_display()
    
    def _select_letter(self, letter: str) -> None:
        """Handle letter selection."""
        self.page_manager.set_selected_letter(letter)
        self._go_to_student_select()
    
    def _register_new_student(self) -> None:
        """Handle new student registration."""
        name = self.student_name_var.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter a name.")
            return
        
        try:
            success, result = self.student_repository.add_new_student(name)
            
            if success:
                # result is a Student object
                self.page_manager.go_to_success(result.to_dict())
                self._update_display()
            else:
                # result is an error message
                messagebox.showerror("Error", result)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def _sign_in_student(self, note: str) -> None:
        """Handle student sign-in."""
        selected_name = self.selected_student_var.get()
        
        if not selected_name:
            messagebox.showerror("Error", "Please select a student.")
            return
        
        try:
            updated_student = self.student_repository.update_student_lesson(selected_name, note)
            
            if updated_student:
                self.page_manager.go_to_success(updated_student.to_dict())
                self._update_display()
            else:
                messagebox.showerror("Error", "Failed to update student record.")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def _start_countdown_timer(self) -> None:
        """Start the countdown timer for the success page."""
        if self.countdown_timer:
            self.root.after_cancel(self.countdown_timer)
        
        self._update_countdown()
    
    def _update_countdown(self) -> None:
        """Update the countdown display."""
        if self.page_manager.countdown_start is None:
            return
        
        elapsed = (datetime.datetime.now() - self.page_manager.countdown_start).total_seconds()
        remaining = max(0, 5 - elapsed)
        
        if hasattr(self, 'countdown_label'):
            if remaining > 0:
                self.countdown_label.config(text=f"Returning to welcome screen in {int(remaining + 1)} seconds...")
                self.countdown_timer = self.root.after(100, self._update_countdown)
            else:
                self.page_manager.clear_success_data()
                self._go_to_welcome()