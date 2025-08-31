#!/usr/bin/env python3
"""
Simple Gunicorn configuration for Alopecosa Fabrilis Web Crawler
Fallback configuration without gevent-websocket
"""

import os
import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes - simple configuration
workers = min(multiprocessing.cpu_count() * 2 + 1, 4)  # Reduced for stability
worker_class = "gevent"  # Use regular gevent worker
worker_connections = 1000

# Request limits
max_requests = 1000
max_requests_jitter = 50

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
