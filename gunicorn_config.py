"""
Gunicorn configuration for production deployment
"""
import os

# Server socket
bind = "0.0.0.0:" + os.environ.get("PORT", "5000")
workers = 2
worker_class = 'gevent'
worker_connections = 1000
timeout = 30
keepalive = 2

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging
errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
