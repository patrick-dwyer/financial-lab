from flask import Blueprint, render_template, request, jsonify
from app.services.amortization_service import AmortizationService

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

    # 2. create instance of "base" mortgage
    my_mortgage = AmortizationService(
        principal_start=500000,
        amortization_years=25,
        interest_rate=0.05,
        payment_frequency="monthly",
        term=5
    )

    # 3. capture base information 
    base_df = my_mortgage.amortization_table

    # 4. run a secondary scenario with blocks included
    scenario_df = my_mortgage._calculate_amortization_table(event_data=event_data)
    
    print(base_df.tail(5))
    print(scenario_df.tail(5))

    # 5. Pass the response back to front end
    return jsonify({
        "status": "success",
        "message": f"Python received {len(event_data)} blocks",
        "base_df": f"{len(base_df)}",
        "scenario_df": f"{len(scenario_df)}",
        # "saved_interest": 50000, # dummy data
        # "new_payoff_date": "Jan 2045" # dummy data
    })