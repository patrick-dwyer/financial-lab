from app.models.amortization import AmortizationRow

class AmortizationService:
    '''
    Represents the calculation of a users ammortization of their mortgage.

    This class requires:
        - principal_start: the total amount of the mortgage loan
        - interest_rate: the interest rate at which the loan is being provided by the lender
        - years: the length of time that the loan is scheduled, the amortization
    '''
    
    def __init__(self, principal_start, interest_rate, years):
        return None