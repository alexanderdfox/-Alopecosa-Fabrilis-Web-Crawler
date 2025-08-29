# 📖 Alopecosa Fabrilis Web Crawler - Usage Guide

This comprehensive guide will walk you through using the spider-inspired web crawler, from basic setup to advanced customization.

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd web-crawler

# Install dependencies
pip install -r requirements.txt

# Verify installation
python3 alopecosa_crawler.py --help
```

### 2. Your First Crawl

```bash
# Basic crawl
python3 alopecosa_crawler.py https://example.com

# This will:
# - Crawl example.com up to depth 3
# - Limit to 100 pages maximum
# - Use polite delays between requests
# - Save results to a timestamped JSON file
```

## 🔧 Command Line Interface

### Basic Syntax

```bash
python3 alopecosa_crawler.py <URL> [OPTIONS]
```

### Available Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--depth` | Maximum crawl depth | 3 | `--depth 5` |
| `--pages` | Maximum pages to crawl | 100 | `--pages 200` |
| `--delay` | Delay between requests (seconds) | 1.0 | `--delay 2.0` |
| `--output` | Custom output filename | auto-generated | `--output my_results.json` |
| `--help` | Show help message | - | `--help` |

### Command Examples

```bash
# Conservative crawl (slow, respectful)
python3 alopecosa_crawler.py https://example.com --depth 2 --pages 50 --delay 3.0

# Aggressive crawl (fast, more intensive)
python3 alopecosa_crawler.py https://example.com --depth 5 --pages 500 --delay 0.5

# Custom output file
python3 alopecosa_crawler.py https://example.com --output company_analysis.json

# Deep exploration of a specific site
python3 alopecosa_crawler.py https://blog.example.com --depth 8 --pages 1000
```

## 🐍 Python API Usage

### Basic Usage

```python
from alopecosa_crawler import AlopecosaCrawler

# Create crawler instance
crawler = AlopecosaCrawler(
    base_url="https://example.com",
    max_depth=3,
    max_pages=100
)

# Start crawling
results = crawler.crawl()

# Save results
crawler.save_results("my_crawl_results.json")

# Get statistics
stats = crawler.get_crawl_statistics()
print(stats)
```

### Advanced Configuration

```python
# Custom crawler with all options
crawler = AlopecosaCrawler(
    base_url="https://example.com",
    max_depth=5,
    max_pages=500,
    delay_range=(1, 3),  # Random delay between 1-3 seconds
    user_agent="My-Custom-Crawler/1.0",
    respect_robots=True
)

# Start crawling
results = crawler.crawl()

# Access spider-specific features
print(f"Terrain mapped: {len(crawler.terrain_map)} areas")
print(f"Rich hunting grounds: {len(crawler.prey_scent)}")
```

### Working with Results

```python
# Process crawl results
for result in results:
    print(f"URL: {result.url}")
    print(f"Title: {result.title}")
    print(f"Content: {result.content[:200]}...")  # First 200 chars
    print(f"Links found: {len(result.links)}")
    print(f"Crawl time: {result.crawl_time:.2f}s")
    print("---")

# Filter results by content length
substantial_content = [r for r in results if len(r.content) > 500]

# Find pages with many links
link_rich_pages = [r for r in results if len(r.links) > 10]
```

## 🕷️ Spider Behavior Features

### Understanding the Spider's Mind

The crawler mimics real spider behavior:

```python
# Access the spider's mental map
terrain_map = crawler.terrain_map
for url, info in terrain_map.items():
    print(f"Area: {url}")
    print(f"  Depth: {info['depth']}")
    print(f"  Link density: {info['link_count']}")
    print(f"  Discovered: {info['discovered_at']}")

# Check prey scent (rich areas)
rich_areas = crawler.prey_scent
print(f"Spider found {len(rich_areas)} rich hunting grounds")
```

### Adaptive Behavior

The spider learns and adapts:

```python
# Monitor how the spider adapts
crawler = AlopecosaCrawler(
    base_url="https://example.com",
    max_depth=3,
    max_pages=50
)

# The spider will automatically:
# - Adjust link density thresholds
# - Prioritize successful areas
# - Learn from failed attempts
# - Build efficient exploration paths

results = crawler.crawl()
```

## 📊 Output and Results

### JSON Output Structure

```json
{
  "crawl_info": {
    "base_url": "https://example.com",
    "max_depth": 3,
    "max_pages": 100,
    "pages_crawled": 45,
    "crawl_timestamp": "2024-01-15T10:30:00"
  },
  "terrain_map": {
    "https://example.com": {
      "depth": 0,
      "link_count": 15,
      "title": "Example Domain",
      "discovered_at": "2024-01-15T10:30:00"
    }
  },
  "results": [
    {
      "url": "https://example.com",
      "title": "Example Domain",
      "content": "This domain is for use in illustrative examples...",
      "links": ["https://example.com/page1", "https://example.com/page2"],
      "status_code": 200,
      "crawl_time": 1.23,
      "timestamp": "2024-01-15T10:30:00",
      "metadata": {
        "depth": 0,
        "link_count": 15,
        "response_time": 0.5
      }
    }
  ]
}
```

### Statistics and Analytics

```python
# Get comprehensive statistics
stats = crawler.get_crawl_statistics()

print("Crawl Statistics:")
print(f"  Total pages: {stats['total_pages']}")
print(f"  Total links: {stats['total_links_discovered']}")
print(f"  Success rate: {stats['success_rate']:.1%}")
print(f"  Average crawl time: {stats['average_crawl_time']:.2f}s")
print(f"  Terrain coverage: {stats['terrain_coverage']}")
print(f"  Hunting efficiency: {stats['hunting_efficiency']}")
```

