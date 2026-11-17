import os
from dotenv import load_dotenv

# load .env variable when app package initializes
load_dotenv()

from flask import Flask

def create_app():
    # Initialize the Flask application
    app = Flask(__name__)

    # Define env and load configurations dynamically
    env = os.environ.get('FLASK_ENV', 'development')
    
    if env == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    with app.app_context():
        # Import routes here to avoid circular imports
        from .routes.mortgage_routes import mortgage_routes
        
        # Register Blueprints
        app.register_blueprint(mortgage_routes)

    return app