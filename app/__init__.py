from flask import Flask

def create_app():
    # Initialize the Flask application
    app = Flask(__name__)

    # Load configurations (optional, but good practice)
    app.config.from_object('config.Config')

    with app.app_context():
        # Import routes here to avoid circular imports
        from .routes.mortgage_routes import mortgage_routes
        
        # Register Blueprints (this keeps your routes organized)
        app.register_blueprint(mortgage_routes)

        return app