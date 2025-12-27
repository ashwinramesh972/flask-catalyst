from flask import Blueprint
from .controllers import index

leave_bp = Blueprint(
    "leave",
    __name__,
    url_prefix="/leave"
)

leave_bp.route("", methods=["GET"])(index)
