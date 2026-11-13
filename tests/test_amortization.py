import pytest
from app.services.amortization_service import AmortizationService
from app import create_app  # Import your application factory

def test_base_mortgage_calculation():
    """Verify standard monthly mortgage calculation produces expected output structure."""
    result = AmortizationService(
        principal_start=500000,
        amortization_years=25,
        interest_rate=0.05,
        payment_frequency="monthly"
    )
    
    assert 'visual_principal_list' in result.amortization_table
    assert result.amortization_table['total_interest'] > 0
    assert result.amortization_table['payoff_month'] > 0
    assert result.amortization_table['payoff_month'] == 300

def test_flask_app_smoke_test():
    """Smoke test to ensure Flask app starts and responds using the factory pattern."""
    app = create_app()
    client = app.test_client()
    
    response = client.get('/')
    assert response.status_code in [200, 301, 302]


### test functions
# test_base_mortgage_calculation()
# test_flask_app_smoke_test()