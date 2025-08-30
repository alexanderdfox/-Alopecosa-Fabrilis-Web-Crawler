#!/usr/bin/env python3
"""
Demo script for AI-Enhanced Web Crawler
Shows various use cases and capabilities
"""

import os
import sys
import time
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from crawler.ai_enhanced_crawler import AIEnhancedCrawler
from utils.ai_config import load_ai_config, validate_ai_config


def demo_tech_blog_crawling():
    """Demo: Crawling tech blogs for AI/ML content"""
    print("🚀 Demo 1: Crawling tech blog for AI/ML content")
    
    crawler = AIEnhancedCrawler(
        base_url="https://towardsdatascience.com",
        crawl_objective="Find high-quality articles about artificial intelligence and machine learning",
        target_topics=["artificial intelligence", "machine learning", "deep learning", "neural networks"],
        max_depth=2,
        max_pages=15,
        delay_range=(2, 4)
    )
    
    print("Starting smart crawl...")
    results = crawler.smart_crawl()
    
    print(f"Crawled {len(results)} pages")
    
    # Show insights
    insights = crawler.get_ai_insights()
    print(f"High-quality pages: {insights.get('high_quality_pages', 0)}")
    print(f"Average relevance: {insights.get('average_relevance_score', 0):.2f}")
    
    # Export results
    crawler.export_enhanced_results("tech_blog_crawl.json")
    
    return crawler


def demo_semantic_search(crawler):
    """Demo: Semantic search on crawled content"""
    print("\n🔍 Demo 2: Semantic search capabilities")
    
    search_queries = [
        "neural network architectures",
        "machine learning algorithms",
        "deep learning applications",
        "AI ethics and responsibility"
    ]
    
    for query in search_queries:
        print(f"\nSearching for: '{query}'")
        results = crawler.semantic_search(query, top_k=3)
        
        for i, (result, similarity) in enumerate(results, 1):
            print(f"  {i}. [{similarity:.3f}] {result.title}")
            if result.ai_analysis:
                print(f"     Summary: {result.ai_analysis.summary}")


def demo_content_analysis(crawler):
    """Demo: Content analysis and categorization"""
    print("\n📊 Demo 3: Content analysis and insights")
    
    insights = crawler.get_ai_insights()
    
    print("Content Categories:")
    for category, count in insights.get('content_categories', {}).items():
        print(f"  {category}: {count}")
    
    print(f"\nQuality Distribution:")
    print(f"  High quality (>0.8): {insights.get('high_quality_pages', 0)}")
    print(f"  Highly relevant (>0.8): {insights.get('highly_relevant_pages', 0)}")
    print(f"  Duplicates detected: {insights.get('duplicates_detected', 0)}")
    
    if crawler.use_ai:
        print(f"\nAI Performance:")
        print(f"  Total AI calls: {insights.get('ai_calls_made', 0)}")
        print(f"  AI processing time: {insights.get('ai_processing_time', 0):.2f}s")


def demo_adaptive_crawling():
    """Demo: Adaptive crawling with different objectives"""
    print("\n🔄 Demo 4: Adaptive crawling strategies")
    
    # Different crawling objectives
    objectives = [
        {
            "name": "Research Papers",
            "url": "https://arxiv.org",
            "objective": "Find research papers in computer science and AI",
            "topics": ["computer science", "artificial intelligence", "research papers"]
        },
        {
            "name": "Tech News",
            "url": "https://techcrunch.com",
            "objective": "Find latest technology news and startup information",
            "topics": ["technology", "startups", "innovation", "tech news"]
        }
    ]
    
    for obj in objectives:
        print(f"\nCrawling for: {obj['name']}")
        
        crawler = AIEnhancedCrawler(
            base_url=obj["url"],
            crawl_objective=obj["objective"],
            target_topics=obj["topics"],
            max_depth=1,
            max_pages=10,
            delay_range=(1, 2)
        )
        
        results = crawler.smart_crawl()
        insights = crawler.get_ai_insights()
        
        print(f"  Pages crawled: {len(results)}")
        print(f"  Average relevance: {insights.get('average_relevance_score', 0):.2f}")
        print(f"  High-quality content: {insights.get('high_quality_pages', 0)}")


def demo_fallback_mode():
    """Demo: Crawler working without AI (fallback mode)"""
    print("\n🔄 Demo 5: Fallback mode without AI")
    
    crawler = AIEnhancedCrawler(
        base_url="https://example.com",
        crawl_objective="General web content discovery",
        target_topics=["web development", "programming"],
        use_ai=False,  # Disable AI features
        max_depth=1,
        max_pages=5
    )
    
    print("Crawler initialized in fallback mode")
    print("AI features disabled - using heuristic-based analysis")
    
    # This would normally crawl, but we'll just show the configuration
    print(f"Crawl objective: {crawler.crawl_objective}")
    print(f"Target topics: {crawler.target_topics}")
    print(f"AI features enabled: {crawler.use_ai}")


def main():
    """Main demo function"""
    print("🕷️ AI-Enhanced Web Crawler Demo")
    print("=" * 50)
    
    # Check if OpenAI API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables")
        print("   AI features will be disabled. Set the key to enable full functionality.")
        print("   You can still run the crawler in fallback mode.")
        print()
    
    try:
        # Run demos
        if api_key:
            # Demo with AI enabled
            crawler = demo_tech_blog_crawling()
            demo_semantic_search(crawler)
            demo_content_analysis(crawler)
            demo_adaptive_crawling()
        else:
            # Demo without AI
            demo_fallback_mode()
        
        print("\n✅ All demos completed successfully!")
        print("\nTo run your own crawls:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Use: python -m src.examples.ai_crawler_demo")
        print("3. Or import AIEnhancedCrawler in your own scripts")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("This might be due to network issues or API limitations.")


if __name__ == "__main__":
    main()
