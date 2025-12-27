from flask import request
from sqlalchemy import desc
from app.modules.user.models import User
from app.modules.user.schemas import UserOut
from app.utils.pagination import paginate

def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    per_page = min(per_page, 100)

    query = User.query.order_by(desc(User.id))
    return paginate(query, UserOut)