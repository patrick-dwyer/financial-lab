class Mortgage:
    '''
    Represents a mortgage scenario that the user creates.

    This class determines:
        - minimum down payment required
        - mortgage insurance
        - principal final (uninsured and insured)

    Class variables include:
        - min_down_payment_cutoff_1: minimum amount before second down payment percent is applied (500,000 CAD)
        - min_down_payment_cutoff_2: minimum amount before second down payment percent is applied (1,500,000 CAD)
        - min_down_payment_percent_1: the percent for purchase prices below 500k CAD
        - min_down_payment_percent_2: the percent for the amount above 500k CAD
        - min_down_payment_percent_3: the percent for the amount above 1.5M CAD

    Assumptions:
        - down payment will initially default to minimum value but user can override
        - mortgage insurance only taken if mandatory (loan-to-value <80%)
    '''

    min_down_payment_cutoff_1 = 500000 # amount that is cutoff between minimum down payment percent 1 and 2
    min_down_payment_cutoff_2 = 1500000 # amount that is cutoff for minimum down payment for percent 3 of purchase price

    min_down_payment_percent_1 = 0.05 # percent of purchase price for minimum down payment below 500K CAD
    min_down_payment_percent_2 = 0.10 # percent of purchase price for down payment amount above 500K CAD
    min_down_payment_percent_3 = 0.20 # percent of purchase price for down payment amount above 1.5M CAD

    def __init__(self, purchase_price: float, down_payment = None):
        '''
        Initializes the Mortgage object with Flask==3.1.3core attributes:
            - purchase_price: user input to create object. Price of real estate.
            - min_down_payment: calculated minimum down payment required based on purchase price.
            - down_payment: initial payment put against purchase price to reduce mortgage amount.
            - uninsured_principal: principal calculation without mortgage insurance (purchase_price - down_payment).
            - insured_principal: principal calculation with mortgage insurance (purchase_price - down_payment + mortgage_insurance).
        '''
        
        self.purchase_price = purchase_price # assign purchase price from user input
        self.min_down_payment = self._calculate_min_down_payment() # calculate minimum down payment
        self.down_payment =  down_payment or self.min_down_payment # User can input downpayment or default to minimum down payment
        self.uninsured_principal = self.purchase_price - self.down_payment # calculated uninsured principal amount
        self.insured_principal = self._calculate_mortgage_insurance() # calculated insured principal amount

    # Getter and setter for down payment amount
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
        '''Internal helper to calculate minimum down payment based on purchase price.
        As of 2026, three tiers of rates are <500k, 500k-1.5M, >1.5M
        '''
        
        # Rule 1: purchase price at or above min_down_payment_cutoff_2
        if self.purchase_price >= Mortgage.min_down_payment_cutoff_2:
            return self.purchase_price * Mortgage.min_down_payment_percent_3
        
        # Rule 2: purchase price at or below min_down_payment_cutoff_1
        if self.purchase_price <= Mortgage.min_down_payment_cutoff_1:
            return self.purchase_price * Mortgage.min_down_payment_percent_1
        
        # Rule 3: purchase price between min_down_payment_cutoff_1 and min_down_payment_cutoff_2
        amount_over_500k = (self.purchase_price - Mortgage.min_down_payment_cutoff_1) * Mortgage.min_down_payment_percent_2
        amount_under_500k = Mortgage.min_down_payment_cutoff_1 * Mortgage.min_down_payment_percent_1
        return amount_over_500k + amount_under_500k
    
    def _calculate_mortgage_insurance(self) -> float:
        '''
        Internal helper for mortgage insurance calculation. Dictionary is from table provided by
        Canadian Mortgage and Housing Commission (CMHC) for loan to value premium based on down payment.
        '''

        # CMHC mortgage loan insurance table as a dictionary.
        loan_to_value_premium = {
            95: 0.040,
            90: 0.031,
            85: 0.028,
            80: 0.024,
            75: 0.017,
            65: 0.006
        }

        # create list of keys in mortgage loan insurance table keys
        loan_to_value_premium_key_list = list(loan_to_value_premium)

        # Case 1: if house costs more than $1.5M CAD, can not get mortgage insurance
        if self.purchase_price >= self.min_down_payment_cutoff_2:
            return self.uninsured_principal

        # calculate loan_to_value_pct = (principal / purchase_price) * 100%
        loan_to_value_pct = round(self.uninsured_principal / self.purchase_price * 100)

        # Case 2: if down payment percent is >=20%, no mortgage insurance required
        if loan_to_value_pct <= loan_to_value_premium_key_list[-1]:
            return self.uninsured_principal
        
        # while loop to find where the loan_to_value_pct is larger than key value
        count = 0
        while loan_to_value_pct > loan_to_value_premium_key_list[count] :
            count+=1

        # Condition 1: if loan_to_value_pct is > 90%
        if count == 0:
            return (self.uninsured_principal * loan_to_value_premium[loan_to_value_premium_key_list[count]]) + self.uninsured_principal
        
        # Condition 2: Find previous index to appropriately calculate loan_to_value_pct
        else:
            return (self.uninsured_principal * loan_to_value_premium[loan_to_value_premium_key_list[count-1]]) + self.uninsured_principal