from flask import Blueprint
from .controllers import register, login

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

auth_bp.route("/register", methods=["POST"])(register)
auth_bp.route("/login", methods=["POST"])(login)