#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """Test all package imports"""
    print("🧪 Testing Alopecosa Fabrilis package imports...")
    print("=" * 50)
    
    try:
        # Test crawler package
        print("📦 Testing crawler package...")
        from crawler.alopecosa_crawler import AlopecosaCrawler, CrawlResult
        print("✅ Crawler package imported successfully")
        
        # Test database package
        print("📦 Testing database package...")
        from database.database_manager import DatabaseManager
        print("✅ Database package imported successfully")
        
        # Test batch scraper package
        print("📦 Testing batch scraper package...")
        from batch_scraper.batch_url_scraper import BatchURLScraper
        print("✅ Batch scraper package imported successfully")
        
        # Test utils package
        print("📦 Testing utils package...")
        from utils.config import CRAWLER_CONFIG, LOGGING_CONFIG
        print("✅ Utils package imported successfully")
        
        # Test web interface package (without starting server)
        print("📦 Testing web interface package...")
        from web_interface.web_interface import app, crawler_manager
        print("✅ Web interface package imported successfully")
        
        # Test main package
        print("📦 Testing main package...")
        from src import AlopecosaCrawler, DatabaseManager, BatchURLScraper, CRAWLER_CONFIG
        print("✅ Main package imported successfully")
        
        print("\n🎉 All imports successful! The project structure is working correctly.")
        print("\n📋 Available components:")
        print("   • AlopecosaCrawler - Core crawling engine")
        print("   • DatabaseManager - Database operations")
        print("   • BatchURLScraper - Batch URL processing")
        print("   • CRAWLER_CONFIG - Configuration settings")
        print("   • Flask app - Web interface")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without starting servers"""
    print("\n🧪 Testing basic functionality...")
    print("=" * 50)
    
    try:
        # Test crawler creation
        print("🕷️  Testing crawler creation...")
        from crawler.alopecosa_crawler import AlopecosaCrawler
        crawler = AlopecosaCrawler("https://example.com", max_depth=1, max_pages=1)
        print("✅ Crawler created successfully")
        
        # Test database manager
        print("🗄️  Testing database manager...")
        from database.database_manager import db_manager
        print("✅ Database manager created successfully")
        
        # Test batch scraper
        print("🔄 Testing batch scraper...")
        from batch_scraper.batch_url_scraper import BatchURLScraper
        scraper = BatchURLScraper(max_workers=1)
        print("✅ Batch scraper created successfully")
        
        print("\n🎉 Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Alopecosa Fabrilis Import and Functionality Test")
    print("=" * 60)
    
    # Test imports
    imports_ok = test_imports()
    
    if imports_ok:
        # Test basic functionality
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n🎯 All tests passed! Your project is ready to use.")
            print("\n💡 Next steps:")
            print("   1. Initialize database: python3 init_database.py")
            print("   2. Launch web interface: python3 launch_web.py")
            print("   3. Run batch processor: python3 launch_batch.py --create-samples")
        else:
            print("\n⚠️  Import tests passed but functionality tests failed.")
            print("💡 Check the error messages above for issues.")
            sys.exit(1)
    else:
        print("\n❌ Import tests failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
