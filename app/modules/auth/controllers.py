from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from app.modules.user.models import User
from app import db
from app.utils.rate_limiter import limiter
from app.utils.response import success, error
from flask import current_app as app
from app.utils.debug_logger import debug_log

def register():
    try:
        data = request.get_json()
        if not data:
            return error("No data provided", 400)

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not all([username, email, password]):
            return error("Username, email and password are required", 400)

        if User.query.filter_by(username=username).first():
            return error("Username already exists", 400)
        if User.query.filter_by(email=email).first():
            return error("Email already exists", 400)

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return success(
            message="User created successfully",
            data={"user": user.to_dict()},
            code=201
        )

    except Exception as e:
        db.session.rollback()
        return error("Registration failed", 500)


@limiter.limit("10 per minute")
def login():
    try:
        data = request.get_json()
        if not data:
            return error("No data provided", 400)

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return error("Username and password required", 400)

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))

            debug_log("username", username)

            return success(
                data={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user.to_dict()
                },
                message="Login successful"
            )

        return error("Invalid credentials", 401)

    except Exception as e:
        return error("Login failed", 500)