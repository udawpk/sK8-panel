# api/__init__.py

from flask import Blueprint

# Create a Blueprint for the API module
api_bp = Blueprint('api', __name__)

# Import views to register routes
from app.api import views
