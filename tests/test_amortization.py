import pytest
from amortization_service import AmortizationService

def test_base_mortgage_calculation():
    """Verify standard monthly mortgage calculation produces expected output structure."""
    service = AmortizationService(
        principal=500000,
        amortization_years=25,
        interest_rate=0.05,
        payment_frequency="Monthly"
    )
    result = service.calculate()
    
    assert "visual_principal_list" in result
    assert result["total_interest"] > 0
    assert result["payoff_month"] > 0
    # A 25-year monthly mortgage should take 300 months
    assert result["payoff_month"] == 300

def test_month_zero_lump_sum_event():
    """Verify that a Month 0 lump sum successfully reduces the starting principal."""
    # Scenario without lump sum
    service_normal = AmortizationService(
        principal=500000, amortization_years=25, interest_rate=0.05, payment_frequency="Monthly"
    )
    res_normal = service_normal.calculate()
    
    # Scenario with $50,000 lump sum at Month 0
    service_lump = AmortizationService(
        principal=500000, amortization_years=25, interest_rate=0.05, payment_frequency="Monthly"
    )
    res_lump = service_lump.calculate(event_data=[{"month": 0, "type": "Lump Sum", "value": 50000}])
    
    # Total interest and payoff time should be significantly lower with a Month 0 lump sum
    assert res_lump["total_interest"] < res_normal["total_interest"]
    assert res_lump["payoff_month"] < res_normal["payoff_month"]
    # First entry in visual principal list should reflect the reduced principal (500k - 50k = 450k)
    assert res_lump["visual_principal_list"][0] == 450000

def test_flask_app_smoke_test():
    """Smoke test to ensure Flask app starts and responds."""
    # Assuming your Flask app instance is named `app` in `app.py`
    from app import app
    client = app.test_client()
    
    response = client.get('/')
    # Expecting 200 OK or a redirect to your main view
    assert response.status_code in [200, 301, 302]