#!/usr/bin/env python3
"""
WebSocket-enabled Gunicorn configuration for Alopecosa Fabrilis Web Crawler
Optimized for Flask-SocketIO with proper WebSocket support
"""

import os
import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes - optimized for WebSocket
workers = min(multiprocessing.cpu_count() * 2 + 1, 4)  # Reduced for stability

# Try to use gevent-websocket worker, fallback to gevent
try:
    import geventwebsocket
    worker_class = "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"
    worker_connections = 1000
    print("✅ Using gevent-websocket worker for WebSocket support")
except ImportError:
    # Fallback to regular gevent worker
    worker_class = "gevent"
    worker_connections = 500
    print("⚠️ Using regular gevent worker (limited WebSocket support)")

# Request limits
max_requests = 1000
max_requests_jitter = 50

# Timeout settings - increased for WebSocket connections
timeout = 60  # Increased for WebSocket ping/pong
keepalive = 5  # Increased for WebSocket connections
graceful_timeout = 30

# WebSocket specific settings
websocket_ping_interval = 25
websocket_ping_timeout = 60

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "alopecosa-crawler"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance
preload_app = True
worker_tmp_dir = "/dev/shm"

# Environment
raw_env = [
    "FLASK_ENV=production",
    "WERKZEUG_RUN_MAIN=true",
]

# WebSocket specific headers
forwarded_allow_ips = "*"
