# 🕷️ Batch URL Scraper for Alopecosa Fabrilis

A powerful batch processing tool for the Alopecosa Fabrilis web crawler that can scrape multiple URLs simultaneously and store all results in the database.

## ✨ Features

- **🔄 Concurrent Processing**: Scrape multiple URLs simultaneously with configurable worker threads
- **📁 Multiple File Formats**: Support for TXT, CSV, and JSON input files
- **🗄️ Database Integration**: Automatically stores all crawl results in the database
- **⚙️ Configurable Settings**: Customize crawl depth, page limits, and delays
- **📊 Comprehensive Reporting**: Detailed statistics and error tracking
- **🛡️ Respectful Crawling**: Built-in delays and rate limiting
- **💾 Result Export**: Save batch results to JSON files
- **🔍 Search Integration**: All results are searchable through the database interface

## 🚀 Quick Start

### 1. Create Sample URL Files

```bash
python3 batch_url_scraper.py --create-samples
```

This creates sample files in the `sample_urls/` directory:
- `sample_urls.txt` - Simple text file with one URL per line
- `sample_urls.csv` - CSV file with URL and description columns
- `sample_urls.json` - JSON file with structured URL data

### 2. Run Batch Scrape

```bash
# Basic usage with text file
python3 batch_url_scraper.py sample_urls/sample_urls.txt

# With custom settings
python3 batch_url_scraper.py sample_urls/sample_urls.txt \
    --max-workers 5 \
    --max-depth 2 \
    --max-pages 20 \
    --delay 3.0
```

### 3. Programmatic Usage

```python
from batch_url_scraper import BatchURLScraper
from config import CRAWLER_CONFIG

# Initialize scraper
scraper = BatchURLScraper(max_workers=3, delay_between_crawls=2.0)

# Load URLs from file
urls = scraper.load_urls_from_file("my_urls.txt")

# Run batch scrape
results = scraper.scrape_urls(urls, CRAWLER_CONFIG)

# Print summary
scraper.print_summary()

# Save results
output_file = scraper.save_batch_results()
```

## 📋 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `url_file` | File containing URLs to scrape | Required |
| `--file-type` | File type (txt, csv, json, auto) | auto |
| `--max-workers` | Maximum concurrent crawlers | 3 |
| `--delay` | Delay between crawls (seconds) | 2.0 |
| `--max-depth` | Maximum crawl depth | 1 |
| `--max-pages` | Maximum pages per site | 10 |
| `--output` | Output file for results | auto-generated |
| `--create-samples` | Create sample URL files | False |

## 📁 Input File Formats

### Text File (.txt)
```
# Comments start with #
https://example.com
https://httpbin.org
https://jsonplaceholder.typicode.com
```

### CSV File (.csv)
```csv
url,description
https://example.com,Example Domain
https://httpbin.org,HTTP Testing Service
https://jsonplaceholder.typicode.com,JSON API Testing
```

### JSON File (.json)
```json
{
  "description": "My URL List",
  "urls": [
    "https://example.com",
    "https://httpbin.org",
    "https://jsonplaceholder.typicode.com"
  ]
}
```

## ⚙️ Configuration

The batch scraper uses the same configuration system as the main crawler:

```python
from config import CRAWLER_CONFIG

# Default settings
config = CRAWLER_CONFIG.copy()

# Customize for batch processing
config.update({
    'default_max_depth': 2,      # Crawl 2 levels deep
    'default_max_pages': 50,     # Maximum 50 pages per site
    'default_delay_range': (2, 5)  # 2-5 second delays
})
```

## 🔧 Advanced Usage

### Custom Worker Configuration

```python
# High-performance scraping (use with caution)
scraper = BatchURLScraper(
    max_workers=10,              # 10 concurrent crawlers
    delay_between_crawls=1.0     # 1 second between crawls
)

# Conservative scraping (be respectful)
scraper = BatchURLScraper(
    max_workers=2,               # 2 concurrent crawlers
    delay_between_crawls=5.0     # 5 seconds between crawls
)
```

### Error Handling and Monitoring

```python
# Run batch scrape
results = scraper.scrape_urls(urls, config)

# Check results
if results['summary']['success_rate'] > 80:
    print("✅ High success rate achieved!")
else:
    print("⚠️  Some crawls failed, check errors")

# Access individual results
for url, result in results['results'].items():
    if result['success']:
        print(f"✅ {url}: {result['pages_crawled']} pages")
    else:
        print(f"❌ {url}: {result['error']}")
```

### Database Integration

All crawl results are automatically stored in the database:

```python
# Check database statistics
stats = db_manager.get_statistics()
print(f"Total websites: {stats['total_websites']}")
print(f"Total sessions: {stats['total_sessions']}")

# Search through crawled data
results, count = db_manager.search_websites("example")
print(f"Found {count} results containing 'example'")
```

## 📊 Output and Results

