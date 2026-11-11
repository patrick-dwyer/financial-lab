from asyncio import events

import pandas as pd

class AmortizationService:
    '''
    Represents the calculation of a user's amortization of their mortgage.

    This class requires:
        - principal_start: the total amount of the mortgage loan
        - interest_rate: the interest rate at which the loan is being provided by the lender
        - amortization_years: the length of time that the loan is scheduled, the amortization
        - payment_frequency: what type of schedule you plan to pay off your loan (monthly, semi-monthly, bi-weekly, etc)

    Class variables:
        - payment_frequency: describes how many payments are put towards the mortgage each year
        - months_in_a_year: variable used to represent 12 months in a year for calculations
        - fixed_rate_compounding_periods: in Canada, any fixed rate mortgage only compounds 2 times a year

    Class methods:
        __init__: initializes core attributes for the AmortizationService object.
        _calculate_interest__rate: calculate interest rate of each payment.
        _calculate_monthly_payment_anchor: calculate monthly payment amount.
        _calculate_amortization_table: calculate base amortization table for mortgage.

    '''

    '''
    payment_frequency dictionary: tuples that include
        - index 0: payments per year based on frequency of payments
        - index 1: factor based on number payment months / number of payments
    '''
    payment_frequency = {
        "monthly":        (12, 12/12),
        "semi_monthly":   (24, 12/24),
        "bi_weekly":      (26, 12/26),
        "acc_bi_weekly":  (26, 13/26),
        "weekly":         (52, 12/52),
        "acc_weekly":     (52, 13/52)
    }

    # number of months in a year
    months_in_a_year = 12

    # number of periods that compound interest is calculated on a fixed rate mortgage in Canada
    fixed_rate_compounding_periods = 2

    
    def __init__(
            self, 
            principal_start: float, 
            interest_rate: float, 
            amortization_years: int, 
            payment_frequency: str
            ):
        
        '''
        Initialize core attributes for AmmortizationService
            - principal_start: the starting principal of the mortgage loan.
            - interest_rate: the posted interest rate provided for the start of the mortgage.
            - amortization_years: the total length in years of the mortgage loan.
            - monthly_anchor_interest_rate: the effective interest rate calculated over 12 payments in a year.
            - total_number_of_payments: the total amount of payments over your mortgage lifespan at a monthly payment frequency.
            - monthly_anchor_payments: the amount paid for a frequency of monthly payments over your mortgage.
            - payment_frequency: tuple that holds two parts.
                1) the payment frequency that was inputted by the user (i.e. monthly, semi-monthly, bi-weekly, etc.).
                2) another tuple that holds in position 0 the number of payments in a year and position 1 the ratio of months paid to payments made in that year.
            - min_payment_per_frequency: calculates the minimum payment amount required for the specific frequency provided by the user.
            - amortization_table: table of principal, interest, and a new principal balance after every payment at a set frequency.
        '''

        self.principal = principal_start
        self.interest_rate = interest_rate
        self.amortization_years = amortization_years
        self.monthly_anchor_interest_rate = self._calculate_interest_rate(self.interest_rate, AmortizationService.months_in_a_year)
        self.total_number_of_payments = self.amortization_years * AmortizationService.months_in_a_year
        self.monthly_anchor_payments = self._calculate_monthly_payment_anchor()
        self.payment_frequency = (payment_frequency, AmortizationService.payment_frequency[payment_frequency])
        self.min_payment_per_frequency = self.monthly_anchor_payments * self.payment_frequency[1][1]
        self.amortization_table = self._calculate_amortization_table()
        

    def _calculate_interest_rate(self, interest_rate, payment_frequency) -> float:
        '''
        Calculate the interest rate calculated on each payment.

        Formula is i = [(1 + r/C)**C/N] - 1
        
        (i) Effective Periodic Interest Rate
        (r) Nominal Annual Interest Rate
        (C) Compounding periods (in Canada, fixed rate is 2)
        (N) Payment Periods
        '''

        growth_base = 1 + (interest_rate / 2)

        compounding_to_payment_ratio = 2 / payment_frequency

        return (growth_base ** compounding_to_payment_ratio) - 1        
    
    def _calculate_monthly_payment_anchor(self) -> float:
        '''
        Internal calculator to determine the monthly payment basis of loan.

        Formula is [P * i] / [1 - (1 + i )**-n ]

        (p) Principal
        (i) Monthly Effective Interest Rate
        (n) Total number of monthly periods
        '''
        
        # the cost of borrowing against the principal
        principal_interest = self.principal * self.monthly_anchor_interest_rate

        # discount factor that spreads the principal and interest over the total number of periods
        discount_factor = 1 - (1 + self.monthly_anchor_interest_rate)**-(self.total_number_of_payments)

        # combinator of the two factors to determin the base monthly payments
        return principal_interest / discount_factor   

    def _calculate_amortization_table(self, event_data=None):
        '''
        Internal calculator to create a table representing all payments over the mortage.

        This does take into account what your actual payments and interest rate are depending
        on what type of payment schedule you have selected (monthly, semi_monthly, weekly, acc_weekly, etc)
        '''   

        # local copy of principal and interest rate
        current_principal = self.principal
        current_annual_rate = self.interest_rate
        payment_per_frequency = self.min_payment_per_frequency

        # catch any data from front end input blocks
        # Group events by month into lists to allow multiple events on the same date
        events = {}
        for item in (event_data or []):
            m = int(item['month'])
            if m not in events:
                events[m] = []
            events[m].append(item)
        
        # data frame to hold information from each monthly payment
        amortization_df = pd.DataFrame(
            data=None,
            columns=["interest_paid", "principal_paid", "new_principal_balance"]
        )

        # calculate per payment interest rate 
        payment_interest_rate = self._calculate_interest_rate(
            current_annual_rate,
            self.payment_frequency[1][0]
        )
        
        # loop to calculate each payment to principal and interest
        total_steps = int(self.total_number_of_payments * (1/ self.payment_frequency[1][1]))
        for month in range(1, total_steps + 2):           
            
            ## dynamic section to include block alterations
            if month in events:
                for block in events[month]:
                    
                    # determine which type of event: Lump Sum, Rate Change or Payment Change
                    if block['type'] == "Lump Sum":
                        current_principal -= block['value']
                        
                    elif block['type'] == "Rate Change":
                        current_annual_rate = block['value']

                        # payment change involves recalculating the interest rate per payment
                        payment_interest_rate = self._calculate_interest_rate(
                            current_annual_rate,
                            self.payment_frequency[1][0]
                        )
                    elif block['type'] == "Payment Change":
                        payment_per_frequency = block['value']

            ## main loop logic for calculations
            # calculate interest owed
            interest_paid = current_principal * payment_interest_rate

            # calculate how much of your payment is principal
            principal_paid = payment_per_frequency - interest_paid

            # deduct principal payment from total principal
            current_principal -= principal_paid

            # add row to amortization_df
            amortization_df.loc[len(amortization_df)] = [interest_paid, principal_paid, current_principal]
            
            # stop loop when payments are completed
            if current_principal <= 0:
                break
        
        ## calculate monthly representation of principle for visual
        # capture list of table for principal values
        current_principal_list = amortization_df['new_principal_balance'].tolist()

        # find number that represents "payments per year" (i.e. 52 for weekly)
        payments_per_year = self.payment_frequency[1][0]

        # calculate fractional step to get 1 month (i.e. weekly: 52 / 12 = 4.333)
        step = payments_per_year / 12

        # create downsampled list for chart
        down_sampled_principal = [self.principal] # start with beginning principal

        # loop to calculate downsampled list
        month = 1
        while True:

            # calculate the exact target month for list
            target_index = round(month * step) - 1

            # check if index exists in full table
            if target_index < len(current_principal_list):
                balance = current_principal_list[target_index]
                down_sampled_principal.append(balance)

                # break if we hit $0
                if balance <= 0:
                    break
                
                # move to next month
                month += 1
            
            else:
                # safety to try and append last number if loop ends and we have not hit 0 yet!
                if down_sampled_principal[-1] != current_principal_list[-1]:
                    down_sampled_principal.append(current_principal_list[-1])
                break
        
        

        # sum of all interest rows paid
        total_interest = amortization_df['interest_paid'].sum()
        
        # take into account that final value might be <0
        payoff_month = len(down_sampled_principal) - 1

        return {
            "visual_principal_list": down_sampled_principal,
            "total_interest": total_interest,
            "payoff_month": payoff_month,
            "frequency_payment": payment_per_frequency,
            "base_min_payment": self.min_payment_per_frequency
        }


if __name__ == "__main__":
    # This only runs if you execute the file directly
    test_service = AmortizationService(
        principal_start=500000,
        amortization_years=25,
        interest_rate=0.05,
        payment_frequency="monthly"
        )
    print(test_service.amortization_table)
    
    print("Test successful!")



