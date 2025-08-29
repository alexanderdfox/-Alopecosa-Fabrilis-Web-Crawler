#!/usr/bin/env python3
"""
Example Usage of Alopecosa Fabrilis Web Crawler
Demonstrates various ways to use the crawler
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
from datetime import datetime


def basic_crawl_example():
    """Basic example of using the crawler"""
    print("🕷️  Starting basic crawl example...")
    
    # Create crawler instance
    crawler = AlopecosaCrawler(
        base_url="https://example.com",
        max_depth=2,
        max_pages=10,
        delay_range=(1, 2)
    )
    
    # Start crawling
    results = crawler.crawl()
    
    print(f"✅ Crawled {len(results)} pages")
    
    # Save results
    crawler.save_results("basic_crawl_example.json")
    
    # Show statistics
    stats = crawler.get_crawl_statistics()
    print("\n📊 Crawl Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


def advanced_crawl_example():
    """Advanced example with custom settings"""
    print("\n🕷️  Starting advanced crawl example...")
    
    # Create crawler with custom settings
    crawler = AlopecosaCrawler(
        base_url="https://httpbin.org",
        max_depth=3,
        max_pages=20,
        delay_range=(0.5, 1.5),
        user_agent="My-Custom-Spider/1.0",
        respect_robots=True
    )
    
    # Start crawling
    results = crawler.crawl()
    
    print(f"✅ Crawled {len(results)} pages")
    
    # Save results with custom filename
    crawler.save_results("advanced_crawl_example.json")
    
    # Show detailed results
    print("\n🔍 Sample Results:")
    for i, result in enumerate(results[:3]):  # Show first 3 results
        print(f"\n  Result {i+1}:")
        print(f"    URL: {result.url}")
        print(f"    Title: {result.title}")
        print(f"    Links found: {len(result.links)}")
        print(f"    Crawl time: {result.crawl_time:.2f}s")


def spider_behavior_demo():
    """Demonstrate the spider-like behavior features"""
    print("\n🕷️  Demonstrating spider behavior...")
    
    crawler = AlopecosaCrawler(
        base_url="https://quotes.toscrape.com",
        max_depth=2,
        max_pages=15,
        delay_range=(1, 2)
    )
    
    # Start crawling
    results = crawler.crawl()
    
    print(f"✅ Crawled {len(results)} pages")
    
    # Show terrain map (spider's mental map of the web)
    print("\n🗺️  Terrain Map (Spider's Mental Map):")
    for url, info in list(crawler.terrain_map.items())[:5]:
        print(f"  {url}")
        print(f"    Depth: {info['depth']}")
        print(f"    Links: {info['link_count']}")
        print(f"    Title: {info['title']}")
        print()
    
    # Show prey scent (promising areas)
    print(f"🎯 Prey Scent (Rich hunting grounds): {len(crawler.prey_scent)} areas detected")
    
    # Save results
    crawler.save_results("spider_behavior_demo.json")


def custom_crawl_function():
    """Custom crawling function with specific requirements"""
    print("\n🕷️  Custom crawl function...")
    
    def custom_content_filter(result):
        """Custom filter for content"""
        # Only keep results with substantial content
        return len(result.content) > 100
    
    def custom_link_filter(links):
        """Custom filter for links"""
        # Only keep links that contain certain keywords
        keywords = ['page', 'article', 'post', 'content']
        return [link for link in links if any(keyword in link.lower() for keyword in keywords)]
    
    # Create crawler
    crawler = AlopecosaCrawler(
        base_url="https://httpbin.org",
        max_depth=2,
        max_pages=10,
        delay_range=(1, 2)
    )
    
    # Start crawling
    results = crawler.crawl()
    
    # Apply custom filters
    filtered_results = [r for r in results if custom_content_filter(r)]
    
    print(f"✅ Original results: {len(results)}")
    print(f"✅ Filtered results: {len(filtered_results)}")
    
    # Save filtered results
    with open("custom_filtered_results.json", "w") as f:
        json.dump([{
            'url': r.url,
            'title': r.title,
            'content_length': len(r.content),
            'links': custom_link_filter(r.links)
        } for r in filtered_results], f, indent=2)
    
    print("💾 Saved filtered results to custom_filtered_results.json")


def main():
    """Main function to run all examples"""
    print("🕷️  Alopecosa Fabrilis Web Crawler Examples")
    print("=" * 50)
    
    try:
        # Run examples
        basic_crawl_example()
        advanced_crawl_example()
        spider_behavior_demo()
        custom_crawl_function()
        
        print("\n🎉 All examples completed successfully!")
        print("\n📁 Generated files:")
        print("  - basic_crawl_example.json")
        print("  - advanced_crawl_example.json")
        print("  - spider_behavior_demo.json")
        print("  - custom_filtered_results.json")
        print("  - alopecosa_crawler.log")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("💡 Make sure you have the required dependencies installed:")
        print("   pip install -r requirements.txt")


if __name__ == "__main__":
    main()
