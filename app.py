# app.py

from flask import Flask
from app.api import api_bp
from app.routes.main import main_bp
from app.routes.details import details_bp


def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(details_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=8000, debug=True)
