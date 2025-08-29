#!/usr/bin/env python3
"""
Alopecosa Fabrilis Web Crawler
A web crawler inspired by the hunting behavior of the Alopecosa fabrilis spider.
This spider is known for its active hunting strategy and efficient terrain navigation.
"""

import requests
import time
import random
import logging
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import deque
import json
import os
from typing import Set, Dict, List, Optional
import threading
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CrawlResult:
    """Represents the result of crawling a single URL"""
    url: str
    title: str
    content: str
    links: List[str]
    status_code: int
    crawl_time: float
    timestamp: datetime
    metadata: Dict


class AlopecosaCrawler:
    """
    A web crawler that mimics the hunting behavior of Alopecosa fabrilis:
    - Active hunting: Proactively seeks out new URLs
    - Terrain mapping: Builds a map of the web structure
    - Adaptive behavior: Adjusts crawling strategy based on results
    - Efficient movement: Uses intelligent pathfinding
    """
    
    def __init__(self, 
                 base_url: str,
                 max_depth: int = 3,
                 max_pages: int = 100,
                 delay_range: tuple = (1, 3),
                 user_agent: str = None,
                 respect_robots: bool = True):
        
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.delay_range = delay_range
        self.respect_robots = respect_robots
        
        # Spider-like behavior attributes
        self.hunting_mode = True  # Active hunting vs passive waiting
        self.terrain_map = {}     # Map of discovered URLs and their relationships
        self.prey_scent = set()   # URLs that seem promising (high link density, etc.)
        self.explored_areas = set()  # Already visited URLs
        self.current_depth = 0
        
        # Crawling state
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent or 'Alopecosa-Fabrilis-Crawler/1.0 (Spider-inspired Web Crawler)'
        })
        
        # Results storage
        self.results: List[CrawlResult] = []
        self.url_queue = deque([(base_url, 0)])  # (url, depth)
        self.visited_urls: Set[str] = set()
        
        # Adaptive behavior
        self.success_rate = 0.0
        self.avg_response_time = 0.0
        self.link_density_threshold = 5  # Minimum links to consider area "rich"
        
        # Setup logging
        self._setup_logging()
        
        # Load robots.txt if respecting robots
        if self.respect_robots:
            self._load_robots_txt()
    
    def _setup_logging(self):
        """Setup logging for the crawler"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('alopecosa_crawler.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _load_robots_txt(self):
        """Load and parse robots.txt file"""
        try:
            robots_url = urljoin(self.base_url, '/robots.txt')
            response = self.session.get(robots_url, timeout=10)
            if response.status_code == 200:
                self.logger.info("Robots.txt loaded successfully")
                # Simple robots.txt parsing - could be enhanced
                self.robots_content = response.text
            else:
                self.robots_content = ""
        except Exception as e:
            self.logger.warning(f"Could not load robots.txt: {e}")
            self.robots_content = ""
    
    def _is_allowed_url(self, url: str) -> bool:
        """Check if URL is allowed according to robots.txt and domain restrictions"""
        parsed = urlparse(url)
        
        # Check domain restriction
        if parsed.netloc != self.domain:
            return False
        
        # Check robots.txt (simplified)
        if self.respect_robots and self.robots_content:
            if 'Disallow: /' in self.robots_content:
                return False
        
        # Avoid common non-content URLs
        excluded_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mp3'}
        if any(url.lower().endswith(ext) for ext in excluded_extensions):
            return False
        
        return True
    
    def _hunt_for_prey(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """
        Hunt for promising URLs like the spider hunts for prey.
        Identifies URLs that seem "rich" in content or links.
        """
        links = []
        link_elements = soup.find_all('a', href=True)
        
        for link in link_elements:
            href = link.get('href')
            absolute_url = urljoin(current_url, href)
            
            if not self._is_allowed_url(absolute_url):
                continue
            
            # Spider-like prey detection: look for "rich" areas
            link_text = link.get_text(strip=True)
            link_count = len(link.find_all('a')) if link.find_all('a') else 0
            
            # If this link leads to an area with many sub-links, it's promising
            if link_count > self.link_density_threshold:
                self.prey_scent.add(absolute_url)
                self.logger.info(f"Found rich hunting ground: {absolute_url} (links: {link_count})")
            
            links.append(absolute_url)
        
        return links
    
    def _adapt_hunting_strategy(self):
        """Adapt the crawling strategy based on current success rate"""
        if self.success_rate < 0.5:
            # If success rate is low, be more selective
            self.link_density_threshold = max(3, self.link_density_threshold - 1)
            self.logger.info(f"Adapting: Lowering link density threshold to {self.link_density_threshold}")
        elif self.success_rate > 0.8:
            # If success rate is high, be more aggressive
            self.link_density_threshold = min(10, self.link_density_threshold + 1)
            self.logger.info(f"Adapting: Raising link density threshold to {self.link_density_threshold}")
    
    def _crawl_page(self, url: str, depth: int) -> Optional[CrawlResult]:
        """Crawl a single page and extract information"""
        if url in self.visited_urls:
            return None
        
        self.visited_urls.add(url)
        start_time = time.time()
        
        try:
            # Spider-like behavior: random delay to avoid detection
            delay = random.uniform(*self.delay_range)
            time.sleep(delay)
            
            self.logger.info(f"Crawling {url} at depth {depth}")
            response = self.session.get(url, timeout=15)
            
            if response.status_code != 200:
                self.logger.warning(f"Failed to crawl {url}: Status {response.status_code}")
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else "No Title"
            
            # Extract main content (simplified)
            content = ""
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            if main_content:
                content = main_content.get_text(strip=True)
            else:
                # Fallback: get all text from body
                body = soup.find('body')
                if body:
                    content = body.get_text(strip=True)
            
            # Hunt for links (spider behavior)
            links = self._hunt_for_prey(soup, url)
            
            # Update terrain map
            self.terrain_map[url] = {
                'depth': depth,
                'link_count': len(links),
                'title': title_text,
                'discovered_at': datetime.now().isoformat()
            }
            
            crawl_time = time.time() - start_time
            
            result = CrawlResult(
                url=url,
                title=title_text,
                content=content[:1000],  # Limit content length
                links=links,
                status_code=response.status_code,
                crawl_time=crawl_time,
                timestamp=datetime.now(),
                metadata={
                    'depth': depth,
                    'link_count': len(links),
                    'response_time': response.elapsed.total_seconds()
                }
            )
            
            self.results.append(result)
            self.logger.info(f"Successfully crawled {url} in {crawl_time:.2f}s")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error crawling {url}: {e}")
            return None
    
    def crawl(self) -> List[CrawlResult]:
        """Main crawling method - mimics spider's hunting behavior"""
        self.logger.info(f"Starting Alopecosa Fabrilis crawler on {self.base_url}")
        self.logger.info(f"Max depth: {self.max_depth}, Max pages: {self.max_pages}")
        
        pages_crawled = 0
        
        while self.url_queue and pages_crawled < self.max_pages:
            current_url, depth = self.url_queue.popleft()
            
            if depth > self.max_depth:
                continue
            
            result = self._crawl_page(current_url, depth)
            if result:
                pages_crawled += 1
                
                # Add new URLs to queue (spider exploring new territory)
                for link in result.links:
                    if link not in self.visited_urls and link not in [url for url, _ in self.url_queue]:
                        self.url_queue.append((link, depth + 1))
                
                # Prioritize URLs with high prey scent (rich areas)
                if self.prey_scent:
                    # Move some high-value URLs to front of queue
                    high_value_urls = list(self.prey_scent)[:3]
                    for url in high_value_urls:
                        if url not in self.visited_urls and url not in [u for u, _ in self.url_queue]:
                            self.url_queue.appendleft((url, depth + 1))
                    self.prey_scent.clear()
                
                # Adaptive behavior
                if pages_crawled % 10 == 0:
                    self._adapt_hunting_strategy()
        
        self.logger.info(f"Crawling completed. Crawled {pages_crawled} pages.")
        return self.results
    
    def save_results(self, filename: str = None):
        """Save crawling results to a file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"alopecosa_crawl_results_{timestamp}.json"
        
        # Convert results to serializable format
        serializable_results = []
        for result in self.results:
            serializable_results.append({
                'url': result.url,
                'title': result.title,
                'content': result.content,
                'links': result.links,
                'status_code': result.status_code,
                'crawl_time': result.crawl_time,
                'timestamp': result.timestamp.isoformat(),
                'metadata': result.metadata
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'crawl_info': {
                    'base_url': self.base_url,
                    'max_depth': self.max_depth,
                    'max_pages': self.max_pages,
                    'pages_crawled': len(self.results),
                    'crawl_timestamp': datetime.now().isoformat()
                },
                'terrain_map': self.terrain_map,
                'results': serializable_results
            }, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Results saved to {filename}")
    
    def get_crawl_statistics(self) -> Dict:
        """Get statistics about the crawling session"""
        if not self.results:
            return {}
        
        total_links = sum(len(result.links) for result in self.results)
        avg_links = total_links / len(self.results)
        avg_crawl_time = sum(result.crawl_time for result in self.results) / len(self.results)
        
        return {
            'total_pages': len(self.results),
            'total_links_discovered': total_links,
            'average_links_per_page': avg_links,
            'average_crawl_time': avg_crawl_time,
            'success_rate': len([r for r in self.results if r.status_code == 200]) / len(self.results),
            'terrain_coverage': len(self.terrain_map),
            'hunting_efficiency': len(self.prey_scent)
        }


def main():
    """Main function to demonstrate the crawler"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Alopecosa Fabrilis Web Crawler')
    parser.add_argument('url', help='Starting URL to crawl')
    parser.add_argument('--depth', type=int, default=3, help='Maximum crawl depth')
    parser.add_argument('--pages', type=int, default=50, help='Maximum pages to crawl')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    parser.add_argument('--output', help='Output filename for results')
    
    args = parser.parse_args()
    
    # Create and run the crawler
    crawler = AlopecosaCrawler(
        base_url=args.url,
        max_depth=args.depth,
        max_pages=args.pages,
        delay_range=(args.delay, args.delay * 2)
    )
    
    try:
        results = crawler.crawl()
        print(f"\nCrawling completed! Crawled {len(results)} pages.")
        
        # Show statistics
        stats = crawler.get_crawl_statistics()
        print("\nCrawl Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        # Save results
        crawler.save_results(args.output)
        
    except KeyboardInterrupt:
        print("\nCrawling interrupted by user.")
        crawler.save_results(args.output)
    except Exception as e:
        print(f"Error during crawling: {e}")


if __name__ == "__main__":
    main()
