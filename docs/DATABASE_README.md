# 🗄️ Database System - Alopecosa Fabrilis Web Crawler

A powerful SQLite-based database system for storing, searching, and managing crawled websites.

## ✨ Features

- **📊 Persistent Storage**: All crawled websites are automatically saved
- **🔍 Full-Text Search**: Search through titles, content, and URLs
- **🎯 Advanced Filtering**: Filter by domain, depth, status code, and more
- **📈 Statistics Dashboard**: Real-time database metrics
- **🔄 Session Tracking**: Complete crawl session history
- **🧹 Data Management**: Cleanup old data and maintenance tools

## 🚀 Quick Start

### 1. Initialize Database
```bash
python3 init_database.py
```

### 2. Launch Web Interface
```bash
python3 launch_web.py
```

### 3. Access Database Interface
Navigate to: **http://localhost:5000/database**

## 🏗️ Architecture

### Database Tables
- **websites**: Stores all crawled website data
- **links**: Tracks relationships between websites
- **crawl_sessions**: Records crawl job history
- **search_index**: Full-text search using FTS5

### Key Features
- **Content Deduplication**: MD5 hashing prevents duplicate content
- **Relationship Tracking**: Maps website connections
- **Search Optimization**: FTS5 indexing for fast searches
- **Automatic Storage**: Results saved after each crawl

## 🔍 Search Capabilities

### Basic Search
- **Keywords**: Search in titles, content, and URLs
- **Domain Filter**: Filter by specific websites
- **Depth Filter**: Filter by crawl depth
- **Status Filter**: Filter by HTTP status codes

### Advanced Options
- **Results per Page**: 10, 20, 50, or 100 results
- **Sorting**: By timestamp, title, domain, or depth
- **Content Length**: Short, medium, or long content

## 📊 Database Statistics

- Total websites crawled
- Total links discovered
- Unique domains
- Recent activity (last 7 days)
- Average content length
- Crawl session count

## 🛠️ Management Tools

### Data Cleanup
- Remove old websites (configurable age)
- Clean orphaned links
- Rebuild search index

### Export Features
- Download search results
- Export crawl sessions
- Backup database

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/database/search` | GET | Search websites |
| `/api/database/websites/{id}` | GET | Get website details |
| `/api/database/domains` | GET | List all domains |
| `/api/database/sessions` | GET | Get crawl sessions |
| `/api/database/statistics` | GET | Get database stats |
| `/api/database/cleanup` | POST | Clean old data |

## 💡 Usage Examples

### Search for Specific Content
```
Query: "machine learning"
Domain: example.com
Depth: 2
Status: 200
```

### Find Recent Crawls
```
Query: ""
Domain: ""
Depth: ""
Status: ""
Sort: Timestamp (newest first)
```

### Analyze Website Structure
```
Query: ""
Domain: "target-site.com"
Depth: "All"
Status: "All"
```

## 🎯 Benefits

- **Persistent Data**: Never lose crawled information
- **Fast Search**: Find specific content quickly
- **Data Analysis**: Understand website structures
- **Historical Tracking**: Monitor crawl performance
- **Content Discovery**: Find related information

## 🔒 Data Privacy

- **Local Storage**: All data stays on your machine
- **No External Sharing**: Complete privacy control
- **Secure Access**: Only accessible through web interface
- **Data Ownership**: You control all crawled data

---

**🕷️ Your spider now has a powerful memory!**

Store, search, and analyze all your crawled websites with the database system! 🗄️✨
