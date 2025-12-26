from flask import jsonify
from .response import error

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return error("Bad request", 400)

    @app.errorhandler(401)
    def unauthorized(e):
        return error("Unauthorized — invalid or missing token", 401)

    @app.errorhandler(403)
    def forbidden(e):
        return error("Forbidden — you don't have permission", 403)

    @app.errorhandler(404)
    def not_found(e):
        return error("Resource not found", 404)

    @app.errorhandler(422)
    def validation_error(e):
        return error("Validation failed", 422, e.exc.messages if hasattr(e, 'exc') else {})

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f"Server Error: {e}")
        return error("Internal server error", 500)


    # JWT Errors (current Flask-JWT-Extended)
    from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError, WrongTokenError

    @app.errorhandler(NoAuthorizationError)
    @app.errorhandler(InvalidHeaderError)
    @app.errorhandler(WrongTokenError)
    def jwt_error(e):
        return error("Invalid or missing token", 401)