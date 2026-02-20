class Mortgage:
    '''
    Represents a mortgage that the user creates.

    This class manages the basic calculations for:
        - Miniumum down payment required
        - Mortgage insurance
        - Principal final

    Class variables include
        - min_down_payment_cutoff_1: minimum amount before second down payment percent is applied (500,000 CAD)
        - min_down_payment_cutoff_2: minimum amount before second down payment percent is applied (1,500,000 CAD)
        - min_down_payment_percent_1: the percent for purchase prices below 500k CAD
        - min_down_payment_percent_2: the percent for the amount above 500k CAD
        - min_down_payment_percent_3: the percent for the amount above 1.5M CAD
    '''

    min_down_payment_cutoff_1 = 500000 # amount that is cutoff between minimum down payment percent 1 and 2
    min_down_payment_cutoff_2 = 1500000 # amount that is cutoff for minimum down payment for percent 3 of purchase price
    min_down_payment_percent_1 = 0.05 # percent of purchase price for minimum down payment below 500K CAD
    min_down_payment_percent_2 = 0.10 # percent of purchase price for down payment amount above 500K CAD
    min_down_payment_percent_3 = 0.20 # percent of purchase price for down payment amount avoe 1.5M CAD

    def __init__(self, purchase_price: float):
        '''
        Initializes the Mortgage object with starting purchase price and minimum down payment required.
        '''
        self.purchase_price = purchase_price
        self.min_down_payment = self._calculate_min_down_payment()
        self.down_payment = self.min_down_payment

    @property
    def down_payment(self):
        '''Getter: Returns the value when you call variable.down_payment'''
        return self._down_payment
    
    @down_payment.setter
    def down_payment(self, value: float):
        '''Setter: runs logic when you try to change this value'''
        if value < self.min_down_payment:
            raise ValueError(f"Down payment {value} is below the legal minimum of {self.min_down_payment}")
        
        self._down_payment = value
        

    def _calculate_min_down_payment(self) -> float:
        '''Internal helper to calculate minimum down payment based on purchase price.'''

        # Rule 1: purchase price at or above $1,500,000
        if self.purchase_price >= Mortgage.min_down_payment_cutoff_2:
            return self.purchase_price * Mortgage.min_down_payment_percent_3
        
        # Rule 2: purchase price at or below $500,000
        if self.purchase_price <= Mortgage.min_down_payment_cutoff_1:
            return self.purchase_price * Mortgage.min_down_payment_percent_1
        
        # Rule 3: purchase price between $500,000 and $1,500,000
        amount_over_500k = (self.purchase_price - Mortgage.min_down_payment_cutoff_1) * Mortgage.min_down_payment_percent_2
        amount_under_500k = Mortgage.min_down_payment_cutoff_1 * Mortgage.min_down_payment_percent_1
        return amount_over_500k + amount_under_500k
    
    def _calculate_mortgage_insurance(self) -> float:
        return None



my_mortgage = Mortgage(650000)
print(f"Purchase price: {my_mortgage.purchase_price}, Min down payment: {my_mortgage.min_down_payment}")
my_mortgage.down_payment = 25000
print(my_mortgage.down_payment)

# m = Mortgage(600000)
# print(m.down_payment)
# m.down_payment=750000
# m.down_payment=100