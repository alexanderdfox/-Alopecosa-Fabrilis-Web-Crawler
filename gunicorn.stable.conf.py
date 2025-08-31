#!/usr/bin/env python3
"""
Stable Gunicorn configuration for Alopecosa Fabrilis Web Crawler
Designed to handle Werkzeug response conflicts with Flask-SocketIO
"""

import os
import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes - single worker to avoid conflicts
workers = 1  # Single worker to prevent response conflicts
worker_class = "gevent"  # Use regular gevent worker
worker_connections = 1000

# Request limits
max_requests = 1000
max_requests_jitter = 50

# Timeout settings - increased for stability
timeout = 120  # Increased timeout
keepalive = 10  # Increased keepalive
graceful_timeout = 60

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
preload_app = False  # Disable preload to prevent conflicts
worker_tmp_dir = "/dev/shm"

# Environment
raw_env = [
    "FLASK_ENV=production",
    "WERKZEUG_RUN_MAIN=true",
]

# Disable SSL monkey patching to prevent conflicts
disable_ssl_monkey_patch = True
