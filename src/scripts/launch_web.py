#!/usr/bin/env python3
"""
Launcher for Alopecosa Fabrilis Web Interface
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def main():
    """Main launcher function"""
    try:
        from web_interface.web_interface import app, socketio
        
        print("🕷️  Starting Alopecosa Fabrilis Web Interface...")
        print("🌐 Open your browser to: http://localhost:5000")
        print("🕸️  The spider is ready to crawl the web!")
        print("\n💡 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Run the Flask app
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Web interface stopped by user")
        print("👋 Goodbye!")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting web interface: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
