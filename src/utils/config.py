"""
Configuration file for the Alopecosa Fabrilis Web Crawler
"""

import os

# Database Configuration
DATABASE_CONFIG = {
    'database_path': os.path.join('data', 'crawler_database.db'),
    'enable_fts': True,            # Enable full-text search
    'max_results': 1000,           # Maximum search results
    'cleanup_interval': 86400      # Cleanup interval (seconds)
}

# Crawler Behavior Settings
CRAWLER_CONFIG = {
    # Basic crawling parameters
    'default_max_depth': 3,
    'default_max_pages': 100,
    'default_delay_range': (1, 3),
    
    # Spider-like behavior settings
    'hunting_mode': True,
    'adaptive_behavior': True,
    'prey_detection': True,
    'terrain_mapping': True,
    
    # Performance settings
    'timeout': 15,
    'max_retries': 3,
    'concurrent_requests': 1,  # Keep at 1 for spider-like behavior
    
    # Content extraction settings
    'max_content_length': 1000,
    'extract_images': False,
    'extract_metadata': True,
    
    # Respectful crawling
    'respect_robots_txt': True,
    'user_agent': 'Alopecosa-Fabrilis-Crawler/1.0 (Spider-inspired Web Crawler)',
    
    # File extensions to avoid
    'excluded_extensions': {
        '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg',
        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm',
        '.mp3', '.wav', '.flac', '.aac', '.ogg',
        '.zip', '.rar', '.7z', '.tar', '.gz',
        '.exe', '.msi', '.dmg', '.deb', '.rpm',
        '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'
    },
    
    # Content types to focus on
    'preferred_content_types': {
        'text/html',
        'application/xhtml+xml'
    }
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': os.path.join('data', 'alopecosa_crawler.log'),
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Output Configuration
OUTPUT_CONFIG = {
    'default_format': 'json',
    'include_metadata': True,
    'include_terrain_map': True,
    'compress_output': False,
    'output_directory': os.path.join('data', 'crawl_results')
}

# Spider Behavior Patterns
SPIDER_PATTERNS = {
    # Hunting behavior
    'prey_detection_threshold': 5,  # Minimum links to consider area "rich"
    'hunting_aggression': 0.7,      # 0.0 = passive, 1.0 = aggressive
    
    # Movement patterns
    'exploration_strategy': 'depth_first',  # 'depth_first', 'breadth_first', 'adaptive'
    'territory_mapping': True,
    'scent_trail_length': 10,
    
    # Adaptation
    'learning_rate': 0.1,
    'success_threshold': 0.8,
    'failure_threshold': 0.3
}
