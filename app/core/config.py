import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_PATH = os.path.join(BASE_DIR, "..", "..", "instance")

class Config:
    PROJECT_NAME = "flask-catalyst"
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-change-me")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(INSTANCE_PATH, 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 24 * 60 * 60
    JWT_REFRESH_TOKEN_EXPIRES = 30 * 24 * 60 * 60
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/db")


config_by_name = {
    "default": Config,
    "development": Config,
    "production": ProductionConfig,
}