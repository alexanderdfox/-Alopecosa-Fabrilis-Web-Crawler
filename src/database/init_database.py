#!/usr/bin/env python3
"""
Database Initialization Script for Alopecosa Fabrilis Web Crawler
Creates and tests the database system
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    # Try relative imports first (when running as package)
    from ..database.database_manager import db_manager
except ImportError:
    # Fall back to absolute imports (when running from project root)
    from src.database.database_manager import db_manager

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database():
    """Test the database functionality"""
    print("🕷️  Testing Alopecosa Fabrilis Database System")
    print("=" * 50)
    
    try:
        # Test database initialization
        print("✅ Database initialized successfully")
        
        # Test statistics
        stats = db_manager.get_statistics()
        print(f"📊 Database Statistics:")
        print(f"   Total websites: {stats.get('total_websites', 0)}")
        print(f"   Total links: {stats.get('total_links', 0)}")
        print(f"   Total sessions: {stats.get('total_sessions', 0)}")
        print(f"   Unique domains: {stats.get('unique_domains', 0)}")
        print(f"   Recent activity (7 days): {stats.get('websites_last_7_days', 0)}")
        
        # Test domains
        domains = db_manager.get_domains()
        print(f"🌐 Available domains: {len(domains)}")
        if domains:
            print(f"   Sample domains: {', '.join(domains[:5])}")
        
        # Test crawl sessions
        sessions = db_manager.get_crawl_sessions(limit=5)
        print(f"📅 Crawl sessions: {len(sessions)}")
        
        # Test search (empty database)
        results, count = db_manager.search_websites("test")
        print(f"🔍 Search test: {count} results found")
        
        print("\n🎉 Database system is working correctly!")
        print("💡 You can now use the web interface to crawl and search websites!")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        logger.error(f"Database test error: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🚀 Initializing Alopecosa Fabrilis Database...")
    
    try:
        success = test_database()
        
        if success:
            print("\n🎯 Next steps:")
            print("1. Launch the web interface: python3 launch_web.py")
            print("2. Create some crawlers and crawl websites")
            print("3. Use the database search interface at /database")
            print("4. Search through your crawled data!")
        else:
            print("\n⚠️  Database initialization failed. Check the error messages above.")
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
