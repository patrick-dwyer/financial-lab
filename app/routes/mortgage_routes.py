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

    print()
    # 2. create instance of "base" mortgage
    my_mortgage = AmortizationService(
        principal_start= event_data[0]['principal'],
        amortization_years= event_data[0]['amortization'],
        interest_rate= event_data[0]['interest'],
        payment_frequency= event_data[0]['payment']
    )

    # 3. capture base information 
    base = my_mortgage.amortization_table 

    # slice out data related to base mortgage
    event_data = event_data[1:]

    # 4. run a secondary scenario with blocks included
    scenario = my_mortgage._calculate_amortization_table(event_data=event_data)

    # 5. Pass the response back to front end
    return jsonify({
        "status": "success",
        "message": f"Python received {len(event_data)} blocks",
        "base_principal": base['current_principal_list'],
        "scenario_principal": scenario['current_principal_list']

    })