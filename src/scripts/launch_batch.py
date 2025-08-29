#!/usr/bin/env python3
"""
Launcher for Alopecosa Fabrilis Batch Scraper
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def main():
    """Main launcher function"""
    try:
        from batch_scraper.batch_url_scraper import main as batch_main
        
        print("🔄 Starting Alopecosa Fabrilis Batch Processor...")
        print("🕷️  The spider is ready to process multiple URLs!")
        print("=" * 50)
        
        # Run the batch processor
        batch_main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting batch processor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
