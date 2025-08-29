"""
Alopecosa Fabrilis Web Crawler - Main Package
A sophisticated web crawling system inspired by spider behavior
"""

from .crawler.alopecosa_crawler import AlopecosaCrawler
from .database.database_manager import DatabaseManager
from .batch_scraper.batch_url_scraper import BatchURLScraper
from .utils.config import CRAWLER_CONFIG, DATABASE_CONFIG

__version__ = "1.0.0"
__author__ = "Alopecosa Fabrilis Team"
__description__ = "Spider-inspired web crawling system"

__all__ = [
    'AlopecosaCrawler',
    'DatabaseManager', 
    'BatchURLScraper',
    'CRAWLER_CONFIG',
    'DATABASE_CONFIG'
]
