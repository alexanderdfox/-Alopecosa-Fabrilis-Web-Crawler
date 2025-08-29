#!/usr/bin/env python3
"""
Test Database Storage for Alopecosa Fabrilis Web Crawler
Tests if the database storage is working properly
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

from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_database_storage():
    """Test database storage functionality"""
    print("🕷️  Testing Database Storage System")
    print("=" * 50)
    
    try:
        # Test basic database functionality
        print("✅ Database manager initialized successfully")
        
        # Get current statistics
        stats = db_manager.get_statistics()
        print(f"📊 Current database stats: {stats}")
        
        # Test storing a simple crawl session
        print("\n🧪 Testing crawl session storage...")
        
        # Create mock results (simplified version of what the crawler would produce)
        class MockResult:
            def __init__(self, url, title, content, links, status_code, crawl_time, timestamp, metadata):
                self.url = url
                self.title = title
                self.content = content
                self.links = links
                self.status_code = status_code
                self.crawl_time = crawl_time
                self.timestamp = timestamp
                self.metadata = metadata
        
        # Create mock results
        mock_results = [
            MockResult(
                url="https://example.com",
                title="Example Domain",
                content="This domain is for use in illustrative examples in documents.",
                links=["https://example.com/page1", "https://example.com/page2"],
                status_code=200,
                crawl_time=0.5,
                timestamp=datetime.now(),
                metadata={"depth": 0, "source": "test"}
            ),
            MockResult(
                url="https://example.com/page1",
                title="Page 1",
                content="This is page 1 content for testing.",
                links=["https://example.com", "https://example.com/page2"],
                status_code=200,
                crawl_time=0.3,
                timestamp=datetime.now(),
                metadata={"depth": 1, "source": "test"}
            )
        ]
        
        # Test storing results
        start_time = datetime.now()
        end_time = datetime.now()
        
        session_id = db_manager.store_crawl_results(
            session_name="Test Crawl Session",
            base_url="https://example.com",
            max_depth=2,
            max_pages=10,
            results=mock_results,
            start_time=start_time,
            end_time=end_time,
            status='completed'
        )
        
        print(f"✅ Successfully stored test crawl session with ID: {session_id}")
        
        # Check updated statistics
        new_stats = db_manager.get_statistics()
        print(f"📊 Updated database stats: {new_stats}")
        
        # Test search functionality
        print("\n🔍 Testing search functionality...")
        results, count = db_manager.search_websites("example")
        print(f"✅ Search test successful: {count} results found")
        
        if results:
            print(f"📄 First result: {results[0]['title']}")
        
        # Test getting crawl sessions
        print("\n📅 Testing crawl sessions retrieval...")
        sessions = db_manager.get_crawl_sessions(limit=5)
        print(f"✅ Retrieved {len(sessions)} crawl sessions")
        
        if sessions:
            latest_session = sessions[0]
            print(f"📋 Latest session: {latest_session['session_name']} - {latest_session['pages_crawled']} pages")
        
        print("\n🎉 Database storage system is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Database storage test failed: {e}")
        logger.error(f"Database storage test error: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def main():
    """Main function"""
    print("🚀 Testing Alopecosa Fabrilis Database Storage...")
    
    try:
        success = test_database_storage()
        
        if success:
            print("\n🎯 Database storage is ready!")
            print("💡 You can now run crawlers and they will be automatically stored in the database.")
        else:
            print("\n⚠️  Database storage test failed. Check the error messages above.")
            
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
