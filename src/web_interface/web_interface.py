#!/usr/bin/env python3
"""
Alopecosa Fabrilis Web Crawler - Web Interface
A beautiful, modern web interface for controlling and monitoring the spider-inspired crawler
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import threading
import time
import json
import os
from datetime import datetime
import queue
try:
    # Try relative imports first (when running as package)
    from ..crawler.alopecosa_crawler import AlopecosaCrawler
    from ..database.database_manager import db_manager
    from ..batch_scraper.batch_url_scraper import BatchURLScraper
    from ..utils.config import CRAWLER_CONFIG
except ImportError:
    # Fall back to absolute imports (when running from project root)
    from src.crawler.alopecosa_crawler import AlopecosaCrawler
    from src.database.database_manager import db_manager
    from src.batch_scraper.batch_url_scraper import BatchURLScraper
    from src.utils.config import CRAWLER_CONFIG
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the project root directory (where templates are located)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
template_dir = os.path.join(project_root, 'templates')

app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = 'alopecosa-fabrilis-spider-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for crawler management
active_crawlers = {}
crawler_queue = queue.Queue()
crawler_results = {}

class WebCrawlerManager:
    """Manages crawler instances and provides web interface functionality"""
    
    def __init__(self):
        self.crawlers = {}
        self.crawl_history = []
        self.max_history = 50
    
    def create_crawler(self, name, base_url, max_depth=3, max_pages=100, delay_range=(1, 3)):
        """Create a new crawler instance"""
        try:
            # Validate inputs
            if not name or not isinstance(name, str):
                return None, "Invalid crawler name"
            
            if not base_url or not isinstance(base_url, str):
                return None, "Invalid base URL"
            
            if not isinstance(max_depth, int) or max_depth < 1 or max_depth > 10:
                return None, "Max depth must be between 1 and 10"
            
            if not isinstance(max_pages, int) or max_pages < 1 or max_pages > 10000:
                return None, "Max pages must be between 1 and 10000"
            
            if not isinstance(delay_range, (tuple, list)) or len(delay_range) != 2:
                return None, "Delay range must be a tuple of two numbers"
            
            crawler = AlopecosaCrawler(
                base_url=base_url,
                max_depth=max_depth,
                max_pages=max_pages,
                delay_range=delay_range
            )
            
            crawler_id = f"crawler_{int(time.time())}_{name}"
            self.crawlers[crawler_id] = {
                'instance': crawler,
                'name': name,
                'base_url': base_url,
                'status': 'ready',
                'progress': 0,
                'start_time': None,
                'end_time': None,
                'results': [],
                'stats': {},
                'logs': []
            }
            
            return crawler_id, "Crawler created successfully"
        except Exception as e:
            logger.error(f"Error creating crawler: {e}")
            return None, f"Error creating crawler: {str(e)}"
    
    def start_crawler(self, crawler_id):
        """Start a crawler in a separate thread"""
        try:
            if not crawler_id or not isinstance(crawler_id, str):
                return False, "Invalid crawler ID"
            
            if crawler_id not in self.crawlers:
                return False, "Crawler not found"
            
            crawler_info = self.crawlers[crawler_id]
            if crawler_info['status'] in ['running', 'completed']:
                return False, "Crawler already running or completed"
            
            # Start crawler in background thread
            thread = threading.Thread(
                target=self._run_crawler,
                args=(crawler_id,),
                daemon=True
            )
            thread.start()
            
            return True, "Crawler started successfully"
        except Exception as e:
            logger.error(f"Error starting crawler {crawler_id}: {e}")
            return False, f"Error starting crawler: {str(e)}"
    
    def _run_crawler(self, crawler_id):
        """Run the crawler and update status"""
        crawler_info = self.crawlers[crawler_id]
        crawler = crawler_info['instance']
        
        try:
            # Update status
            crawler_info['status'] = 'running'
            crawler_info['start_time'] = datetime.now()
            crawler_info['progress'] = 0
            
            # Emit status update
            socketio.emit('crawler_status', {
                'crawler_id': crawler_id,
                'status': 'running',
                'progress': 0
            })
            
            # Start crawling
            results = crawler.crawl()
            
            # Update results and stats
            crawler_info['results'] = results
            crawler_info['stats'] = crawler.get_crawl_statistics()
            crawler_info['status'] = 'completed'
            crawler_info['end_time'] = datetime.now()
            crawler_info['progress'] = 100
            
            # Store results in database
            try:
                logger.info(f"Attempting to store {len(results)} results in database for crawler {crawler_id}")
                logger.info(f"Results type: {type(results)}")
                if results:
                    logger.info(f"First result type: {type(results[0])}")
                    logger.info(f"First result attributes: {dir(results[0])}")
                
                session_id = db_manager.store_crawl_results(
                    session_name=crawler_info['name'],
                    base_url=crawler_info['base_url'],
                    max_depth=crawler.instance.max_depth,
                    max_pages=crawler.instance.max_pages,
                    results=results,
                    start_time=crawler_info['start_time'],
                    end_time=crawler_info['end_time'],
                    status='completed'
                )
                crawler_info['session_id'] = session_id
                logger.info(f"Successfully stored crawl results in database with session ID: {session_id}")
            except Exception as e:
                logger.error(f"Error storing results in database: {e}")
                import traceback
                logger.error(f"Database storage traceback: {traceback.format_exc()}")
                crawler_info['session_id'] = None
            
            # Add to history
            self._add_to_history(crawler_id)
            
            # Emit completion
            socketio.emit('crawler_completed', {
                'crawler_id': crawler_id,
                'results_count': len(results),
                'stats': crawler_info['stats']
            })
            
        except Exception as e:
            crawler_info['status'] = 'error'
            crawler_info['end_time'] = datetime.now()
            crawler_info['logs'].append(f"Error: {str(e)}")
            
            socketio.emit('crawler_error', {
                'crawler_id': crawler_id,
                'error': str(e)
            })
    
    def _add_to_history(self, crawler_id):
        """Add completed crawler to history"""
        crawler_info = self.crawlers[crawler_id]
        
        history_entry = {
            'id': crawler_id,
            'name': crawler_info['name'],
            'base_url': crawler_info['base_url'],
            'start_time': crawler_info['start_time'],
            'end_time': crawler_info['end_time'],
            'status': crawler_info['status'],
            'results_count': len(crawler_info['results']),
            'stats': crawler_info['stats']
        }
        
        self.crawl_history.insert(0, history_entry)
        
        # Keep only recent history
        if len(self.crawl_history) > self.max_history:
            self.crawl_history = self.crawl_history[:self.max_history]
    
    def get_crawler_status(self, crawler_id):
        """Get current status of a crawler"""
        try:
            if not crawler_id or not isinstance(crawler_id, str):
                return None
            
            if crawler_id not in self.crawlers:
                return None
            return self.crawlers[crawler_id]
        except Exception as e:
            logger.error(f"Error getting crawler status {crawler_id}: {e}")
            return None
    
    def get_all_crawlers(self):
        """Get all crawler instances"""
        return self.crawlers
    
    def get_crawl_history(self):
        """Get crawl history"""
        return self.crawl_history
    
    def delete_crawler(self, crawler_id):
        """Delete a crawler instance"""
        try:
            if not crawler_id or not isinstance(crawler_id, str):
                return False
            
            if crawler_id in self.crawlers:
                del self.crawlers[crawler_id]
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting crawler {crawler_id}: {e}")
            return False
    
    def save_results(self, crawler_id, filename=None):
        """Save crawler results to database (and optionally to file)"""
        logger.info(f"Attempting to save results for crawler {crawler_id}")
        
        if crawler_id not in self.crawlers:
            logger.error(f"Crawler {crawler_id} not found in crawlers dict")
            return False, "Crawler not found"
        
        crawler_info = self.crawlers[crawler_id]
        logger.info(f"Crawler info: {crawler_info['name']}, status: {crawler_info['status']}")
        
        # Check if crawler has results
        if not crawler_info.get('results'):
            logger.warning(f"Crawler {crawler_id} has no results key")
            return False, "No results to save - crawler may not have completed"
        
        # Check if results list is empty
        if len(crawler_info['results']) == 0:
            logger.warning(f"Crawler {crawler_id} has empty results list")
            return False, "No results to save - crawler completed but found no pages"
        
        logger.info(f"Crawler {crawler_id} has {len(crawler_info['results'])} results to save")
        
        try:
            # Check if results are already in database
            if crawler_info.get('session_id'):
                logger.info(f"Results already saved to database with session ID: {crawler_info['session_id']}")
                return True, f"Results already saved to database (Session ID: {crawler_info['session_id']})"
            else:
                # Try to store results in database now as a fallback
                logger.warning(f"Crawler {crawler_id} completed but has no session_id, attempting fallback storage")
                
                try:
                    session_id = db_manager.store_crawl_results(
                        session_name=crawler_info['name'],
                        base_url=crawler_info['base_url'],
                        max_depth=crawler_info['instance'].max_depth,
                        max_pages=crawler_info['instance'].max_pages,
                        results=crawler_info['results'],
                        start_time=crawler_info['start_time'],
                        end_time=crawler_info['end_time'],
                        status='completed'
                    )
                    crawler_info['session_id'] = session_id
                    logger.info(f"Fallback database storage successful with session ID: {session_id}")
                    return True, f"Results saved to database (Session ID: {session_id})"
                except Exception as fallback_error:
                    logger.error(f"Fallback database storage failed: {fallback_error}")
                    # As a last resort, save to JSON file
                    return self._save_to_json_fallback(crawler_id, crawler_info)
            
        except Exception as e:
            logger.error(f"Error checking database for crawler {crawler_id}: {e}")
            return False, f"Error checking database: {str(e)}"
    
    def _save_to_json_fallback(self, crawler_id, crawler_info):
        """Fallback method to save results to JSON file if database fails"""
        try:
            import os
            import json
            
            # Create results directory
            results_dir = "crawl_results"
            if not os.path.exists(results_dir):
                os.makedirs(results_dir)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fallback_crawl_{crawler_info['name']}_{timestamp}.json"
            filepath = os.path.join(results_dir, filename)
            
            # Convert results to serializable format
            serializable_results = []
            for result in crawler_info['results']:
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
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'crawl_info': {
                        'name': crawler_info['name'],
                        'base_url': crawler_info['base_url'],
                        'max_depth': crawler_info['instance'].max_depth,
                        'max_pages': crawler_info['instance'].max_pages,
                        'pages_crawled': len(crawler_info['results']),
                        'crawl_timestamp': crawler_info['end_time'].isoformat() if crawler_info['end_time'] else datetime.now().isoformat(),
                        'status': crawler_info['status'],
                        'note': 'Saved as fallback due to database storage failure'
                    },
                    'statistics': crawler_info['stats'],
                    'results': serializable_results
                }, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Fallback JSON save successful: {filepath}")
            return True, f"Results saved to JSON file as fallback: {filename}"
            
        except Exception as e:
            logger.error(f"Fallback JSON save failed: {e}")
            return False, f"Fallback save failed: {str(e)}"
    
    def start_batch_scrape(self, urls, config=None):
        """Start a batch scrape operation"""
        try:
            if not urls or not isinstance(urls, list):
                return None, "Invalid URLs list"
            
            if len(urls) == 0:
                return None, "URLs list is empty"
            
            # Create batch scraper
            batch_scraper = BatchURLScraper(
                max_workers=3,
                delay_between_crawls=2.0
            )
            
            # Start batch scrape in background thread
            thread = threading.Thread(
                target=self._run_batch_scrape,
                args=(batch_scraper, urls, config),
                daemon=True
            )
            thread.start()
            
            batch_id = f"batch_{int(time.time())}"
            return batch_id, "Batch scrape started successfully"
            
        except Exception as e:
            logger.error(f"Error starting batch scrape: {e}")
            return None, f"Error starting batch scrape: {str(e)}"
    
    def _run_batch_scrape(self, batch_scraper, urls, config):
        """Run the batch scrape operation"""
        try:
            logger.info(f"Starting batch scrape of {len(urls)} URLs")
            
            # Run batch scrape
            results = batch_scraper.scrape_urls(urls, config)
            
            # Store results in database (already handled by batch scraper)
            logger.info(f"Batch scrape completed: {results['summary']['successful']} successful, {results['summary']['failed']} failed")
            
            # Emit completion event
            socketio.emit('batch_scrape_completed', {
                'summary': results['summary'],
                'total_urls': len(urls)
            })
            
        except Exception as e:
            logger.error(f"Batch scrape failed: {e}")
            socketio.emit('batch_scrape_error', {
                'error': str(e)
            })
    
    def get_saved_files(self):
        """Get list of saved crawl sessions from database"""
        try:
            # Get crawl sessions from database instead of JSON files
            sessions = db_manager.get_crawl_sessions(limit=100)
            
            files = []
            for session in sessions:
                files.append({
                    'filename': f"Session: {session['session_name']}",
                    'size': session['pages_crawled'],
                    'modified': session['created_at'],
                    'session_id': session['id'],
                    'base_url': session['base_url'],
                    'status': session['status'],
                    'max_depth': session['max_depth'],
                    'max_pages': session['max_pages']
                })
            
            # Sort by creation time (newest first)
            files.sort(key=lambda x: x['created_at'], reverse=True)
            return files
        except Exception as e:
            logger.error(f"Error getting saved sessions from database: {e}")
            return []

# Initialize crawler manager
crawler_manager = WebCrawlerManager()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/database')
def database():
    """Database search interface page"""
    return render_template('database.html')

@app.route('/search')
def search():
    """Search interface page"""
    return render_template('search.html')

@app.route('/batch')
def batch():
    """Batch processing interface page"""
    return render_template('batch.html')

@app.route('/api/crawlers', methods=['GET'])
def get_crawlers():
    """API endpoint to get all crawlers"""
    crawlers = crawler_manager.get_all_crawlers()
    
    # Convert crawler objects to serializable format
    serializable_crawlers = {}
    for crawler_id, crawler_info in crawlers.items():
        serializable_crawlers[crawler_id] = {
            'name': crawler_info['name'],
            'base_url': crawler_info['base_url'],
            'status': crawler_info['status'],
            'progress': crawler_info['progress'],
            'start_time': crawler_info['start_time'].isoformat() if crawler_info['start_time'] else None,
            'end_time': crawler_info['end_time'].isoformat() if crawler_info['end_time'] else None,
            'results_count': len(crawler_info['results']),
            'stats': crawler_info['stats'],
            'logs': crawler_info['logs'],
            'config': {
                'max_depth': crawler_info['instance'].max_depth,
                'max_pages': crawler_info['instance'].max_pages,
                'delay_range': crawler_info['instance'].delay_range
            }
        }
    
    return jsonify(serializable_crawlers)

@app.route('/api/crawlers', methods=['POST'])
def create_crawler():
    """API endpoint to create a new crawler"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        name = data.get('name', 'Unnamed Crawler')
        base_url = data.get('base_url')
        max_depth = int(data.get('max_depth', 3))
        max_pages = int(data.get('max_pages', 100))
        delay = float(data.get('delay', 1.0))
        
        if not base_url:
            return jsonify({'success': False, 'error': 'Base URL is required'}), 400
        
        # Validate inputs
        if max_depth < 1 or max_depth > 10:
            return jsonify({'success': False, 'error': 'Max depth must be between 1 and 10'}), 400
        
        if max_pages < 1 or max_pages > 10000:
            return jsonify({'success': False, 'error': 'Max pages must be between 1 and 10000'}), 400
        
        if delay < 0.1 or delay > 60:
            return jsonify({'success': False, 'error': 'Delay must be between 0.1 and 60 seconds'}), 400
        
        crawler_id, message = crawler_manager.create_crawler(
            name=name,
            base_url=base_url,
            max_depth=max_depth,
            max_pages=max_pages,
            delay_range=(delay, delay * 2)
        )
        
        if crawler_id:
            return jsonify({
                'success': True,
                'crawler_id': crawler_id,
                'message': message
            })
        else:
            return jsonify({'success': False, 'error': message}), 400
            
    except (ValueError, TypeError) as e:
        return jsonify({'success': False, 'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Error creating crawler: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.route('/api/crawlers/<crawler_id>/start', methods=['POST'])
def start_crawler(crawler_id):
    """API endpoint to start a crawler"""
    try:
        success, message = crawler_manager.start_crawler(crawler_id)
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': message}), 400
            
    except Exception as e:
        logger.error(f"Error starting crawler {crawler_id}: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.route('/api/crawlers/<crawler_id>/status', methods=['GET'])
def get_crawler_status(crawler_id):
    """API endpoint to get crawler status"""
    try:
        status = crawler_manager.get_crawler_status(crawler_id)
        
        if status:
            # Convert to serializable format
            serializable_status = {
                'name': status['name'],
                'base_url': status['base_url'],
                'status': status['status'],
                'progress': status['progress'],
                'start_time': status['start_time'].isoformat() if status['start_time'] else None,
                'end_time': status['end_time'].isoformat() if status['end_time'] else None,
                'results_count': len(status['results']),
                'stats': status['stats'],
                'logs': status['logs']
            }
            return jsonify(serializable_status)
        else:
            return jsonify({'error': 'Crawler not found'}), 404
            
    except Exception as e:
        logger.error(f"Error getting crawler status {crawler_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/crawlers/<crawler_id>/results', methods=['GET'])
def get_crawler_results(crawler_id):
    """API endpoint to get crawler results"""
    try:
        status = crawler_manager.get_crawler_status(crawler_id)
        
        if not status:
            return jsonify({'error': 'Crawler not found'}), 404
        
        if status['status'] != 'completed':
            return jsonify({'error': 'Crawler not completed'}), 400
        
        # Convert results to serializable format
        serializable_results = []
        for result in status['results']:
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
        
        return jsonify({
            'results': serializable_results,
            'stats': status['stats']
        })
        
    except Exception as e:
        logger.error(f"Error getting crawler results {crawler_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/crawlers/<crawler_id>/save', methods=['GET', 'POST'])
def save_crawler_results(crawler_id):
    """API endpoint to check crawler results in database"""
    logger.info(f"Database check request received for crawler {crawler_id}")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request headers: {dict(request.headers)}")
    
    try:
        # Check if crawler exists
        if crawler_id not in crawler_manager.crawlers:
            logger.error(f"Crawler {crawler_id} not found in crawler_manager.crawlers")
            return jsonify({'success': False, 'error': 'Crawler not found'}), 404
        
        # Check if crawler has completed
        crawler_info = crawler_manager.crawlers[crawler_id]
        logger.info(f"Crawler {crawler_id} status: {crawler_info['status']}")
        
        if crawler_info['status'] != 'completed':
            return jsonify({'success': False, 'error': 'Crawler has not completed yet'}), 400
        
        # Check if crawler has results
        results_count = len(crawler_info.get('results', []))
        logger.info(f"Crawler {crawler_id} has {results_count} results")
        
        if not crawler_info.get('results') or results_count == 0:
            return jsonify({'success': False, 'error': 'No results to save - crawler completed but found no pages'}), 400
        
        # Check database status
        success, message = crawler_manager.save_results(crawler_id)
        
        if success:
            logger.info(f"Successfully confirmed results in database for crawler {crawler_id}: {message}")
            return jsonify({'success': True, 'message': message})
        
        # If we get here, the save failed, so try to force a save
        logger.info(f"Attempting to force save for crawler {crawler_id}")
        success, message = crawler_manager.save_results(crawler_id)
        
        if success:
            logger.info(f"Force save successful for crawler {crawler_id}: {message}")
            return jsonify({'success': True, 'message': message})
        else:
            logger.error(f"Force save failed for crawler {crawler_id}: {message}")
            return jsonify({'success': False, 'error': message}), 400
            
    except Exception as e:
        logger.error(f"Error checking crawler results in database {crawler_id}: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'success': False, 'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/history', methods=['GET'])
def get_crawl_history():
    """API endpoint to get crawl history"""
    try:
        history = crawler_manager.get_crawl_history()
        return jsonify(history)
    except Exception as e:
        logger.error(f"Error getting crawl history: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/crawlers/<crawler_id>', methods=['DELETE'])
def delete_crawler(crawler_id):
    """API endpoint to delete a crawler"""
    try:
        success = crawler_manager.delete_crawler(crawler_id)
        
        if success:
            return jsonify({'success': True, 'message': 'Crawler deleted'})
        else:
            return jsonify({'success': False, 'error': 'Crawler not found'}), 404
            
    except Exception as e:
        logger.error(f"Error deleting crawler {crawler_id}: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

# Database API endpoints
@app.route('/api/database/search', methods=['GET'])
def search_websites():
    """API endpoint to search websites in database"""
    try:
        query = request.args.get('q', '')
        domain = request.args.get('domain', '')
        depth = request.args.get('depth', type=int)
        status_code = request.args.get('status_code', type=int)
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        filters = {}
        if domain:
            filters['domain'] = domain
        if depth is not None:
            filters['depth'] = depth
        if status_code:
            filters['status_code'] = status_code
        
        offset = (page - 1) * limit
        results, total_count = db_manager.search_websites(query, filters, limit, offset)
        
        return jsonify({
            'results': results,
            'total_count': total_count,
            'page': page,
            'limit': limit,
            'total_pages': (total_count + limit - 1) // limit
        })
        
    except Exception as e:
        logger.error(f"Error searching websites: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/database/websites/<int:website_id>', methods=['GET'])
def get_website_details(website_id):
    """API endpoint to get website details"""
    try:
        website = db_manager.get_website_details(website_id)
        
        if website:
            return jsonify(website)
        else:
            return jsonify({'error': 'Website not found'}), 404
            
    except Exception as e:
        logger.error(f"Error getting website details: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/database/domains', methods=['GET'])
def get_domains():
    """API endpoint to get all domains"""
    try:
        domains = db_manager.get_domains()
        return jsonify(domains)
        
    except Exception as e:
        logger.error(f"Error getting domains: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/database/sessions', methods=['GET'])
def get_crawl_sessions():
    """API endpoint to get crawl sessions"""
    try:
        limit = request.args.get('limit', 50, type=int)
        sessions = db_manager.get_crawl_sessions(limit)
        return jsonify(sessions)
        
    except Exception as e:
        logger.error(f"Error getting crawl sessions: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/database/statistics', methods=['GET'])
def get_database_statistics():
    """API endpoint to get database statistics"""
    try:
        stats = db_manager.get_statistics()
        return jsonify(stats)
        
    except Exception as e:
        logger.error(f"Error getting database statistics: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/database/cleanup', methods=['POST'])
def cleanup_old_data():
    """API endpoint to clean up old data"""
    try:
        data = request.get_json()
        days_old = data.get('days_old', 30) if data else 30
        
        deleted_count = db_manager.delete_old_data(days_old)
        
        return jsonify({
            'success': True,
            'message': f'Deleted {deleted_count} old websites',
            'deleted_count': deleted_count
        })
        
    except Exception as e:
        logger.error(f"Error cleaning up old data: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/saved-files', methods=['GET'])
def get_saved_files():
    """API endpoint to get list of saved result files"""
    try:
        files = crawler_manager.get_saved_files()
        return jsonify(files)
        
    except Exception as e:
        logger.error(f"Error getting saved files: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/debug/crawlers', methods=['GET'])
def debug_crawlers():
    """Debug endpoint to show current crawler state"""
    try:
        debug_info = {}
        for crawler_id, crawler_info in crawler_manager.crawlers.items():
            debug_info[crawler_id] = {
                'name': crawler_info['name'],
                'status': crawler_info['status'],
                'has_results': 'results' in crawler_info,
                'results_count': len(crawler_info.get('results', [])),
                'has_instance': 'instance' in crawler_info,
                'start_time': crawler_info.get('start_time'),
                'end_time': crawler_info.get('end_time')
            }
        
        return jsonify({
            'total_crawlers': len(debug_info),
            'crawlers': debug_info
        })
        
    except Exception as e:
        logger.error(f"Error in debug endpoint: {e}")
        return jsonify({'error': f'Debug error: {str(e)}'}), 500

# Batch Processing Endpoints
@app.route('/api/batch-scrape', methods=['POST'])
def start_batch_scrape():
    """API endpoint to start batch scraping"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        urls = data.get('urls', [])
        config = data.get('config', {})
        
        if not urls or not isinstance(urls, list):
            return jsonify({'success': False, 'error': 'URLs must be a non-empty list'}), 400
        
        # Start batch scrape
        batch_id, message = crawler_manager.start_batch_scrape(urls, config)
        
        if batch_id:
            return jsonify({
                'success': True,
                'batch_id': batch_id,
                'message': message,
                'urls_count': len(urls)
            })
        else:
            return jsonify({'success': False, 'error': message}), 400
            
    except Exception as e:
        logger.error(f"Error starting batch scrape: {e}")
        return jsonify({'success': False, 'error': f'Internal server error: {str(e)}'}), 500

@app.route('/api/batch-scrape/upload', methods=['POST'])
def upload_url_file():
    """API endpoint to upload and process URL files"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Check file type
        allowed_extensions = {'txt', 'csv', 'json'}
        if not file.filename.lower().endswith(tuple('.' + ext for ext in allowed_extensions)):
            return jsonify({'success': False, 'error': 'Invalid file type. Use .txt, .csv, or .json'}), 400
        
        # Read and parse file
        content = file.read().decode('utf-8')
        urls = []
        
        if file.filename.lower().endswith('.txt'):
            urls = [line.strip() for line in content.split('\n') if line.strip() and not line.startswith('#')]
        elif file.filename.lower().endswith('.csv'):
            import csv
            from io import StringIO
            csv_reader = csv.reader(StringIO(content))
            urls = [row[0].strip() for row in csv_reader if row and row[0].strip()]
        elif file.filename.lower().endswith('.json'):
            import json
            data = json.loads(content)
            if isinstance(data, list):
                urls = [str(url) for url in data if url]
            elif isinstance(data, dict) and 'urls' in data:
                urls = [str(url) for url in data['urls'] if url]
            else:
                return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400
        
        if not urls:
            return jsonify({'success': False, 'error': 'No valid URLs found in file'}), 400
        
        # Start batch scrape
        batch_id, message = crawler_manager.start_batch_scrape(urls)
        
        if batch_id:
            return jsonify({
                'success': True,
                'batch_id': batch_id,
                'message': message,
                'urls_count': len(urls),
                'filename': file.filename
            })
        else:
            return jsonify({'success': False, 'error': message}), 400
            
    except Exception as e:
        logger.error(f"Error uploading URL file: {e}")
        return jsonify({'success': False, 'error': f'Internal server error: {str(e)}'}), 500

# Global error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {e}")
    return jsonify({'error': 'Internal server error'}), 500

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    try:
        emit('connected', {'message': 'Connected to Alopecosa Crawler'})
        logger.info('Client connected')
    except Exception as e:
        logger.error(f"Error handling client connection: {e}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    try:
        logger.info('Client disconnected')
    except Exception as e:
        logger.error(f"Error handling client disconnection: {e}")

if __name__ == '__main__':
    print("🕷️  Starting Alopecosa Fabrilis Web Interface...")
    print("🌐 Open your browser to: http://localhost:5000")
    print("🕸️  The spider is ready to crawl the web!")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
