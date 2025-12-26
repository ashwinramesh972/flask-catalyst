from flask import Blueprint
from flask import request
from sqlalchemy import desc
from app.schemas.user import UserOut
from app.utils.pagination import paginate
from app.utils.permissions import admin_required
from app.models.user import User

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/users")
@admin_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = min(per_page, 100)

    query = User.query.order_by(desc(User.id))

    return paginate(query, UserOut)