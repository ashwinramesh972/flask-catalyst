import os
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'svg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(file, folder="uploads"):
    """
    Upload file with 3 options:
    - local (default) — saves to instance/uploads
    - cloudinary — uses Cloudinary
    - s3 — uses AWS S3
    Set in .env: FILE_STORAGE=local|cloudinary|s3
    """
    storage = os.getenv("FILE_STORAGE", "local").lower()

    if not allowed_file(file.filename):
        raise ValueError("File type not allowed")

    filename = secure_filename(file.filename)

    if storage == "cloudinary":
        try:
            import cloudinary.uploader
            cloudinary.config(
                cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
                api_key=os.getenv("CLOUDINARY_API_KEY"),
                api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            )
            result = cloudinary.uploader.upload(file, folder=folder)
            return result['secure_url']
        except Exception as e:
            raise ValueError(f"Cloudinary upload failed: {str(e)}")

    elif storage == "s3":
        try:
            import boto3
            s3 = boto3.client(
                's3',
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("S3_REGION", "us-east-1")
            )
            bucket = os.getenv("S3_BUCKET")
            key = f"{folder}/{filename}"
            file.seek(0)
            s3.upload_fileobj(file, bucket, key)
            return f"https://{bucket}.s3.{os.getenv('S3_REGION', 'us-east-1')}.amazonaws.com/{key}"
        except Exception as e:
            raise ValueError(f"S3 upload failed: {str(e)}")

    else:  # local — default
        upload_folder = os.path.join(current_app.instance_path, "uploads", folder)
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return f"/static/uploads/{folder}/{filename}"