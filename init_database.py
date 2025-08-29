#!/usr/bin/env python3
"""
Database Initializer for Alopecosa Fabrilis Web Crawler
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    # Import and run the database initializer
    from scripts.init_database import main
    main()
