from flask import Blueprint, render_template, request, jsonify
# from app.services.amortization_service import AmortizationService

# Create Blueprint so the main app knows these routes exist
mortgage_routes = Blueprint('mortgage_routes', __name__)

@mortgage_routes.route('/test')
def hello_world():
    return "The handshake is working! Hello from the Mortgage Route."

@mortgage_routes.route('/main')
def main_screen():
    return render_template('index.html')

@mortgage_routes.route('/calculate', methods=['POST'])
def calculate_mortgage():
    # 1. Receive data from front end
    event_data = request.get_json()

    # 2. Pass data to AmortizationService (Placerholder logic for now)
    # result = AmortizationService.calculate(event_data)

    # Just for testing the handshake, let's print it to the terminal
    print(f"Received fron Front End: {event_data}")

    # 3. Pass the re-calculation back to the front end
    # For now, we return a "success" message so the JS "Promise" resolves
    return jsonify({
        "status": "success",
        "message": f"Python received {len(event_data)} blocks",
        "saved_interest": 50000, # dummy data
        "new_payoff_date": "Jan 2045" # dummy data
    })