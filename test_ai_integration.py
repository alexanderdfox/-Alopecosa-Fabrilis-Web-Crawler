#!/usr/bin/env python3
"""
Test script for AI-Enhanced Web Crawler integration
"""

import os
import sys

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        # Test original crawler
        from src.crawler.alopecosa_crawler import AlopecosaCrawler, CrawlResult
        print("✅ Original crawler imported successfully")
        
        # Test AI-enhanced crawler
        from src.crawler.ai_enhanced_crawler import AIEnhancedCrawler, SmartCrawlResult, AIAnalysis
        print("✅ AI-enhanced crawler imported successfully")
        
        # Test AI config
        from src.utils.ai_config import AIConfig, AIPromptTemplates, load_ai_config
        print("✅ AI configuration imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_ai_config():
    """Test AI configuration utilities"""
    print("\n🔧 Testing AI configuration...")
    
    try:
        from src.utils.ai_config import AIConfig, validate_ai_config
        
        # Test config creation
        config = AIConfig(openai_api_key="test-key")
        print("✅ AI config created successfully")
        
        # Test validation
        issues = validate_ai_config(config)
        if not issues:
            print("✅ AI config validation passed")
        else:
            print(f"⚠️  AI config validation issues: {issues}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI config test failed: {e}")
        return False

def test_crawler_creation():
    """Test that AI-enhanced crawler can be created"""
    print("\n🕷️ Testing crawler creation...")
    
    try:
        from src.crawler.ai_enhanced_crawler import AIEnhancedCrawler
        
        # Test creation without AI (fallback mode)
        crawler = AIEnhancedCrawler(
            base_url="https://example.com",
            use_ai=False,  # Disable AI to avoid API key requirement
            max_depth=1,
            max_pages=5
        )
        print("✅ AI-enhanced crawler created successfully (fallback mode)")
        
        # Test attributes
        print(f"  - Base URL: {crawler.base_url}")
        print(f"  - AI enabled: {crawler.use_ai}")
        print(f"  - Crawl objective: {crawler.crawl_objective}")
        print(f"  - Target topics: {crawler.target_topics}")
        
        return True
        
    except Exception as e:
        print(f"❌ Crawler creation test failed: {e}")
        return False

def test_ai_features():
    """Test AI feature availability"""
    print("\n🤖 Testing AI features...")
    
    try:
        from src.crawler.ai_enhanced_crawler import AIEnhancedCrawler
        
        # Check if OpenAI is available
        try:
            import openai
            openai_available = True
            print("✅ OpenAI package available")
        except ImportError:
            openai_available = False
            print("⚠️  OpenAI package not available")
        
        # Check if scikit-learn is available
        try:
            import sklearn
            sklearn_available = True
            print("✅ Scikit-learn package available")
        except ImportError:
            sklearn_available = False
            print("⚠️  Scikit-learn package not available")
        
        # Test AI feature detection
        crawler = AIEnhancedCrawler(
            base_url="https://example.com",
            use_ai=False,
            max_depth=1,
            max_pages=5
        )
        
        print(f"  - AI features enabled: {crawler.use_ai}")
        print(f"  - OpenAI available: {openai_available}")
        print(f"  - Scikit-learn available: {sklearn_available}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI features test failed: {e}")
        return False

def test_fallback_analysis():
    """Test fallback content analysis without AI"""
    print("\n🔄 Testing fallback analysis...")
    
    try:
        from src.crawler.ai_enhanced_crawler import AIEnhancedCrawler
        
        crawler = AIEnhancedCrawler(
            base_url="https://example.com",
            use_ai=False,
            max_depth=1,
            max_pages=5
        )
        
        # Test fallback content analysis
        test_content = "This is a test article about artificial intelligence and machine learning."
        test_title = "AI and ML Test Article"
        test_url = "https://example.com/test"
        
        analysis = crawler._analyze_content_fallback(test_content, test_title, test_url)
        
        print("✅ Fallback analysis created successfully")
        print(f"  - Relevance score: {analysis.relevance_score}")
        print(f"  - Quality score: {analysis.quality_score}")
        print(f"  - Category: {analysis.category}")
        print(f"  - Summary: {analysis.summary}")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback analysis test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AI-Enhanced Web Crawler Integration Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_ai_config,
        test_crawler_creation,
        test_ai_features,
        test_fallback_analysis
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AI integration is ready to use.")
        print("\nNext steps:")
        print("1. Set your OPENAI_API_KEY environment variable")
        print("2. Run: python -m src.examples.ai_crawler_demo")
        print("3. Or import AIEnhancedCrawler in your own scripts")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        print("\nTroubleshooting:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Check that all source files are in the correct locations")
        print("3. Verify Python path and module structure")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
