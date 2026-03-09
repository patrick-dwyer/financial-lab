from flask import Blueprint, render_template

# Create Blueprint so the main app knows these routes exist
mortgage_routes = Blueprint('mortgage_routes', __name__)

@mortgage_routes.route('/test')
def hello_world():
    return "The handshake is working! Hello from the Mortgage Route."

@mortgage_routes.route('/main')
def main_screen():
    return render_template('index.html')