import time
from flask import g, request, has_request_context
from .api_logger import log_api_call 


def add_request_logging(app):
    @app.before_request
    def start_timer():
        g.start = time.time()  

    @app.after_request
    def log_request(response):
        if not has_request_context():
            return response

        if not hasattr(g, 'start'):
            return response  

        duration_ms = round((time.time() - g.start) * 1000, 2)

        log_api_call(
            status_code=response.status_code,
            duration_ms=duration_ms
        )

        user_id = getattr(g, 'user_id', 'anonymous')
        app.logger.info(
            f"{request.method} {request.path} | "
            f"{response.status_code} | "
            f"{duration_ms}ms | "
            f"User: {user_id}"
        )

        return response