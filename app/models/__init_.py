class Mortgage:
    '''
    Represents a mortgage that the user creates.

    This class manages the basic calculations for:
        - Miniumum down payment required
        - Mortgage insurance
        - Principal final

    Class variables include
        - min_down_payment_cutoff: minimum amount before second down payment percent is applied (500,000 CAD)
        - min_down_payment_percent_1: the percent for purchase prices below 500k CAD
        - min_down_payment_percent_2: the percent for the amount above 500k CAD
    '''

    min_down_payment_cutoff = 500000 # amount that is cutoff between minimum down payment percent 1 and 2
    min_down_payment_percent_1 = 0.05 # percent of purchase price for minimum down payment below 500K CAD
    min_down_payment_percent_2 = 0.10 # percent of purchase price for down payment amount above 500K CAD

    def __init__(self, purchase_price: float):
        '''
        Initializes the Mortgage object with starting purchase price and minimum down payment required.
        '''
        # Calculation of minimum down payment for real estate less than min_down_payment_cutoff
        if purchase_price <= self.min_down_payment_cutoff:
        
            min_down_payment = purchase_price * self.min_down_payment_percent_1

        
        # Calculation of minimum down payment for real estate less than min_down_payment_cutoff
        else:
        
            min_down_payment = ( (purchase_price - self.min_down_payment_cutoff) * self.min_down_payment_percent_2) + (self.min_down_payment_cutoff * self.min_down_payment_percent_1)