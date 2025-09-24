"""Success page displayed after student sign-in."""

import datetime
import time

import streamlit

from page_manager import PageManager


def show_success_page(page_manager: PageManager) -> None:
    """Display the success page after signing in a student."""
    streamlit.title("Successful Sign-In")
    
    if page_manager.success_data is None:
        page_manager.go_to_welcome()
        streamlit.rerun()
        return
    
    student_name = page_manager.success_data["name"]
    lesson_number = page_manager.success_data["lesson_number_taken_so_far"]
    
    streamlit.success(
        f"Thank you, {student_name}! You've been signed in for lesson #"
        f"{lesson_number}."
    )
    
    streamlit.markdown(
        f"**Lesson frequency:** "
        f"{page_manager.success_data['frequency_per_week']} per week"
    )
    
    streamlit.markdown(
        f"**Billing cycle:** {page_manager.success_data['billing_cycle']}"
    )
    
    # Display billing message if available
    if "billing_message" in page_manager.success_data:
        billing_msg = page_manager.success_data["billing_message"]
        if billing_msg:
            streamlit.info(f"💰 {billing_msg}")
    
    # Calculate remaining time
    elapsed = (
        datetime.datetime.now() - page_manager.countdown_start
    ).total_seconds()
    
    remaining = 5 - elapsed
    
    streamlit.markdown(
        f"Returning to welcome screen in **{int(remaining + 1)}** seconds..."
    )
    
    # When time is up, redirect to welcome
    if remaining <= 0:
        page_manager.clear_success_data()
        page_manager.go_to_welcome()
        streamlit.rerun()
    else:
        time.sleep(0.1)  # Small delay to prevent too many reruns
        streamlit.rerun()