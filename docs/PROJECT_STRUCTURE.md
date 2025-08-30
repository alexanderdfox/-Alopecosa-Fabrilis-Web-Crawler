# 🏗️ Project Structure Overview

This document provides a detailed overview of the Alopecosa Fabrilis Web Crawler project structure, explaining the organization, purpose, and relationships between different components.

## 📁 Directory Structure

```
web-crawler/
├── 📁 src/                           # Source code package
│   ├── 📄 __init__.py               # Main package initialization
│   ├── 📁 crawler/                  # Core crawler functionality
│   │   ├── 📄 __init__.py          # Crawler package initialization
│   │   └── 📄 alopecosa_crawler.py # Main crawler implementation
│   ├── 📁 web_interface/            # Web interface components
│   │   ├── 📄 __init__.py          # Web interface package initialization
│   │   └── 📄 web_interface.py     # Flask application and API
│   ├── 📁 database/                 # Database management
│   │   ├── 📄 __init__.py          # Database package initialization
│   │   ├── 📄 database_manager.py   # Database operations and queries
│   │   └── 📄 init_database.py     # Database initialization script
│   ├── 📁 batch_scraper/            # Batch processing system
│   │   ├── 📄 __init__.py          # Batch scraper package initialization
│   │   └── 📄 batch_url_scraper.py # Batch URL processing engine
│   ├── 📁 utils/                    # Utility functions and configuration
│   │   ├── 📄 __init__.py          # Utils package initialization
│   │   └── 📄 config.py            # Centralized configuration
│   ├── 📁 scripts/                  # Launcher and utility scripts
│   │   ├── 📄 __init__.py          # Scripts package initialization
│   │   ├── 📄 launch_web.py        # Web interface launcher
│   │   ├── 📄 launch_batch.py      # Batch processor launcher
│   │   ├── 📄 init_database.py     # Database initializer
│   │   └── 📄 test_imports.py      # Import test script
│   ├── 📁 examples/                 # Example scripts and sample data
│   │   ├── 📄 __init__.py          # Examples package initialization
│   │   ├── 📄 example_batch_scraping.py # Batch processing example
│   │   ├── 📄 demo_crawler.py      # Interactive demonstration
│   │   ├── 📄 example_usage.py     # Usage examples
│   │   └── 📁 sample_urls/         # Sample URL files for testing
│   └── 📁 tests/                    # Test files and test suites
│       ├── 📄 __init__.py          # Tests package initialization
│       ├── 📄 test_crawler.py      # Crawler functionality tests
│       └── 📄 test_database_storage.py # Database operation tests
├── 📁 templates/                     # HTML templates for web interface
│   ├── 📄 index.html               # Main dashboard template
│   ├── 📄 database.html            # Database interface template
│   └── 📄 batch.html               # Batch processing template
├── 📁 docs/                         # Documentation files
│   ├── 📄 PROJECT_STRUCTURE.md     # This file
│   ├── 📄 BATCH_SCRAPER_README.md  # Batch processing documentation
│   ├── 📄 DATABASE_README.md       # Database system documentation
│   ├── 📄 WEB_INTERFACE_README.md  # Web interface documentation
│   ├── 📄 INDEX.md                  # Documentation navigation
│   └── 📄 usage.md                  # Comprehensive usage guide
├── 📁 data/                         # Data storage
│   └── 📄 crawler_database.db      # SQLite database file
├── 📄 launch_web.py                # Web interface launcher (root)
├── 📄 launch_batch.py              # Batch processor launcher (root)
├── 📄 init_database.py             # Database initializer (root)
├── 📄 test_project.py              # Test script launcher (root)
├── 📄 requirements.txt              # Python dependencies
├── 📄 README.md                     # Main project documentation
└── 📄 PROJECT_STRUCTURE.md          # This file
```

## 🔧 Package Architecture

### 1. **Main Package** (`src/`)

The `src/` directory contains the main Python package with a clean, modular structure:

```python
# src/__init__.py
from .crawler.alopecosa_crawler import AlopecosaCrawler
from .database.database_manager import DatabaseManager
from .batch_scraper.batch_url_scraper import BatchURLScraper
from .utils.config import CRAWLER_CONFIG

__all__ = [
    'AlopecosaCrawler',
    'DatabaseManager', 
    'BatchURLScraper',
    'CRAWLER_CONFIG'
]
```

