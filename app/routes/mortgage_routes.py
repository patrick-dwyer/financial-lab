from flask import Blueprint, render_template, request, jsonify
from app.services.amortization_service import AmortizationService

# Create Blueprint so the main app knows these routes exist
mortgage_routes = Blueprint('mortgage_routes', __name__)


@mortgage_routes.route('/')
def home_screen():
    return render_template('home.html')

@mortgage_routes.route('/mortgage-lab')
def mortgage_lab_screen():
    return render_template('mortgage-lab.html')

@mortgage_routes.route('/calculate', methods=['POST'])
def calculate_mortgage():
    scenarios_data = request.get_json() # This is now our list of {base: {}, events: []}
    results = []
    print(scenarios_data)

    for item in scenarios_data:
        # Each 'item' contains its own base settings and its own event blocks
        service = AmortizationService(
            principal_start=item['base']['principal'],
            amortization_years=item['base']['amortization'],
            interest_rate=item['base']['interest'],
            payment_frequency=item['base']['payment']
        )
        
        # Calculate using the blocks specific to THIS scenario
        print(item)
        res = service._calculate_amortization_table(event_data=item['events'])
        results.append(res)

    return jsonify({
        "status": "success",
        "scenarios": results # The list of dicts that updateChart() now expects
    })