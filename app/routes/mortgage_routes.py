from flask import Blueprint, render_template, request, jsonify
from app.services.amortization_service import AmortizationService

# Create Blueprint so the main app knows these routes exist
mortgage_routes = Blueprint('mortgage_routes', __name__)


@mortgage_routes.route('/')
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
    base = my_mortgage.amortization_table 

    # 4. run a secondary scenario with blocks included
    scenario = my_mortgage._calculate_amortization_table(event_data=event_data)

    # 5. Pass the response back to front end
    return jsonify({
        "status": "success",
        "message": f"Python received {len(event_data)} blocks",
        "base_principal": base['current_principal_list'],
        "scenario_principal": scenario['current_principal_list']

    })