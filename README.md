# 🕷️ Alopecosa Fabrilis Web Crawler

A sophisticated web crawling system inspired by the hunting and navigation behaviors of the *Alopecosa fabrilis* spider. This project combines biomimicry with modern web technologies to create an intelligent, respectful, and efficient web crawler.

## ✨ Features

- **🕷️ Spider-Inspired Behavior**: Active hunting, terrain mapping, and adaptive strategies
- **🌐 Modern Web Interface**: Beautiful, responsive dashboard with real-time monitoring
- **🗄️ Database Integration**: SQLite with full-text search and comprehensive analytics
- **🔄 Batch Processing**: High-performance concurrent URL processing
- **📊 Real-time Monitoring**: WebSocket-powered live updates and statistics
- **🔍 Advanced Search**: Full-text search across crawled content
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Quick Start

### 1. **Test the Project Structure**
```bash
python3 test_project.py
```

### 2. **Initialize Database**
```bash
python3 init_database.py
```

### 3. **Launch Web Interface**
```bash
python3 launch_web.py
```
Then visit: http://localhost:5000

### 4. **Use Batch Processing**
```bash
python3 launch_batch.py --create-samples
```

## 🏗️ Project Structure

```
web-crawler/
├── 📁 src/                           # Source code package
│   ├── 📁 crawler/                  # Core crawler functionality
│   ├── 📁 web_interface/            # Web interface components
│   ├── 📁 database/                 # Database management
│   ├── 📁 batch_scraper/            # Batch processing system
│   ├── 📁 utils/                    # Configuration and utilities
│   ├── 📁 scripts/                  # Launcher and utility scripts
│   ├── 📁 examples/                 # Example scripts and sample data
│   └── 📁 tests/                    # Test files and test suites
├── 📁 templates/                     # HTML templates
├── 📁 docs/                          # Documentation files
├── 📁 data/                          # Data storage
├── 📄 launch_web.py                 # Web interface launcher
├── 📄 launch_batch.py               # Batch processor launcher
├── 📄 init_database.py              # Database initializer
├── 📄 test_project.py               # Test script launcher
└── 📄 requirements.txt               # Python dependencies
```

## 🔧 Core Components

### **🕷️ AlopecosaCrawler**
The main crawling engine that mimics spider behavior:
- **Active Hunting**: Proactively discovers and follows links
- **Terrain Mapping**: Builds a map of the web landscape
- **Adaptive Strategies**: Adjusts behavior based on environment
- **Respectful Crawling**: Follows robots.txt and implements delays

### **🌐 Web Interface**
Modern Flask-based dashboard with:
- **Real-time Monitoring**: Live crawler status and progress
- **Crawler Management**: Create, configure, and monitor crawlers
- **Database Interface**: Search and browse crawled content
- **Batch Processing**: Upload files and process multiple URLs

### **🗄️ Database System**
SQLite-based storage with advanced features:
- **Full-text Search**: FTS5-powered content search
- **Session Tracking**: Comprehensive crawl session management
- **Statistics**: Detailed analytics and reporting
- **Data Deduplication**: MD5-based content deduplication

### **🔄 Batch Processor**
High-performance concurrent processing:
- **Multiple Formats**: TXT, CSV, and JSON input support
- **Concurrent Crawling**: Process multiple URLs simultaneously
- **Progress Tracking**: Real-time operation monitoring
- **Error Handling**: Comprehensive error management

## 📖 Usage Examples

### **Basic Crawling**
```python
from src.crawler import AlopecosaCrawler

# Create a crawler
crawler = AlopecosaCrawler(
    base_url="https://example.com",
    max_depth=3,
    max_pages=100
)

# Start crawling
results = crawler.crawl()
```

### **Batch Processing**
```python
from src.batch_scraper import BatchURLScraper

# Create batch processor
scraper = BatchURLScraper(max_workers=4)

# Process URLs from file
results = scraper.scrape_urls("urls.txt")
```

### **Database Operations**
```python
from src.database import DatabaseManager

# Initialize database
db = DatabaseManager()

# Search content
results = db.search_content("python web crawler")
```

## 🌟 Web Interface Features

### **Dashboard**
- **Real-time Stats**: Live crawler statistics and database overview
- **Crawler Management**: Create and configure new crawlers
- **Quick Actions**: Start, stop, and monitor crawlers
- **Navigation**: Easy access to all features

