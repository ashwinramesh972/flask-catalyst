from flask import Blueprint
from .controllers import seed, utils_demo
from flask_jwt_extended import jwt_required
from app.utils.rate_limiter import limiter

demo_bp = Blueprint("demo", __name__, url_prefix="/demo")

demo_bp.route("/seed")(seed)
demo_bp.route("/utils-demo")(
    jwt_required()(
        limiter.limit("5 per minute")(utils_demo)
    )
)