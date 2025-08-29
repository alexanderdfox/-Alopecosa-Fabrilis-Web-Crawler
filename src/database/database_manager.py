#!/usr/bin/env python3
"""
Database Manager for Alopecosa Fabrilis Web Crawler
Manages SQLite database for storing crawled websites and search functionality
"""

import sqlite3
import logging
import os
import hashlib
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages SQLite database for storing crawled websites and search functionality"""
    
    def __init__(self, db_path: str = None):
        """
        Initialize the database manager
        
        Args:
            db_path: Path to the database file. If None, uses default from config.
        """
        if db_path is None:
            # Import config here to avoid circular imports
            try:
                from ..utils.config import DATABASE_CONFIG
                db_path = DATABASE_CONFIG['database_path']
            except ImportError:
                # Fallback to absolute import
                try:
                    from src.utils.config import DATABASE_CONFIG
                    db_path = DATABASE_CONFIG['database_path']
                except ImportError:
                    # Final fallback to data folder
                    db_path = os.path.join('data', 'crawler_database.db')
        
        self.db_path = db_path
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create websites table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS websites (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT UNIQUE NOT NULL,
                        title TEXT,
                        content TEXT,
                        content_hash TEXT UNIQUE,
                        status_code INTEGER,
                        crawl_time REAL,
                        crawl_timestamp TEXT,
                        domain TEXT,
                        depth INTEGER,
                        links_count INTEGER,
                        metadata TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create links table for relationship tracking
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS links (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        source_website_id INTEGER,
                        target_url TEXT,
                        link_text TEXT,
                        FOREIGN KEY (source_website_id) REFERENCES websites (id)
                    )
                ''')
                
                # Create crawl_sessions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS crawl_sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_name TEXT,
                        base_url TEXT,
                        max_depth INTEGER,
                        max_pages INTEGER,
                        pages_crawled INTEGER,
                        start_time TEXT,
                        end_time TEXT,
                        status TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create search_index table for full-text search
                cursor.execute('''
                    CREATE VIRTUAL TABLE IF NOT EXISTS search_index 
                    USING fts5(url, title, content, domain)
                ''')
                
                # Create indexes for better performance
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_websites_domain ON websites(domain)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_websites_depth ON websites(depth)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_websites_timestamp ON websites(crawl_timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_links_source ON links(source_website_id)')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def store_crawl_results(self, session_name: str, base_url: str, max_depth: int, 
                           max_pages: int, results: List, start_time: datetime, 
                           end_time: datetime, status: str = 'completed') -> int:
        """Store crawl results in the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Insert crawl session
                cursor.execute('''
                    INSERT INTO crawl_sessions 
                    (session_name, base_url, max_depth, max_pages, pages_crawled, start_time, end_time, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (session_name, base_url, max_depth, max_pages, len(results), 
                     start_time.isoformat(), end_time.isoformat(), status))
                
                session_id = cursor.lastrowid
                
                # Store each website
                for result in results:
                    # Generate content hash to avoid duplicates
                    content_hash = hashlib.md5(result.content.encode('utf-8')).hexdigest()
                    
                    # Check if website already exists
                    cursor.execute('SELECT id FROM websites WHERE content_hash = ?', (content_hash,))
                    existing = cursor.fetchone()
                    
                    if existing:
                        # Update existing record
                        cursor.execute('''
                            UPDATE websites SET 
                            crawl_time = ?, crawl_timestamp = ?, links_count = ?, metadata = ?
                            WHERE content_hash = ?
                        ''', (result.crawl_time, result.timestamp.isoformat(), 
                              len(result.links), json.dumps(result.metadata), content_hash))
                        website_id = existing[0]
                    else:
                        # Insert new website
                        cursor.execute('''
                            INSERT INTO websites 
                            (url, title, content, content_hash, status_code, crawl_time, 
                             crawl_timestamp, domain, depth, links_count, metadata)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            result.url, result.title, result.content, content_hash,
                            result.status_code, result.crawl_time, result.timestamp.isoformat(),
                            self._extract_domain(result.url), result.metadata.get('depth', 0),
                            len(result.links), json.dumps(result.metadata)
                        ))
                        website_id = cursor.lastrowid
                        
                        # Insert into search index
                        cursor.execute('''
                            INSERT INTO search_index (url, title, content, domain)
                            VALUES (?, ?, ?, ?)
                        ''', (result.url, result.title, result.content, 
                              self._extract_domain(result.url)))
                    
                    # Store links
                    for link in result.links:
                        cursor.execute('''
                            INSERT INTO links (source_website_id, target_url, link_text)
                            VALUES (?, ?, ?)
                        ''', (website_id, link, ''))  # link_text could be extracted if needed
                
                conn.commit()
                logger.info(f"Stored {len(results)} websites in database")
                return session_id
                
        except Exception as e:
            logger.error(f"Error storing crawl results: {e}")
            raise
    
    def search_websites(self, query: str, filters: Dict = None, 
                        limit: int = 50, offset: int = 0) -> Tuple[List[Dict], int]:
        """Search websites using full-text search with optional filters"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build base query
                base_sql = '''
                    SELECT w.id, w.url, w.title, w.content, w.status_code, 
                           w.crawl_time, w.crawl_timestamp, w.domain, w.depth, 
                           w.links_count, w.metadata
                    FROM websites w
                '''
                
                where_conditions = []
                params = []
                
                # Full-text search using FTS5
                if query and query.strip():
                    base_sql += ' JOIN search_index si ON w.url = si.url'
                    where_conditions.append('si.search_index MATCH ?')
                    params.append(query)
                
                # Apply filters
                if filters:
                    if 'domain' in filters and filters['domain']:
                        where_conditions.append('w.domain = ?')
                        params.append(filters['domain'])
                    
                    if 'depth' in filters and filters['depth'] is not None:
                        where_conditions.append('w.depth = ?')
                        params.append(filters['depth'])
                    
                    if 'status_code' in filters and filters['status_code']:
                        where_conditions.append('w.status_code = ?')
                        params.append(filters['status_code'])
                
                # Build WHERE clause
                if where_conditions:
                    base_sql += ' WHERE ' + ' AND '.join(where_conditions)
                
                # Get total count
                count_sql = f"SELECT COUNT(*) FROM ({base_sql})"
                cursor.execute(count_sql, params)
                total_count = cursor.fetchone()[0]
                
                # Add ordering and pagination
                search_sql = base_sql + ' ORDER BY w.crawl_timestamp DESC LIMIT ? OFFSET ?'
                params.extend([limit, offset])
                
                cursor.execute(search_sql, params)
                results = []
                
                for row in cursor.fetchall():
                    website = {
                        'id': row[0],
                        'url': row[1] or '',
                        'title': row[2] or 'No Title',
                        'content': (row[3][:500] + '...') if row[3] and len(row[3]) > 500 else (row[3] or 'No content'),
                        'status_code': row[4] or 0,
                        'crawl_time': row[5] or 0.0,
                        'crawl_timestamp': row[6] or '',
                        'domain': row[7] or 'Unknown',
                        'depth': row[8] or 0,
                        'links_count': row[9] or 0,
                        'metadata': json.loads(row[10]) if row[10] else {}
                    }
                    results.append(website)
                
                return results, total_count
                
        except Exception as e:
            logger.error(f"Error searching websites: {e}")
            # Return empty results on error instead of raising
            return [], 0
    
    def get_website_details(self, website_id: int) -> Optional[Dict]:
        """Get detailed information about a specific website"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT w.*, GROUP_CONCAT(l.target_url) as outgoing_links
                    FROM websites w
                    LEFT JOIN links l ON w.id = l.source_website_id
                    WHERE w.id = ?
                    GROUP BY w.id
                ''', (website_id,))
                
                row = cursor.fetchone()
                if row:
                    website = {
                        'id': row[0],
                        'url': row[1] or '',
                        'title': row[2] or 'No Title',
                        'content': row[3] or 'No content',
                        'content_hash': row[4] or '',
                        'status_code': row[5] or 0,
                        'crawl_time': row[6] or 0.0,
                        'crawl_timestamp': row[7] or '',
                        'domain': row[8] or 'Unknown',
                        'depth': row[9] or 0,
                        'links_count': row[10] or 0,
                        'metadata': json.loads(row[11]) if row[11] else {},
                        'created_at': row[12] or '',
                        'outgoing_links': row[13].split(',') if row[13] else []
                    }
                    return website
                return None
                
        except Exception as e:
            logger.error(f"Error getting website details: {e}")
            return None
    
    def get_domains(self) -> List[str]:
        """Get list of all domains in the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT DISTINCT domain FROM websites ORDER BY domain')
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting domains: {e}")
            return []
    
    def get_crawl_sessions(self, limit: int = 50) -> List[Dict]:
        """Get list of crawl sessions"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM crawl_sessions 
                    ORDER BY created_at DESC 
                    LIMIT ?
                ''', (limit,))
                
                columns = [description[0] for description in cursor.description]
                sessions = []
                
                for row in cursor.fetchall():
                    session = dict(zip(columns, row))
                    sessions.append(session)
                
                return sessions
                
        except Exception as e:
            logger.error(f"Error getting crawl sessions: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Total websites
                cursor.execute('SELECT COUNT(*) FROM websites')
                stats['total_websites'] = cursor.fetchone()[0]
                
                # Total links
                cursor.execute('SELECT COUNT(*) FROM links')
                stats['total_links'] = cursor.fetchone()[0]
                
                # Total sessions
                cursor.execute('SELECT COUNT(*) FROM crawl_sessions')
                stats['total_sessions'] = cursor.fetchone()[0]
                
                # Domains count
                cursor.execute('SELECT COUNT(DISTINCT domain) FROM websites')
                stats['unique_domains'] = cursor.fetchone()[0]
                
                # Average content length
                cursor.execute('SELECT AVG(LENGTH(content)) FROM websites')
                stats['avg_content_length'] = cursor.fetchone()[0] or 0
                
                # Recent activity
                cursor.execute('''
                    SELECT COUNT(*) FROM websites 
                    WHERE crawl_timestamp > datetime('now', '-7 days')
                ''')
                stats['websites_last_7_days'] = cursor.fetchone()[0]
                
                return stats
                
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
    
    def delete_old_data(self, days_old: int = 30) -> int:
        """Delete websites older than specified days"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Delete old websites
                cursor.execute('''
                    DELETE FROM websites 
                    WHERE crawl_timestamp < datetime('now', '-{} days')
                '''.format(days_old))
                
                deleted_count = cursor.rowcount
                
                # Clean up orphaned links
                cursor.execute('''
                    DELETE FROM links 
                    WHERE source_website_id NOT IN (SELECT id FROM websites)
                ''')
                
                # Clean up search index
                cursor.execute('DELETE FROM search_index')
                cursor.execute('''
                    INSERT INTO search_index (url, title, content, domain)
                    SELECT url, title, content, domain FROM websites
                ''')
                
                conn.commit()
                logger.info(f"Deleted {deleted_count} old websites")
                return deleted_count
                
        except Exception as e:
            logger.error(f"Error deleting old data: {e}")
            return 0
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return url
    
    def close(self):
        """Close database connection"""
        pass  # SQLite handles connections automatically

# Global database manager instance
db_manager = DatabaseManager()  # Will use default path from config (data/crawler_database.db)