### **Database Interface**
- **Advanced Search**: Full-text search across all content
- **Content Browser**: Browse crawled websites and pages
- **Statistics**: Comprehensive analytics and reporting
- **Data Management**: Clean up and organize data

### **Batch Processing**
- **File Upload**: Support for TXT, CSV, and JSON files
- **Manual Input**: Direct URL input with configuration
- **Real-time Progress**: Live monitoring of batch operations
- **Results Summary**: Comprehensive operation reports

## ⚙️ Configuration

### **Crawler Settings**
```python
# src/utils/config.py
CRAWLER_CONFIG = {
    'default_max_depth': 3,        # Maximum crawl depth
    'default_max_pages': 100,      # Maximum pages per crawl
    'default_delay_range': (1, 3), # Delay between requests (seconds)
    'user_agent': 'Alopecosa Fabrilis Bot/1.0',
    'respect_robots': True,        # Follow robots.txt
    'timeout': 30                  # Request timeout (seconds)
}
```

### **Database Settings**
```python
DATABASE_CONFIG = {
    'database_path': 'data/crawler_database.db',
    'enable_fts': True,            # Enable full-text search
    'max_results': 1000,           # Maximum search results
    'cleanup_interval': 86400      # Cleanup interval (seconds)
}
```

## 🔌 API Endpoints

### **Crawler Management**
- `GET /api/crawlers` - List all crawlers
- `POST /api/crawlers` - Create new crawler
- `GET /api/crawlers/<crawler_id>` - Get crawler status
- `POST /api/crawlers/<crawler_id>/start` - Start crawler
- `POST /api/crawlers/<crawler_id>/stop` - Stop crawler

### **Database Operations**
- `GET /api/database/search` - Search content
- `GET /api/database/websites` - List websites
- `GET /api/database/statistics` - Get statistics
- `POST /api/database/cleanup` - Clean up old data

### **Batch Processing**
- `POST /api/batch-scrape` - Process manual URL input
- `POST /api/batch-scrape/upload` - Process file upload

## 🧪 Testing

### **Run All Tests**
```bash
python3 test_project.py
```

### **Individual Test Categories**
```bash
# Test imports and structure
python3 src/scripts/test_imports.py

# Test crawler functionality
python3 src/tests/test_crawler.py

# Test database operations
python3 src/tests/test_database_storage.py
```

## 📚 Documentation

- **📖 [Usage Guide](docs/usage.md)** - Comprehensive usage instructions
- **🏗️ [Project Structure](PROJECT_STRUCTURE.md)** - Detailed architecture overview
- **🌐 [Web Interface](docs/WEB_INTERFACE_README.md)** - Web interface documentation
- **🗄️ [Database](docs/DATABASE_README.md)** - Database system guide
- **🔄 [Batch Processing](docs/BATCH_SCRAPER_README.md)** - Batch processor documentation
- **📋 [Index](docs/INDEX.md)** - Documentation navigation

## 🚀 Development Setup

### **1. Clone Repository**
```bash
git clone <repository-url>
cd web-crawler
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Initialize Database**
```bash
python3 init_database.py
```

### **4. Test Installation**
```bash
python3 test_project.py
```

### **5. Launch Web Interface**
```bash
python3 launch_web.py
```

## 🔧 Requirements

- **Python**: 3.8 or higher
- **Dependencies**: See `requirements.txt`
- **Database**: SQLite3 (included with Python)
- **Browser**: Modern web browser for interface

## 📦 Dependencies

```
Flask==2.3.3
Flask-SocketIO==5.3.6
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

## 📄 License

This project is licensed under the BSD 3-Clause License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Alopecosa fabrilis** spider for behavioral inspiration
- **Flask** community for the excellent web framework
- **BeautifulSoup** team for HTML parsing capabilities
- **SQLite** developers for the robust database system

## 🆘 Support

- **Documentation**: Check the `docs/` directory
- **Issues**: Report bugs and feature requests
- **Examples**: See `src/examples/` for usage examples
- **Tests**: Run `python3 test_project.py` to verify setup

---

**🕷️ The Alopecosa Fabrilis spider is ready to crawl the web with intelligence and grace!** ✨
