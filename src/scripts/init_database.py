#!/usr/bin/env python3
"""
Database Initializer for Alopecosa Fabrilis Web Crawler
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def main():
    """Initialize and test the database system"""
    print("🕷️  Alopecosa Fabrilis Database Initializer")
    print("=" * 50)
    
    try:
        # Use the global database manager instance
        from database.database_manager import db_manager
        
        print("✅ Database initialized successfully!")
        
        # Get statistics
        stats = db_manager.get_statistics()
        print(f"📊 Database statistics: {stats}")
        
        print("\n🎯 Database is ready!")
        print("💡 You can now run crawlers and batch scrapers")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
