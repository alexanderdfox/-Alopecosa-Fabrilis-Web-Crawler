#!/usr/bin/env python3
"""
Simple test script for the Alopecosa Fabrilis Web Crawler
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    # Try relative imports first (when running as package)
    from ..crawler.alopecosa_crawler import AlopecosaCrawler
except ImportError:
    # Fall back to absolute imports (when running from project root)
    from src.crawler.alopecosa_crawler import AlopecosaCrawler

import json

def test_basic_functionality():
    """Test basic crawler functionality"""
    print("🧪 Testing basic crawler functionality...")
    
    # Test with a simple, reliable site
    crawler = AlopecosaCrawler(
        base_url="https://example.com",
        max_depth=1,
        max_pages=2,
        delay_range=(1, 2)
    )
    
    try:
        # Start crawling
        results = crawler.crawl()
        
        print(f"✅ Crawling completed! Crawled {len(results)} pages")
        
        if results:
            print("\n📄 Sample result:")
            result = results[0]
            print(f"  URL: {result.url}")
            print(f"  Title: {result.title}")
            print(f"  Links found: {len(result.links)}")
            print(f"  Content length: {len(result.content)} characters")
        
        # Save results
        crawler.save_results("test_results.json")
        print("💾 Results saved to test_results.json")
        
        # Show statistics
        stats = crawler.get_crawl_statistics()
        print("\n📊 Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def test_spider_features():
    """Test spider-like behavior features"""
    print("\n🕷️  Testing spider behavior features...")
    
    crawler = AlopecosaCrawler(
        base_url="https://example.com",
        max_depth=2,
        max_pages=3,
        delay_range=(1, 2)
    )
    
    try:
        # Start crawling
        results = crawler.crawl()
        
        print(f"✅ Crawled {len(results)} pages")
        
        # Test terrain mapping
        print(f"🗺️  Terrain map entries: {len(crawler.terrain_map)}")
        
        # Test prey scent detection
        print(f"🎯 Prey scent areas: {len(crawler.prey_scent)}")
        
        # Show some terrain map details
        if crawler.terrain_map:
            print("\n📍 Terrain Map Sample:")
            for url, info in list(crawler.terrain_map.items())[:2]:
                print(f"  {url}")
                print(f"    Depth: {info['depth']}")
                print(f"    Links: {info['link_count']}")
                print(f"    Title: {info['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing spider features: {e}")
        return False

def main():
    """Main test function"""
    print("🕷️  Alopecosa Fabrilis Web Crawler - Test Suite")
    print("=" * 50)
    
    # Test basic functionality
    basic_success = test_basic_functionality()
    
    # Test spider features
    spider_success = test_spider_features()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"  Basic functionality: {'✅ PASS' if basic_success else '❌ FAIL'}")
    print(f"  Spider features: {'✅ PASS' if spider_success else '❌ FAIL'}")
    
    if basic_success and spider_success:
        print("\n🎉 All tests passed! The crawler is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
    
    print("\n📁 Generated files:")
    print("  - test_results.json")
    print("  - alopecosa_crawler.log")

if __name__ == "__main__":
    main()
