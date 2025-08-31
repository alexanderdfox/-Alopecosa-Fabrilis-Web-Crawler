#!/usr/bin/env python3
"""
WSGI entry point for Alopecosa Fabrilis Web Crawler
Production-ready configuration for deployment
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set production environment
os.environ['FLASK_ENV'] = 'production'

try:
    from web_interface.web_interface import app, socketio
    
    # Production WSGI application
    application = app
    
    # Log the async mode being used
    print(f"✅ Web interface loaded successfully")
    print(f"🌐 SocketIO async mode: {socketio.async_mode}")
    print(f"🏭 Flask environment: {os.environ.get('FLASK_ENV', 'development')}")
    
    # For development/testing, you can still use socketio.run
    if __name__ == "__main__":
        print("🏭 Starting Alopecosa Fabrilis Web Interface in production mode...")
        print("🌐 Open your browser to: http://localhost:5000")
        print("🕸️  The spider is ready to crawl the web!")
        print("=" * 50)
        
        # Use Gunicorn for production (recommended)
        # Run: gunicorn -c gunicorn.conf.py wsgi:application
        print("💡 For production, use: gunicorn -c gunicorn.conf.py wsgi:application")
        
        # Fallback to socketio.run with production settings
        socketio.run(
            app, 
            host='0.0.0.0', 
            port=5000, 
            debug=False, 
            allow_unsafe_werkzeug=True,
            log_output=True
        )
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting web interface: {e}")
    sys.exit(1)
