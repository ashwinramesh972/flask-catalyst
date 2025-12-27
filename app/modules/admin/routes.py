from flask import Blueprint
from .controllers import get_users
from app.utils.permissions import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

admin_bp.route("/users")(admin_required(get_users))