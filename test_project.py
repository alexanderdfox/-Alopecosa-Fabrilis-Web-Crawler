#!/usr/bin/env python3
"""
Test script launcher for Alopecosa Fabrilis Web Crawler
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    # Import and run the test script
    from scripts.test_imports import main
    main()
