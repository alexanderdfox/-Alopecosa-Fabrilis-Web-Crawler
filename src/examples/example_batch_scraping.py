#!/usr/bin/env python3
"""
Example Batch Scraping with Alopecosa Fabrilis Web Crawler
Demonstrates how to use the batch scraper for multiple URLs
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    # Try relative imports first (when running as package)
    from ..batch_scraper.batch_url_scraper import BatchURLScraper
    from ..utils.config import CRAWLER_CONFIG
except ImportError:
    # Fall back to absolute imports (when running from project root)
    from src.batch_scraper.batch_url_scraper import BatchURLScraper
    from src.utils.config import CRAWLER_CONFIG

import time
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def example_batch_scraping():
    """Example of using the batch scraper programmatically"""
    
    print("🕷️  Example: Batch URL Scraping")
    print("=" * 50)
    
    # List of URLs to scrape
    urls = [
        "https://example.com",
        "https://httpbin.org",
        "https://jsonplaceholder.typicode.com"
    ]
    
    print(f"📋 URLs to scrape: {len(urls)}")
    for url in urls:
        print(f"   • {url}")
    
    try:
        # Initialize the batch scraper
        print("\n🚀 Initializing batch scraper...")
        scraper = BatchURLScraper(
            max_workers=2,  # Process 2 URLs concurrently
            delay_between_crawls=3.0  # 3 second delay between crawls
        )
        
        # Create custom configuration
        config = CRAWLER_CONFIG.copy()
        config.update({
            'default_max_depth': 1,      # Only crawl 1 level deep
            'default_max_pages': 5,      # Maximum 5 pages per site
            'default_delay_range': (2, 4)  # 2-4 second delays between requests
        })
        
        print(f"⚙️  Configuration: max_depth={config['default_max_depth']}, max_pages={config['default_max_pages']}")
        
        # Start the batch scrape
        print("\n🕷️  Starting batch scrape...")
        results = scraper.scrape_urls(urls, config)
        
        # Print summary
        scraper.print_summary()
        
        # Save results to file
        output_file = scraper.save_batch_results()
        print(f"\n💾 Results saved to: {output_file}")
        
        # Show database statistics
        try:
            stats = db_manager.get_statistics()
            print(f"\n🗄️  Database Statistics:")
            print(f"   Total Websites: {stats['total_websites']}")
            print(f"   Total Links: {stats['total_links']}")
            print(f"   Total Sessions: {stats['total_sessions']}")
            print(f"   Unique Domains: {stats['unique_domains']}")
        except Exception as e:
            print(f"⚠️  Could not retrieve database statistics: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"Batch scraping example failed: {e}")
        print(f"❌ Error: {e}")
        return False

def example_with_custom_urls():
    """Example with custom URLs from a file"""
    
    print("\n🕷️  Example: Custom URLs from File")
    print("=" * 50)
    
    try:
        # Initialize scraper
        scraper = BatchURLScraper(max_workers=1, delay_between_crawls=5.0)
        
        # Load URLs from the sample text file
        urls = scraper.load_urls_from_file("sample_urls/sample_urls.txt", "txt")
        
        print(f"📂 Loaded {len(urls)} URLs from file")
        
        # Use default configuration
        config = CRAWLER_CONFIG.copy()
        
        # Run with limited scope for demo
        limited_urls = urls[:3]  # Only first 3 URLs for demo
        print(f"🧪 Running demo with first {len(limited_urls)} URLs...")
        
        results = scraper.scrape_urls(limited_urls, config)
        
        # Print summary
        scraper.print_summary()
        
        return True
        
    except Exception as e:
        logger.error(f"Custom URLs example failed: {e}")
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Alopecosa Fabrilis Batch Scraper Examples")
    print("=" * 60)
    
    # Example 1: Direct URL list
    success1 = example_batch_scraping()
    
    if success1:
        print("\n✅ First example completed successfully!")
    else:
        print("\n❌ First example failed")
    
    # Example 2: URLs from file
    success2 = example_with_custom_urls()
    
    if success2:
        print("\n✅ Second example completed successfully!")
    else:
        print("\n❌ Second example failed")
    
    print("\n🎯 Examples completed!")
    print("💡 You can now use the batch scraper with your own URL lists!")

if __name__ == "__main__":
    main()