## ⚙️ Configuration

### Modifying Behavior

Edit `config.py` to customize crawler behavior:

```python
# Spider behavior patterns
SPIDER_PATTERNS = {
    'prey_detection_threshold': 5,  # Links needed for "rich" area
    'hunting_aggression': 0.7,      # Aggressiveness level
    'exploration_strategy': 'depth_first',  # 'depth_first', 'breadth_first', 'adaptive'
    'learning_rate': 0.1
}

# Crawler settings
CRAWLER_CONFIG = {
    'default_max_depth': 3,
    'default_max_pages': 100,
    'default_delay_range': (1, 3),
    'timeout': 15,
    'max_retries': 3
}
```

### Environment Variables

```bash
# Set custom user agent
export ALOPECOSA_USER_AGENT="My-Crawler/1.0"

# Set custom delay
export ALOPECOSA_DELAY=2.0

# Disable robots.txt respect
export ALOPECOSA_RESPECT_ROBOTS=false
```

## 🎯 Use Case Examples

### Academic Research

```python
# Crawl academic websites for research papers
crawler = AlopecosaCrawler(
    base_url="https://arxiv.org",
    max_depth=4,
    max_pages=200,
    delay_range=(2, 4)  # Be extra respectful
)

results = crawler.crawl()

# Filter for research papers
papers = [r for r in results if 'pdf' in r.url.lower() or 'abs' in r.url.lower()]
```

### E-commerce Analysis

```python
# Analyze product catalogs
crawler = AlopecosaCrawler(
    base_url="https://shop.example.com",
    max_depth=3,
    max_pages=500
)

results = crawler.crawl()

# Find product pages
product_pages = [r for r in results if '/product/' in r.url or '/item/' in r.url]
```

### News Monitoring

```python
# Monitor news websites
crawler = AlopecosaCrawler(
    base_url="https://news.example.com",
    max_depth=2,
    max_pages=100,
    delay_range=(1, 2)  # Check frequently
)

results = crawler.crawl()

# Extract headlines
headlines = [r.title for r in results if r.title and len(r.title) > 10]
```

## 🔒 Ethical Crawling

### Best Practices

1. **Respect robots.txt**: Always check website crawling policies
2. **Use polite delays**: Don't overwhelm servers
3. **Stay within limits**: Don't crawl too deeply or too many pages
4. **Respect terms of service**: Check website usage policies
5. **Use appropriate user agents**: Identify your crawler clearly

### Rate Limiting

```python
# Conservative crawling
crawler = AlopecosaCrawler(
    base_url="https://example.com",
    delay_range=(3, 5),  # 3-5 second delays
    max_pages=50,        # Limit page count
    max_depth=2          # Limit depth
)

# Aggressive crawling (use with caution)
crawler = AlopecosaCrawler(
    base_url="https://example.com",
    delay_range=(0.5, 1),  # 0.5-1 second delays
    max_pages=1000,        # More pages
    max_depth=5            # Deeper exploration
)
```

## 🐛 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure dependencies are installed
pip install -r requirements.txt

# Check Python version
python3 --version  # Should be 3.7+
```

#### Network Timeouts
```python
# Increase timeout in config.py
CRAWLER_CONFIG = {
    'timeout': 30,  # Increase from 15 to 30 seconds
    # ... other settings
}
```

#### Rate Limiting
```python
# Increase delays if getting blocked
crawler = AlopecosaCrawler(
    base_url="https://example.com",
    delay_range=(5, 10),  # Much longer delays
    max_pages=20          # Fewer pages
)
```

### Debug Mode

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Or modify config.py
LOGGING_CONFIG = {
    'level': 'DEBUG',  # Change from 'INFO' to 'DEBUG'
    # ... other settings
}
```

## 📚 Advanced Topics

### Custom Content Extraction

```python
# Override content extraction
class CustomCrawler(AlopecosaCrawler):
    def _extract_content(self, soup, url):
        # Custom content extraction logic
        content = ""
        
        # Look for specific content areas
        main_content = soup.find('div', class_='content')
        if main_content:
            content = main_content.get_text(strip=True)
        
        # Extract specific data
        price = soup.find('span', class_='price')
        if price:
            content += f"\nPrice: {price.get_text()}"
        
        return content

# Use custom crawler
crawler = CustomCrawler("https://example.com")
results = crawler.crawl()
```

### Concurrent Crawling

```python
# For advanced users: implement concurrent crawling
import threading
from concurrent.futures import ThreadPoolExecutor

def crawl_section(base_url, section):
    crawler = AlopecosaCrawler(
        base_url=f"{base_url}/{section}",
        max_depth=2,
        max_pages=50
    )
    return crawler.crawl()

# Crawl multiple sections concurrently
sections = ['news', 'blog', 'products']
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(crawl_section, 'https://example.com', section) 
               for section in sections]
    all_results = [future.result() for future in futures]
```

## 🎉 Getting Help

### Resources

- **README.md**: Complete project overview
- **example_usage.py**: Working examples
- **test_crawler.py**: Test suite
- **demo_crawler.py**: Interactive demonstration

### Support

- Check the logs in `alopecosa_crawler.log`
- Review error messages for specific issues
- Ensure all dependencies are installed
- Verify network connectivity and firewall settings

---

**🕷️ Happy crawling with your spider-inspired web crawler!**

Remember: The Alopecosa Fabrilis is patient, intelligent, and respectful - just like your crawler should be! 🕸️✨