**Benefits:**
- **Clean Imports**: `from src.crawler import AlopecosaCrawler`
- **Modular Design**: Each component is self-contained
- **Easy Testing**: Components can be tested independently
- **Scalable**: Easy to add new modules and features

### 2. **Crawler Package** (`src/crawler/`)

Contains the core web crawling functionality:

```python
# src/crawler/__init__.py
from .alopecosa_crawler import AlopecosaCrawler, CrawlResult

__all__ = ['AlopecosaCrawler', 'CrawlResult']
```

**Components:**
- **`AlopecosaCrawler`**: Main crawling engine with spider-inspired behavior
- **`CrawlResult`**: Data class for storing crawl results
- **Spider Behavior**: Hunting, terrain mapping, adaptive strategies

**Key Features:**
- Active hunting mode
- Terrain mapping and exploration
- Adaptive crawling strategies
- Respectful crawling with delays

### 3. **Web Interface Package** (`src/web_interface/`)

Flask-based web application for managing crawlers:

```python
# src/web_interface/__init__.py
from .web_interface import app, crawler_manager

__all__ = ['app', 'crawler_manager']
```

**Components:**
- **Flask App**: Main web application
- **API Endpoints**: RESTful API for crawler management
- **WebSocket Support**: Real-time updates and monitoring
- **Template Rendering**: HTML page generation

**Key Features:**
- Real-time crawler monitoring
- Crawler creation and management
- Database integration
- Batch processing interface

### 4. **Database Package** (`src/database/`)

SQLite database management with advanced features:

```python
# src/database/__init__.py
from .database_manager import DatabaseManager

__all__ = ['DatabaseManager']
```

**Components:**
- **`DatabaseManager`**: Main database operations class
- **FTS5 Search**: Full-text search capabilities
- **Session Tracking**: Crawl session management
- **Statistics**: Comprehensive crawling analytics

**Key Features:**
- SQLite database with FTS5
- Full-text search across content
- Crawl session tracking
- Statistics and analytics
- Data deduplication

### 5. **Batch Scraper Package** (`src/batch_scraper/`)

High-performance batch URL processing:

```python
# src/batch_scraper/__init__.py
from .batch_url_scraper import BatchURLScraper

__all__ = ['BatchURLScraper']
```

**Components:**
- **`BatchURLScraper`**: Main batch processing engine
- **Concurrent Processing**: Multiple URLs simultaneously
- **File Format Support**: TXT, CSV, JSON input files
- **Progress Tracking**: Real-time operation monitoring

**Key Features:**
- Concurrent URL processing
- Multiple input file formats
- Real-time progress tracking
- Comprehensive error handling
- Database integration

### 6. **Utils Package** (`src/utils/`)

Utility functions and centralized configuration:

```python
# src/utils/__init__.py
from .config import CRAWLER_CONFIG, LOGGING_CONFIG, OUTPUT_CONFIG, SPIDER_PATTERNS

__all__ = ['CRAWLER_CONFIG', 'LOGGING_CONFIG', 'OUTPUT_CONFIG', 'SPIDER_PATTERNS']
```

**Components:**
- **`config.py`**: Centralized configuration management
- **Crawler Settings**: Behavior and performance parameters
- **Logging Configuration**: Log levels and formatting
- **Spider Patterns**: Behavior pattern definitions

### 7. **Scripts Package** (`src/scripts/`)

Launcher and utility scripts:

```python
# src/scripts/__init__.py
__all__ = [
    'launch_web',
    'launch_batch', 
    'init_database',
    'test_imports'
]
```

**Components:**
- **`launch_web.py`**: Web interface launcher
- **`launch_batch.py`**: Batch processor launcher
- **`init_database.py`**: Database initialization
- **`test_imports.py`**: Import validation script

### 8. **Examples Package** (`src/examples/`)

Example scripts and sample data:

```python
# src/examples/__init__.py
__all__ = [
    'example_batch_scraping',
    'demo_crawler',
    'example_usage'
]
```

**Components:**
- **`example_batch_scraping.py`**: Batch processing examples
- **`demo_crawler.py`**: Interactive demonstrations
- **`example_usage.py`**: Usage examples
- **`sample_urls/`**: Sample URL files for testing

### 9. **Tests Package** (`src/tests/`)

Test files and test suites:

