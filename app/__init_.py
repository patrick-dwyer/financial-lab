# app/__init__.py
__version__ = "0.0.1"
__author__ = "Patrick Dwyer"

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create database object
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configure the app
    app.config('SQLALCHEMY_DATABASE_URI') = 'sqlite:///project.db'

    # Connect the database object to this app
    db.init_app(app)

    # Register routes
    from .routes.main_routes import main_bp
    app.register_blueprint(main_bp)

    return app



