#!/usr/bin/env python3
"""
Launch script for the Interactive Tracker GUI application.
This script can be used to run the application from the command line.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from main_app import main
    main()
except KeyboardInterrupt:
    print("\nApplication terminated by user.")
except Exception as e:
    print(f"Error starting application: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)