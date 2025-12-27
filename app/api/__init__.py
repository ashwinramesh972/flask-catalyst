from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api")

from app.modules.auth import auth_bp
from app.modules.admin import admin_bp
from app.modules.demo import demo_bp
from app.modules.leave import leave_bp

api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(admin_bp)
api_bp.register_blueprint(demo_bp)
api_bp.register_blueprint(leave_bp)
