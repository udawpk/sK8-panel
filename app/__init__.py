import os
from flask import Flask
from app.api.views import api_bp
from app.routes.main import main_bp
from app.routes.details import details_bp

def create_app():
    app = Flask(__name__)

    # Генеруємо випадковий секретний ключ, якщо його немає
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your-secret-key")

    # Реєструємо Blueprints
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(main_bp)
    app.register_blueprint(details_bp)

    return app
