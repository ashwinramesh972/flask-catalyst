from flask import g
from functools import wraps
from .response import error
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.modules.user import User

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if not user or user.role != required_role:
                return error("Forbidden — insufficient permissions", 403)
            g.user = user  
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return role_required("admin")(f)