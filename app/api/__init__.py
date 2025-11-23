from flask import Blueprint

api_bp = Blueprint("api", __name__)

# Import routes so they get registered
from .auth import *