```python
# src/tests/__init__.py
__all__ = [
    'test_database_storage',
    'test_crawler'
]
```

**Components:**
- **`test_crawler.py`**: Crawler functionality tests
- **`test_database_storage.py`**: Database operation tests

## 🌐 Web Interface Structure

### Templates Directory (`templates/`)

Contains HTML templates for the web interface:

```
templates/
├── 📄 index.html      # Main dashboard with crawler management
├── 📄 database.html   # Database search and management interface
└── 📄 batch.html      # Batch processing interface
```

**Template Features:**
- **Responsive Design**: Works on desktop and mobile
- **Modern UI**: Tailwind CSS with glass-morphism effects
- **Real-time Updates**: WebSocket integration for live data
- **Interactive Elements**: Forms, buttons, and dynamic content

### Navigation Structure

```
Dashboard (/) → Crawler Management, Real-time Stats
     ↓
Database (/database) → Search, Browse, Statistics
     ↓
Batch Processing (/batch) → URL Input, File Upload, Status
```

## 🚀 Launcher Scripts

### Root Level Launchers

The root directory contains simple launcher scripts that import from the `src` package:

#### **1. `launch_web.py`**
```python
#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    from scripts.launch_web import main
    main()
```

#### **2. `launch_batch.py`**
```python
#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    from scripts.launch_batch import main
    main()
```

#### **3. `init_database.py`**
```python
#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    from scripts.init_database import main
    main()
```

#### **4. `test_project.py`**
```python
#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    from scripts.test_imports import main
    main()
```

### Script Package Launchers

The actual launcher logic is in `src/scripts/`:

#### **`src/scripts/launch_web.py`**
```python
#!/usr/bin/env python3
from ..web_interface.web_interface import app, socketio

def main():
    print("🕷️  Starting Alopecosa Fabrilis Web Interface...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    main()
```

## 📊 Data Flow Architecture

### 1. **Single Crawler Flow**
```
User Input → Web Interface → Crawler Manager → AlopecosaCrawler → Database
    ↓              ↓              ↓              ↓              ↓
URL + Config → API Endpoint → Crawler Instance → Crawl Results → Storage
```

### 2. **Batch Processing Flow**
```
File Upload → Batch Scraper → Multiple Crawlers → Database Storage → Results
    ↓              ↓              ↓              ↓              ↓
TXT/CSV/JSON → URL Parsing → Concurrent Crawling → Batch Storage → Summary
```

### 3. **Database Query Flow**
```
Search Query → Database Manager → SQLite + FTS5 → Results → Web Interface
    ↓              ↓              ↓              ↓              ↓
User Input → Query Processing → Full-text Search → Data Retrieval → Display
```

## 🔗 Component Dependencies

### Dependency Graph

```
src/
├── web_interface/
│   ├── depends on: crawler, database, batch_scraper, utils
│   └── provides: Flask app, API endpoints
├── crawler/
│   ├── depends on: utils
│   └── provides: Crawling engine, results
├── database/
│   ├── depends on: utils
│   └── provides: Data storage, search
├── batch_scraper/
│   ├── depends on: crawler, database, utils
│   └── provides: Batch processing
├── utils/
│   ├── depends on: (none)
│   └── provides: Configuration, utilities
├── scripts/
│   ├── depends on: all other packages
│   └── provides: Launcher scripts
├── examples/
│   ├── depends on: all other packages
│   └── provides: Usage examples
└── tests/
    ├── depends on: all other packages
    └── provides: Testing functionality
```

### Import Patterns

**Relative Imports (within src package):**
```python
# Within src package
from ..crawler.alopecosa_crawler import AlopecosaCrawler
from ..database.database_manager import db_manager
from ..utils.config import CRAWLER_CONFIG
```

**Absolute Imports (from project root):**
```python
# From project root
from src.crawler import AlopecosaCrawler
from src.database import DatabaseManager
from src.batch_scraper import BatchURLScraper
```

**Fallback Imports (flexible system):**
```python
try:
    # Try relative imports first
    from ..crawler.alopecosa_crawler import AlopecosaCrawler
except ImportError:
    # Fall back to absolute imports
    from src.crawler.alopecosa_crawler import AlopecosaCrawler
```

## 🧪 Testing Structure

### Test Organization

