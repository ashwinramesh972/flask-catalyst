from flask_jwt_extended import get_jwt_identity
from app.modules.user.models import User
from app.modules.user.schemas import UserOut
from app.utils.pagination import paginate
from app.utils.response import success, error  
from app import db
from faker import Faker


def seed():
    try:
        if User.query.count() > 10:
            return success(message="Already seeded")

        fake = Faker()
        for i in range(100):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                role="admin" if i % 10 == 0 else "user"
            )
            user.set_password("123456")
            db.session.add(user)

        db.session.commit()
        return success(message="Seeded 100 fake users", code=201)

    except Exception as e:
        db.session.rollback()
        return error(message="Seeding failed", code=500)


def utils_demo():
    try:
        query = User.query.order_by(User.id.desc())
        paginated = paginate(query, UserOut)
        paginated_data = paginated[0].json["data"]

        return success(
            data={
                "paginated_users": paginated_data,
                "current_user": get_jwt_identity(),
                "rate_limit_info": "This endpoint is rate limited to 5/min"
            },
            message="Utils demo fetched successfully"
        )

    except Exception as e:
        return error(message="Failed to fetch demo data", code=500)