#!/usr/bin/env python3
"""
Batch URL Scraper for Alopecosa Fabrilis Web Crawler
Scrapes a list of URLs and stores all results in the database
"""

import json
import csv
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

try:
    # Try relative imports first (when running as package)
    from ..crawler.alopecosa_crawler import AlopecosaCrawler
    from ..database.database_manager import db_manager
    from ..utils.config import CRAWLER_CONFIG
except ImportError:
    # Fall back to absolute imports (when running from project root)
    from src.crawler.alopecosa_crawler import AlopecosaCrawler
    from src.database.database_manager import db_manager
    from src.utils.config import CRAWLER_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BatchURLScraper:
    """Batch scraper for processing multiple URLs"""
    
    def __init__(self, max_workers: int = 3, delay_between_crawls: float = 2.0):
        """
        Initialize the batch scraper
        
        Args:
            max_workers: Maximum number of concurrent crawlers
            delay_between_crawls: Delay between starting new crawls (seconds)
        """
        self.max_workers = max_workers
        self.delay_between_crawls = delay_between_crawls
        self.results = {}
        self.errors = {}
        self.lock = threading.Lock()
        
        # Ensure database is initialized
        try:
            db_manager.init_database()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def load_urls_from_file(self, file_path: str, file_type: str = 'auto') -> List[str]:
        """
        Load URLs from various file formats
        
        Args:
            file_path: Path to the file containing URLs
            file_type: File type ('txt', 'csv', 'json', 'auto' for detection)
        
        Returns:
            List of URLs to scrape
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"URL file not found: {file_path}")
        
        # Auto-detect file type if not specified
        if file_type == 'auto':
            if file_path.suffix == '.txt':
                file_type = 'txt'
            elif file_path.suffix == '.csv':
                file_type = 'csv'
            elif file_path.suffix == '.json':
                file_type = 'json'
            else:
                file_type = 'txt'  # Default to text
        
        urls = []
        
        try:
            if file_type == 'txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):  # Skip empty lines and comments
                            urls.append(line)
            
            elif file_type == 'csv':
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row and row[0].strip():  # Skip empty rows
                            urls.append(row[0].strip())
            
            elif file_type == 'json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        urls = [str(url) for url in data if url]
                    elif isinstance(data, dict) and 'urls' in data:
                        urls = [str(url) for url in data['urls'] if url]
                    else:
                        raise ValueError("JSON file must contain a list of URLs or dict with 'urls' key")
            
            logger.info(f"Loaded {len(urls)} URLs from {file_path}")
            return urls
            
        except Exception as e:
            logger.error(f"Error loading URLs from {file_path}: {e}")
            raise
    
    def create_sample_url_files(self):
        """Create sample URL files for testing"""
        sample_dir = Path("sample_urls")
        sample_dir.mkdir(exist_ok=True)
        
        # Sample URLs for testing
        sample_urls = [
            "https://example.com",
            "https://httpbin.org",
            "https://jsonplaceholder.typicode.com",
            "https://httpstat.us",
            "https://httpbin.org/status/200",
            "https://httpbin.org/status/404",
            "https://httpbin.org/delay/1",
            "https://httpbin.org/headers",
            "https://httpbin.org/user-agent",
            "https://httpbin.org/ip"
        ]
        
        # Create text file
        txt_file = sample_dir / "sample_urls.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("# Sample URLs for testing the batch scraper\n")
            f.write("# Lines starting with # are comments\n\n")
            for url in sample_urls:
                f.write(f"{url}\n")
        
        # Create CSV file
        csv_file = sample_dir / "sample_urls.csv"
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["url", "description"])
            for url in sample_urls:
                writer.writerow([url, "Test URL"])
        
        # Create JSON file
        json_file = sample_dir / "sample_urls.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "description": "Sample URLs for testing",
                "created": datetime.now().isoformat(),
                "urls": sample_urls
            }, f, indent=2)
        
        logger.info(f"Created sample URL files in {sample_dir}/")
        return sample_dir
    
    def scrape_single_url(self, url: str, config: dict) -> Dict[str, Any]:
        """
        Scrape a single URL with the given configuration
        
        Args:
            url: URL to scrape
            config: Crawler configuration dictionary
        
        Returns:
            Dictionary containing scrape results and metadata
        """
        start_time = time.time()
        result = {
            'url': url,
            'success': False,
            'start_time': datetime.now(),
            'end_time': None,
            'pages_crawled': 0,
            'links_found': 0,
            'error': None,
            'session_id': None,
            'results': []
        }
        
        try:
            logger.info(f"Starting crawl of {url}")
            
            # Create crawler instance with proper configuration
            crawler = AlopecosaCrawler(
                base_url=url,
                max_depth=config.get('default_max_depth', 3),
                max_pages=config.get('default_max_pages', 100),
                delay_range=config.get('default_delay_range', (1, 3))
            )
            
            # Run the crawl
            results = crawler.crawl()
            
            # Calculate statistics
            end_time = datetime.now()
            crawl_duration = time.time() - start_time
            
            # Store results in database
            try:
                session_id = db_manager.store_crawl_results(
                    session_name=f"Batch Crawl - {url}",
                    base_url=url,
                    max_depth=config.get('default_max_depth', 3),
                    max_pages=config.get('default_max_pages', 100),
                    results=results,
                    start_time=result['start_time'],
                    end_time=end_time,
                    status='completed'
                )
                result['session_id'] = session_id
                logger.info(f"Stored results in database with session ID: {session_id}")
            except Exception as e:
                logger.error(f"Failed to store results in database for {url}: {e}")
                result['error'] = f"Database storage failed: {e}"
            
            # Update result metadata
            result.update({
                'success': True,
                'end_time': end_time,
                'pages_crawled': len(results),
                'links_found': sum(len(r.links) for r in results),
                'crawl_duration': crawl_duration,
                'results': results
            })
            
            logger.info(f"Successfully crawled {url}: {len(results)} pages in {crawl_duration:.2f}s")
            
        except Exception as e:
            end_time = datetime.now()
            result.update({
                'end_time': end_time,
                'error': str(e),
                'crawl_duration': time.time() - start_time
            })
            logger.error(f"Failed to crawl {url}: {e}")
        
        return result
    
    def scrape_urls(self, urls: List[str], config: dict = None) -> Dict[str, Any]:
        """
        Scrape multiple URLs using thread pool
        
        Args:
            urls: List of URLs to scrape
            config: Crawler configuration dictionary (uses default if None)
        
        Returns:
            Dictionary containing all scrape results
        """
        if config is None:
            config = CRAWLER_CONFIG.copy()
        
        logger.info(f"Starting batch scrape of {len(urls)} URLs with {self.max_workers} workers")
        
        # Create thread pool
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all crawl jobs
            future_to_url = {
                executor.submit(self.scrape_single_url, url, config): url 
                for url in urls
            }
            
            # Process completed jobs
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    
                    with self.lock:
                        if result['success']:
                            self.results[url] = result
                        else:
                            self.errors[url] = result
                    
                    # Add delay between crawls to be respectful
                    time.sleep(self.delay_between_crawls)
                    
                except Exception as e:
                    logger.error(f"Unexpected error processing {url}: {e}")
                    with self.lock:
                        self.errors[url] = {
                            'url': url,
                            'success': False,
                            'error': f"Unexpected error: {e}",
                            'start_time': datetime.now(),
                            'end_time': datetime.now()
                        }
        
        # Generate summary
        summary = self._generate_summary()
        logger.info(f"Batch scrape completed: {summary['successful']} successful, {summary['failed']} failed")
        
        return {
            'summary': summary,
            'results': self.results,
            'errors': self.errors
        }
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics from batch scrape"""
        successful = len(self.results)
        failed = len(self.errors)
        total_pages = sum(r['pages_crawled'] for r in self.results.values())
        total_links = sum(r['links_found'] for r in self.results.values())
        total_duration = sum(r.get('crawl_duration', 0) for r in self.results.values())
        
        return {
            'total_urls': successful + failed,
            'successful': successful,
            'failed': failed,
            'total_pages_crawled': total_pages,
            'total_links_found': total_links,
            'total_crawl_time': total_duration,
            'average_crawl_time': total_duration / successful if successful > 0 else 0,
            'success_rate': (successful / (successful + failed)) * 100 if (successful + failed) > 0 else 0
        }
    
    def save_batch_results(self, output_file: str = None) -> str:
        """
        Save batch results to a file
        
        Args:
            output_file: Output file path (auto-generated if None)
        
        Returns:
            Path to the saved file
        """
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"batch_scrape_results_{timestamp}.json"
        
        # Prepare data for JSON serialization
        serializable_results = {}
        for url, result in self.results.items():
            serializable_results[url] = {
                'url': result['url'],
                'success': result['success'],
                'start_time': result['start_time'].isoformat(),
                'end_time': result['end_time'].isoformat() if result['end_time'] else None,
                'pages_crawled': result['pages_crawled'],
                'links_found': result['links_found'],
                'crawl_duration': result.get('crawl_duration', 0),
                'session_id': result.get('session_id'),
                'error': result.get('error')
            }
        
        serializable_errors = {}
        for url, error in self.errors.items():
            serializable_errors[url] = {
                'url': error['url'],
                'success': error['success'],
                'start_time': error['start_time'].isoformat(),
                'end_time': error['end_time'].isoformat() if error.get('end_time') else None,
                'error': error['error'],
                'crawl_duration': error.get('crawl_duration', 0)
            }
        
        output_data = {
            'batch_scrape_summary': {
                'timestamp': datetime.now().isoformat(),
                'summary': self._generate_summary()
            },
            'successful_crawls': serializable_results,
            'failed_crawls': serializable_errors
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Batch results saved to {output_file}")
        return output_file
    
    def print_summary(self):
        """Print a formatted summary of the batch scrape"""
        summary = self._generate_summary()
        
        print("\n" + "="*60)
        print("🕷️  BATCH SCRAPE SUMMARY")
        print("="*60)
        print(f"📊 Total URLs: {summary['total_urls']}")
        print(f"✅ Successful: {summary['successful']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"📄 Total Pages Crawled: {summary['total_pages_crawled']}")
        print(f"🔗 Total Links Found: {summary['total_links_found']}")
        print(f"⏱️  Total Crawl Time: {summary['total_crawl_time']:.2f}s")
        print(f"📈 Success Rate: {summary['success_rate']:.1f}%")
        print(f"⏱️  Average Crawl Time: {summary['average_crawl_time']:.2f}s")
        
        if self.errors:
            print(f"\n❌ FAILED CRAWLS:")
            for url, error in self.errors.items():
                print(f"   • {url}: {error.get('error', 'Unknown error')}")
        
        print("="*60)


def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Batch URL Scraper for Alopecosa Fabrilis Web Crawler"
    )
    parser.add_argument(
        'url_file',
        nargs='?',
        help='File containing URLs to scrape (txt, csv, or json)'
    )
    parser.add_argument(
        '--file-type',
        choices=['txt', 'csv', 'json', 'auto'],
        default='auto',
        help='File type (auto-detected if not specified)'
    )
    parser.add_argument(
        '--max-workers',
        type=int,
        default=3,
        help='Maximum number of concurrent crawlers (default: 3)'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=2.0,
        help='Delay between starting new crawls in seconds (default: 2.0)'
    )
    parser.add_argument(
        '--max-depth',
        type=int,
        default=1,
        help='Maximum crawl depth (default: 1)'
    )
    parser.add_argument(
        '--max-pages',
        type=int,
        default=10,
        help='Maximum pages to crawl per site (default: 10)'
    )
    parser.add_argument(
        '--output',
        help='Output file for results (auto-generated if not specified)'
    )
    parser.add_argument(
        '--create-samples',
        action='store_true',
        help='Create sample URL files for testing'
    )
    
    args = parser.parse_args()
    
    try:
        # Create sample files if requested
        if args.create_samples:
            scraper = BatchURLScraper()
            sample_dir = scraper.create_sample_url_files()
            print(f"✅ Sample URL files created in {sample_dir}/")
            print("📝 Edit these files to add your own URLs, then run the scraper")
            return
        
        # Check if URL file is provided
        if not args.url_file:
            print("❌ URL file is required unless using --create-samples")
            return 1
        
        # Initialize scraper
        scraper = BatchURLScraper(
            max_workers=args.max_workers,
            delay_between_crawls=args.delay
        )
        
        # Load URLs
        print(f"📂 Loading URLs from {args.url_file}...")
        urls = scraper.load_urls_from_file(args.url_file, args.file_type)
        
        if not urls:
            print("❌ No URLs found in file")
            return 1
        
        # Create crawler configuration
        config = CRAWLER_CONFIG.copy()
        config.update({
            'default_max_depth': args.max_depth,
            'default_max_pages': args.max_pages,
            'default_delay_range': (1, 3)  # Be respectful
        })
        
        # Run batch scrape
        print(f"🚀 Starting batch scrape of {len(urls)} URLs...")
        results = scraper.scrape_urls(urls, config)
        
        # Print summary
        scraper.print_summary()
        
        # Save results
        output_file = scraper.save_batch_results(args.output)
        print(f"💾 Results saved to {output_file}")
        
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
        
    except Exception as e:
        logger.error(f"Batch scrape failed: {e}")
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
