class AmortizationRow:
    '''
    Represents a snapshot for a month within the users mortgage amortization period.

    This class represents:
        - the status of a mortgage at a certain month
        - how much has been paid overall
        - how much interst has been paid overall
        - how much principal has been paid overall
        - how much principal is remaining on the loan

    '''
    def __init__(self, month_number: int, payment: float, interest: float, principal: float, balance: float):
        self.month_number = month_number
        self.payment = payment
        self.interest_paid = interest
        self.principal_paid = principal
        self.remaining_balance = balance
