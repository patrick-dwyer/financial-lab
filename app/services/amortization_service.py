from app.models.amortization import AmortizationRow

class AmortizationService:
    '''
    Represents the calculation of a users ammortization of their mortgage.

    This class requires:
        - principal_start: the total amount of the mortgage loan
        - interest_rate: the interest rate at which the loan is being provided by the lender
        - years: the length of time that the loan is scheduled, the amortization

    Class Variables:
        - payment_frequency: describes how many payments are put towards the mortgage each year
    '''

    # dictionary of payments per year based on frequency of payments
    payment_frequency = {
        "monthly": 12,
        "semi_monthly": 24,
        "bi_weekly": 26,
        "acc_bi_weekly": 26,
        "weekly": 52,
        "acc_weekly": 52
    }

    fixed_rate_compounding_periods = 2

    
    def __init__(self, principal_start: float, interest_rate: float, payment_frequency: str, years: int):
        self.principal = principal_start
        self.interest_rate = interest_rate
        self.payment_frequency = (payment_frequency, AmortizationService.payment_frequency[payment_frequency])
        self.years = years
        self.effecive_rate = self._calculate_effective_periodic_interest_rate()

    def _calculate_effective_periodic_interest_rate(self) -> float:
        '''
        Internal calculator to determine the interest rate applied over the course of the loan ammortization.
        This takes into account the effects of compounding.
        '''
        
        # the base growth rate per compounding period
        base_growth = 1 + (self.interest_rate / AmortizationService.fixed_rate_compounding_periods)

        # ratio of how often the bank compounds vs how often user pays
        compounding_ratio = (AmortizationService.fixed_rate_compounding_periods / self.payment_frequency[1])

        #calculate final effective rate
        effective_rate = (base_growth ** compounding_ratio) - 1

        return effective_rate

if __name__ == "__main__":
    # This only runs if you execute the file directly
    test_service = AmortizationService(
        principal_start=500000,
        interest_rate=0.03,
        payment_frequency="monthly",
        years=25
        )
    print(test_service.effecive_rate)
    print("Test successful!")


