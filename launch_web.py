#!/usr/bin/env python3
"""
Launcher for Alopecosa Fabrilis Web Interface
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    # Import and run the web interface launcher
    from scripts.launch_web import main
    main()