### Console Output
```
🕷️  BATCH SCRAPE SUMMARY
============================================================
📊 Total URLs: 10
✅ Successful: 8
❌ Failed: 2
📄 Total Pages Crawled: 45
🔗 Total Links Found: 234
⏱️  Total Crawl Time: 67.32s
📈 Success Rate: 80.0%
⏱️  Average Crawl Time: 8.42s

❌ FAILED CRAWLS:
   • https://example.com: Connection timeout
   • https://invalid-url.com: Invalid URL
============================================================
```

### JSON Results File
```json
{
  "batch_scrape_summary": {
    "timestamp": "2025-08-29T11:30:00",
    "summary": {
      "total_urls": 10,
      "successful": 8,
      "failed": 2,
      "total_pages_crawled": 45,
      "success_rate": 80.0
    }
  },
  "successful_crawls": {
    "https://httpbin.org": {
      "url": "https://httpbin.org",
      "success": true,
      "pages_crawled": 5,
      "session_id": 123
    }
  },
  "failed_crawls": {
    "https://example.com": {
      "url": "https://example.com",
      "success": false,
      "error": "Connection timeout"
    }
  }
}
```

## 🗄️ Database Storage

Every successful crawl is automatically stored in the database with:

- **Crawl Session**: Metadata about the batch crawl
- **Website Data**: Content, links, and metadata for each page
- **Search Index**: Full-text search capabilities
- **Statistics**: Aggregated data for analysis

Access the data through:
- Web interface: `/database` route
- API endpoints: `/api/database/*`
- Direct database queries

## 🚨 Best Practices

### 1. Be Respectful
```python
# Good: Conservative settings
scraper = BatchURLScraper(
    max_workers=2,
    delay_between_crawls=5.0
)

# Avoid: Aggressive settings
scraper = BatchURLScraper(
    max_workers=20,  # Too many concurrent requests
    delay_between_crawls=0.1  # Too fast
)
```

### 2. Monitor Resources
```python
# Check database size periodically
stats = db_manager.get_statistics()
if stats['total_websites'] > 10000:
    print("⚠️  Large dataset, consider cleanup")

# Clean old data if needed
db_manager.delete_old_data(days=30)
```

### 3. Error Handling
```python
try:
    results = scraper.scrape_urls(urls, config)
    
    # Check for failures
    if results['summary']['failed'] > 0:
        print(f"⚠️  {results['summary']['failed']} crawls failed")
        
        # Retry failed URLs
        failed_urls = list(results['errors'].keys())
        retry_results = scraper.scrape_urls(failed_urls, config)
        
except Exception as e:
    print(f"❌ Batch scrape failed: {e}")
    # Implement fallback or notification
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure all dependencies are installed
   pip install -r requirements.txt
   ```

2. **Database Errors**
   ```bash
   # Reinitialize database
   python3 init_database.py
   ```

3. **Memory Issues**
   ```python
   # Reduce concurrent workers
   scraper = BatchURLScraper(max_workers=1)
   ```

4. **Rate Limiting**
   ```python
   # Increase delays
   scraper = BatchURLScraper(delay_between_crawls=10.0)
   ```

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Tuning

### Optimal Settings by Use Case

| Use Case | Workers | Delay | Depth | Pages |
|----------|---------|-------|-------|-------|
| **Testing** | 1 | 1s | 1 | 5 |
| **Development** | 2 | 2s | 2 | 20 |
| **Production** | 3-5 | 3-5s | 2-3 | 50-100 |
| **Aggressive** | 10+ | 1s | 3+ | 100+ |

### Memory Management

```python
# For large batches, process in chunks
def process_large_batch(urls, chunk_size=100):
    for i in range(0, len(urls), chunk_size):
        chunk = urls[i:i + chunk_size]
        results = scraper.scrape_urls(chunk, config)
        scraper.print_summary()
        
        # Clear results to free memory
        scraper.results.clear()
        scraper.errors.clear()
```

## 🔗 Integration Examples

### Web Interface Integration

```python
# Add batch processing to web interface
@app.route('/api/batch-scrape', methods=['POST'])
def batch_scrape():
    data = request.get_json()
    urls = data.get('urls', [])
    
    scraper = BatchURLScraper()
    results = scraper.scrape_urls(urls)
    
    return jsonify({
        'success': True,
        'results': results['summary']
    })
```

### Scheduled Batch Processing

```python
import schedule
import time

def daily_batch_scrape():
    scraper = BatchURLScraper()
    urls = load_daily_urls()
    results = scraper.scrape_urls(urls)
    
    # Send notification
    send_notification(f"Daily batch complete: {results['summary']['successful']} successful")

# Schedule daily at 2 AM
schedule.every().day.at("02:00").do(daily_batch_scrape)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 📚 Examples

See `example_batch_scraping.py` for complete working examples:

- Basic batch scraping
- Custom configuration
- File-based URL loading
- Error handling
- Database integration

## 🤝 Contributing

The batch scraper is designed to be extensible:

- Add new input file formats
- Implement custom result processors
- Add monitoring and alerting
- Create specialized configurations

## 📄 License

Part of the Alopecosa Fabrilis Web Crawler project.

---

**🕷️ Happy Batch Scraping!** The Alopecosa Fabrilis spider is now ready to hunt across multiple websites simultaneously! 🕸️✨
