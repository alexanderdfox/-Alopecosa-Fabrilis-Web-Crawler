#!/usr/bin/env python3
"""
Interactive Demo for Alopecosa Fabrilis Web Crawler
Demonstrates the crawler's capabilities with user interaction
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

import time
import json

def demo_spider_behavior():
    """Demonstrate the spider-like behavior with a content-rich site"""
    print("🕷️  Alopecosa Fabrilis Web Crawler - Live Demonstration")
    print("=" * 60)
    
    print("🎯 Target: Quotes.toscrape.com (a quotes website)")
    print("🕸️  Strategy: Hunt for content-rich areas like a spider")
    print("🗺️  Goal: Build a mental map of the web structure")
    print()
    
    # Create crawler with spider-like settings
    crawler = AlopecosaCrawler(
        base_url="https://quotes.toscrape.com",
        max_depth=2,
        max_pages=10,
        delay_range=(1, 2),
        respect_robots=True
    )
    
    print("🚀 Starting the hunt...")
    start_time = time.time()
    
    try:
        # Start crawling
        results = crawler.crawl()
        
        crawl_duration = time.time() - start_time
        
        print(f"\n✅ Hunt completed in {crawl_duration:.1f} seconds!")
        print(f"🕷️  Pages explored: {len(results)}")
        print(f"🗺️  Territory mapped: {len(crawler.terrain_map)} areas")
        print(f"🎯 Rich hunting grounds found: {len(crawler.prey_scent)}")
        
        # Show what the spider discovered
        if results:
            print("\n🔍 Spider's Discoveries:")
            for i, result in enumerate(results[:5]):  # Show first 5 results
                print(f"\n  📄 Discovery {i+1}:")
                print(f"     🏷️  Title: {result.title}")
                print(f"     🔗 URL: {result.url}")
                print(f"     📊 Links found: {len(result.links)}")
                print(f"     ⏱️  Crawl time: {result.crawl_time:.2f}s")
                print(f"     📏 Content length: {len(result.content)} chars")
                
                # Show some sample links
                if result.links:
                    print(f"     🔗 Sample links:")
                    for link in result.links[:3]:
                        print(f"        - {link}")
        
        # Show terrain map insights
        if crawler.terrain_map:
            print(f"\n🗺️  Spider's Mental Map:")
            print(f"     Total areas explored: {len(crawler.terrain_map)}")
            
            # Find the richest area (most links)
            richest_area = max(crawler.terrain_map.items(), 
                             key=lambda x: x[1]['link_count'])
            print(f"     🎯 Richest hunting ground: {richest_area[1]['link_count']} links")
            print(f"     📍 Location: {richest_area[0]}")
        
        # Show statistics
        stats = crawler.get_crawl_statistics()
        print(f"\n📊 Hunt Statistics:")
        print(f"     🎯 Success rate: {stats.get('success_rate', 0):.1%}")
        print(f"     🔗 Total links discovered: {stats.get('total_links_discovered', 0)}")
        print(f"     📊 Average links per page: {stats.get('average_links_per_page', 0):.1f}")
        print(f"     ⏱️  Average crawl time: {stats.get('average_crawl_time', 0):.2f}s")
        
        # Save the spider's findings
        filename = "spider_hunt_results.json"
        crawler.save_results(filename)
        print(f"\n💾 Spider's findings saved to: {filename}")
        
        print(f"\n🎉 The Alopecosa Fabrilis has completed its hunt successfully!")
        print(f"🕷️  It has mapped {len(crawler.terrain_map)} areas and discovered {len(results)} pages")
        print(f"🗺️  The terrain map shows the web structure as the spider sees it")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Hunt failed: {e}")
        print("🕷️  The spider encountered an obstacle...")
        return False

def show_spider_insights():
    """Show insights about how the spider thinks"""
    print("\n🧠 Spider Intelligence Insights:")
    print("=" * 40)
    
    print("🕸️  How the Alopecosa Fabrilis thinks:")
    print("   • It doesn't just crawl randomly - it hunts intelligently")
    print("   • It builds a mental map of the web as it explores")
    print("   • It remembers 'rich' areas with lots of content/links")
    print("   • It adapts its strategy based on what it finds")
    print("   • It prioritizes promising areas over barren ones")
    
    print("\n🎯 Prey Detection Strategy:")
    print("   • Analyzes link density in each area")
    print("   • Marks areas with >5 links as 'rich hunting grounds'")
    print("   • Prioritizes these areas for deeper exploration")
    print("   • Builds scent trails to remember good locations")
    
    print("\n🗺️  Terrain Mapping:")
    print("   • Creates a mental model of the web structure")
    print("   • Records depth, link counts, and discovery times")
    print("   • Uses this map to navigate efficiently")
    print("   • Avoids revisiting already explored areas")

def main():
    """Main demonstration function"""
    print("🕷️  Welcome to the Alopecosa Fabrilis Web Crawler!")
    print("This crawler mimics the hunting behavior of a real spider.")
    print()
    
    # Show spider insights
    show_spider_insights()
    
    print("\n" + "=" * 60)
    print("🚀 Ready to see the spider in action?")
    input("Press Enter to start the demonstration...")
    
    # Run the demonstration
    success = demo_spider_behavior()
    
    if success:
        print("\n🎯 Demonstration completed successfully!")
        print("🕷️  You've witnessed the power of spider-inspired web crawling!")
    else:
        print("\n⚠️  Demonstration encountered issues.")
        print("🕷️  Even spiders have bad days sometimes...")
    
    print("\n📚 To learn more, check out:")
    print("   • README.md - Complete documentation")
    print("   • example_usage.py - More examples")
    print("   • config.py - Configuration options")

if __name__ == "__main__":
    main()
