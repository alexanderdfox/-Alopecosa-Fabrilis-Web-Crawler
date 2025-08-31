#!/usr/bin/env python3
"""
Gunicorn configuration for Alopecosa Fabrilis Web Crawler
Production WSGI server configuration
"""

import os
import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes - optimized for performance
workers = min(multiprocessing.cpu_count() * 2 + 1, 8)  # Cap at 8 workers

# Try gevent-websocket worker first, fallback to gevent if not available
try:
    import geventwebsocket
    worker_class = "geventwebsocket.gunicorn.workers.GeventWebSocketWorker"
    worker_connections = 2000  # Increased for better concurrency
except ImportError:
    # Fallback to regular gevent worker
    worker_class = "gevent"
    worker_connections = 1000  # Reduced for regular gevent
max_requests = 2000  # Increased for better performance
max_requests_jitter = 100  # Increased jitter for better distribution

# WebSocket specific settings
websocket_ping_interval = 25
websocket_ping_timeout = 60

# Performance optimizations
preload_app = True
worker_tmp_dir = "/dev/shm"  # Use shared memory for temp files

# Timeout settings
timeout = 30
keepalive = 2
graceful_timeout = 30

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

# SSL (uncomment for HTTPS)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"