```
src/tests/
├── 📄 __init__.py                    # Tests package initialization
├── 📄 test_crawler.py               # Crawler functionality tests
└── 📄 test_database_storage.py      # Database operation tests
```

### Testing Strategy

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete workflows
4. **Import Tests**: Verify package structure and imports

## 📚 Documentation Structure

### Documentation Files

```
docs/
├── 📄 PROJECT_STRUCTURE.md         # This file - detailed structure
├── 📄 BATCH_SCRAPER_README.md      # Batch processing guide
├── 📄 DATABASE_README.md           # Database system documentation
├── 📄 WEB_INTERFACE_README.md      # Web interface guide
├── 📄 INDEX.md                     # Documentation navigation
└── 📄 usage.md                     # Comprehensive usage guide
```

### README Files

- **`README.md`**: Main project overview and quick start
- **`PROJECT_STRUCTURE.md`**: This file - detailed structure explanation

## 🚀 Deployment Structure

### Production Layout

```
production/
├── 📁 app/                          # Application files
│   ├── 📁 src/                     # Source code
│   ├── 📁 templates/               # HTML templates
│   └── 📁 static/                  # Static assets
├── 📁 data/                         # Data storage
│   ├── 📁 database/                # SQLite database files
│   ├── 📁 logs/                    # Application logs
│   └── 📁 crawl_results/           # Crawl result files
├── 📁 config/                       # Configuration files
│   ├── 📄 production.py            # Production settings
│   └── 📄 logging.py               # Logging configuration
└── 📁 scripts/                      # Deployment scripts
    ├── 📄 deploy.sh                # Deployment script
    └── 📄 backup.sh                # Backup script
```

## 🔧 Configuration Management

### Configuration Hierarchy

1. **Default Config** (`src/utils/config.py`)
2. **Environment Variables** (`.env` file)
3. **Command Line Arguments** (CLI tools)
4. **Runtime Configuration** (Web interface)

### Configuration Files

```python
# src/utils/config.py
CRAWLER_CONFIG = {
    'default_max_depth': 3,
    'default_max_pages': 100,
    'default_delay_range': (1, 3),
    # ... more settings
}

LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}
```

## 📈 Scalability Considerations

### Horizontal Scaling

- **Load Balancing**: Multiple web interface instances
- **Database Sharding**: Distribute data across multiple databases
- **Queue Systems**: Use message queues for batch processing
- **Caching**: Implement Redis for session and result caching

### Vertical Scaling

- **Worker Processes**: Multiple crawler worker processes
- **Database Optimization**: Index optimization and query tuning
- **Memory Management**: Efficient data structures and cleanup
- **Resource Monitoring**: Monitor CPU, memory, and disk usage

## 🔒 Security Considerations

### Security Measures

1. **Input Validation**: Validate all user inputs
2. **Rate Limiting**: Prevent abuse and DoS attacks
3. **Authentication**: User authentication for admin functions
4. **Data Sanitization**: Sanitize data before database storage
5. **HTTPS**: Use HTTPS in production
6. **CORS**: Configure CORS properly for web interface

## 🎯 Future Enhancements

### Planned Features

1. **Distributed Crawling**: Multi-server crawling coordination
2. **Advanced Analytics**: Machine learning for crawl optimization
3. **Plugin System**: Extensible architecture for custom behaviors
4. **API Rate Limiting**: Intelligent rate limiting based on server responses
5. **Content Classification**: Automatic content categorization
6. **Export Formats**: Support for more export formats (XML, CSV, etc.)

## 🚀 Quick Start Commands

### From Project Root

```bash
# Test the project structure
python3 test_project.py

# Initialize database
python3 init_database.py

# Launch web interface
python3 launch_web.py

# Run batch processor
python3 launch_batch.py --create-samples
```

### From src Directory

```bash
# Test imports
python3 scripts/test_imports.py

# Initialize database
python3 scripts/init_database.py

# Launch web interface
python3 scripts/launch_web.py

# Run batch processor
python3 scripts/launch_batch.py --create-samples
```

---

This project structure provides a solid foundation for a professional web crawling system that is:
- **Modular**: Easy to maintain and extend
- **Scalable**: Can grow with requirements
- **Testable**: Well-organized for comprehensive testing
- **Documented**: Clear documentation for all components
- **Professional**: Follows Python best practices and standards
- **Clean**: Organized with minimal clutter in root directory
