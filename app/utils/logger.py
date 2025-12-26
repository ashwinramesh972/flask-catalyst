import logging
import os
from logging.handlers import RotatingFileHandler
from flask import request, has_request_context
from datetime import datetime

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.method = request.method
            record.remote_addr = request.remote_addr or "unknown"
            record.user_id = getattr(request, 'user_id', 'anonymous')
            record.user_type = getattr(request, 'user_type', 'unknown')
            record.status = getattr(request, 'status', 0)
            record.duration_ms = getattr(request, 'duration_ms', 0)
        else:
            record.url = record.method = record.remote_addr = "N/A"
            record.user_id = record.user_type = "system"
            record.status = 0
            record.duration_ms = 0

        return super().format(record)

def setup_logger(app):
    # Create logs folder
    log_dir = os.path.join(app.instance_path, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Daily rotating log file
    log_file = os.path.join(log_dir, 'flask-catalyst.log')
    handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=10)  # 10MB per file, 10 files
    handler.setLevel(logging.INFO)

    # Beautiful format — exactly like your example
    formatter = RequestFormatter(
        fmt='[%(asctime)s] %(method)s %(url)s → %(status)d\n'
            '{\n'
            '  "user_id": %(user_id)s,\n'
            '  "user_type": "%(user_type)s",\n'
            '  "duration_ms": %(duration_ms)d,\n'
            '  "ip": "%(remote_addr)s",\n'
            '  "status": %(status)d,\n'
            '  "method": "%(method)s"\n'
            '}\n'
            '────────────────────────────────────────────────────────────\n',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    # Also log to console in development
    if app.debug:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)

    app.logger.info("flask-catalyst logger initialized — UTILS EMPIRE IS RISING")