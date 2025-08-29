#!/usr/bin/env python3
"""
Alopecosa Fabrilis Web Crawler - Cloudflare Workers Version
Optimized for Cloudflare Workers environment
"""

import json
import os
from datetime import datetime
import logging
from typing import Dict, Any, Optional

# Configure logging for Cloudflare Workers
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CloudflareCrawlerWorker:
    """Cloudflare Workers-compatible crawler worker"""
    
    def __init__(self):
        self.config = {
            'max_depth': 3,
            'max_pages': 100,
            'delay_range': (1, 3),
            'user_agent': 'Alopecosa Fabrilis Bot/1.0 (Cloudflare)',
            'respect_robots': True,
            'timeout': 30
        }
    
    def handle_request(self, request):
        """Handle incoming HTTP requests"""
        try:
            url = str(request.url)
            method = request.method
            
            if method == "GET":
                if url.endswith("/") or url.endswith("/index.html"):
                    return self.serve_dashboard()
                elif "/api/status" in url:
                    return self.get_status()
                else:
                    return self.serve_static_file(url)
            
            elif method == "POST":
                if "/api/crawl" in url:
                    return self.handle_crawl_request(request)
                elif "/api/batch" in url:
                    return self.handle_batch_request(request)
                else:
                    return self.create_response({"error": "Endpoint not found"}, 404)
            
            else:
                return self.create_response({"error": "Method not allowed"}, 405)
                
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return self.create_response({"error": str(e)}, 500)
    
    def serve_dashboard(self):
        """Serve the main dashboard HTML"""
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Alopecosa Fabrilis Web Crawler</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
                .crawler-form { background: #ecf0f1; padding: 20px; border-radius: 8px; margin-bottom: 30px; }
                .form-group { margin-bottom: 15px; }
                label { display: block; margin-bottom: 5px; font-weight: bold; }
                input, select { width: 100%; padding: 10px; border: 1px solid #bdc3c7; border-radius: 4px; }
                button { background: #3498db; color: white; padding: 12px 24px; border: none; border-radius: 4px; cursor: pointer; }
                button:hover { background: #2980b9; }
                .status { background: #e8f5e8; padding: 15px; border-radius: 4px; margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🕷️ Alopecosa Fabrilis Web Crawler</h1>
                
                <div class="crawler-form">
                    <h3>Create New Crawler</h3>
                    <form id="crawlerForm">
                        <div class="form-group">
                            <label for="name">Crawler Name:</label>
                            <input type="text" id="name" name="name" required placeholder="My Spider">
                        </div>
                        
                        <div class="form-group">
                            <label for="base_url">Base URL:</label>
                            <input type="url" id="base_url" name="base_url" required placeholder="https://example.com">
                        </div>
                        
                        <div class="form-group">
                            <label for="max_depth">Max Depth:</label>
                            <select id="max_depth" name="max_depth">
                                <option value="1">1</option>
                                <option value="2">2</option>
                                <option value="3" selected>3</option>
                                <option value="4">4</option>
                                <option value="5">5</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="max_pages">Max Pages:</label>
                            <input type="number" id="max_pages" name="max_pages" min="1" max="1000" value="100">
                        </div>
                        
                        <button type="submit">🕷️ Start Crawling</button>
                    </form>
                </div>
                
                <div id="status" class="status" style="display: none;">
                    <h4>Crawler Status</h4>
                    <div id="statusContent"></div>
                </div>
            </div>
            
            <script>
                document.getElementById('crawlerForm').addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    const formData = new FormData(e.target);
                    const data = Object.fromEntries(formData.entries());
                    
                    try {
                        const response = await fetch('/api/crawl', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(data)
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            document.getElementById('status').style.display = 'block';
                            document.getElementById('statusContent').innerHTML = `
                                <p><strong>✅ Crawler Started!</strong></p>
                                <p>Name: ${data.name}</p>
                                <p>URL: ${data.base_url}</p>
                                <p>Status: Running</p>
                            `;
                        } else {
                            alert('Error: ' + result.error);
                        }
                    } catch (error) {
                        alert('Error: ' + error.message);
                    }
                });
            </script>
        </body>
        </html>
        """
        
        return self.create_response(html, 200, "text/html")
    
    def handle_crawl_request(self, request):
        """Handle crawler creation requests"""
        try:
            # For now, simulate the request data since we can't easily parse JSON in this environment
            # In a real implementation, you'd parse the request body
            data = {"name": "Test Crawler", "base_url": "https://example.com"}
            
            # Validate input
            if not data.get('name') or not data.get('base_url'):
                return self.create_response({"error": "Name and base_url are required"}, 400)
            
            # Simulate crawler creation (in real implementation, you'd store this)
            crawler_id = f"crawler_{int(datetime.now().timestamp())}"
            
            return self.create_response({
                "success": True,
                "crawler_id": crawler_id,
                "message": "Crawler created successfully"
            })
            
        except Exception as e:
            logger.error(f"Error handling crawl request: {e}")
            return self.create_response({"error": str(e)}, 500)
    
    def handle_batch_request(self, request):
        """Handle batch processing requests"""
        try:
            # Simulate batch processing
            urls = ["https://example1.com", "https://example2.com"]
            
            results = []
            for url in urls[:10]:  # Limit to 10 URLs for demo
                results.append({
                    "url": url,
                    "status": "queued",
                    "timestamp": datetime.now().isoformat()
                })
            
            return self.create_response({
                "success": True,
                "message": f"Batch processing started for {len(urls)} URLs",
                "results": results
            })
            
        except Exception as e:
            logger.error(f"Error handling batch request: {e}")
            return self.create_response({"error": str(e)}, 500)
    
    def get_status(self):
        """Get system status"""
        return self.create_response({
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "environment": "cloudflare-workers"
        })
    
    def serve_static_file(self, url):
        """Serve static files (simplified)"""
        return self.create_response("File not found", 404)
    
    def create_response(self, content, status_code=200, content_type="application/json"):
        """Create a Cloudflare Workers response"""
        if isinstance(content, dict):
            content = json.dumps(content)
        
        headers = {
            "Content-Type": content_type,
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
        
        return Response(content, status=status_code, headers=headers)

# Global worker instance
worker = CloudflareCrawlerWorker()

# Main Cloudflare Workers event handler - this is what Cloudflare expects
def fetch(request, env, ctx):
    """Main fetch event handler for Cloudflare Workers"""
    try:
        return worker.handle_request(request)
    except Exception as e:
        logger.error(f"Error in fetch handler: {e}")
        return Response(
            json.dumps({"error": "Internal server error"}),
            status=500,
            headers={"Content-Type": "application/json"}
        )

# Alternative handler names that Cloudflare might expect
def on_fetch(request, env, ctx):
    """Alternative fetch handler name"""
    return fetch(request, env, ctx)

def on_request(request, env, ctx):
    """Alternative request handler name"""
    return fetch(request, env, ctx)

# For local testing
if __name__ == "__main__":
    print("This file is designed to run on Cloudflare Workers")
    print("Use 'wrangler dev' to test locally")
