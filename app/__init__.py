from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .utils.error_handler import register_error_handlers
from .utils.logger import setup_logger
from .utils.middleware import add_request_logging


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()


def create_app(config_name: str = "default"):
    from .core.config import config_by_name

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    register_error_handlers(app)
    setup_logger(app)
    add_request_logging(app)

    # Register API blueprint
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy", "project": "flask-catalyst"}), 200
    
    

    return app