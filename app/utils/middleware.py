import time
from flask import g, request, has_request_context

def add_request_logging(app):
    @app.before_request
    def start_timer():
        g.start = time.time()

    @app.after_request
    def log_request(response):
        if not has_request_context():
            return response

        # Calculate duration
        duration = round((time.time() - g.start) * 1000, 2)  # ms

        # Attach data to request object for logger
        request.duration_ms = duration
        request.status = response.status_code
        request.user_id = getattr(g, 'user_id', 'anonymous')
        request.user_type = getattr(g, 'user_type', 'unknown')

        app.logger.info("Request completed")
        return response