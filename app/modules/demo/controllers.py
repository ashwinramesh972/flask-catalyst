from flask import request, current_app as app
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.modules.user.models import User
from app.modules.user.schemas import UserOut
from app.utils.pagination import paginate
from app.utils.response import success, error
from app.utils.file_upload import upload_file
from app.utils.email import send_email
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
        return error(message=f"Seeding failed: {str(e)}", code=500)


def utils_demo():
    try:
        if request.method == 'GET':
            # GET — just return data
            query = User.query.order_by(User.id.desc())
            paginated = paginate(query, UserOut)
            paginated_data = paginated[0].json["data"]
            
            return success({
                "paginated_users": paginated_data,
                "current_user": get_jwt_identity(),
                "rate_limit_info": "This endpoint is rate limited to 5/min"
            }, "Utils demo fetched")

        # POST — file upload + email
        if request.method == 'POST':
            data = {}

            # File upload
            if 'file' in request.files:
                try:
                    file = request.files['file']
                    url = upload_file(file, folder="demo")
                    data["uploaded_file_url"] = url
                    app.logger.info(f"Demo file uploaded: {url}")
                except Exception as e:
                    data["file_upload_error"] = str(e)

            # Email test
            email_to = request.json.get("email") if request.is_json else ashwinramesh972@gmail.com
            if email_to:
                try:
                    send_email(
                        to=email_to,
                        subject="flask-catalyst Demo Email",
                        template="<h1>Hello from flask-catalyst!</h1><p>All utils working!</p>"
                    )
                    data["email_status"] = f"Test email sent to {email_to}"
                except Exception as e:
                    data["email_error"] = str(e)

            # Always return paginated users for POST too
            query = User.query.order_by(User.id.desc())
            paginated = paginate(query, UserOut)
            data["paginated_users"] = paginated[0].json["data"]
            data["current_user"] = get_jwt_identity()
            data["rate_limit_info"] = "This endpoint is rate limited to 5/min"

            return success(data, "All flask-catalyst backend utils demo — SUCCESS!")

    except Exception as e:
        app.logger.error(f"Utils demo failed: {str(e)}")
        return error(message="Utils demo failed", code=500)