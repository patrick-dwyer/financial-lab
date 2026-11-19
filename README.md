# financial-lab
An application that helps simulate financial decisions to help you with decisions.

Prospective projects include:
- Rent vs Buy comparison: tool to compare renting versus purchasing.
- Retirement Calculator: get an estimate on what your spending will be in retirement.

Current projects include:
# 🏦 Mortgage Lab

**Mortgage Lab** is an interactive financial simulation dashboard engineered to model, stress-test, and compare Canadian mortgage payoff strategies side-by-side.

Whether simulating upfront lump sums, term renewal interest rate adjustments, or custom payment changes, Mortgage Lab provides real-time visual feedback, lifetime cost breakdowns, and strict validation to keep calculations mathematically accurate and easy to digest.

## 🌟 Key Features

### 📊 Multi-Scenario Comparison Engine

* **Side-by-Side Analytics:** Compare up to **5 custom scenarios** simultaneously against a baseline.

* **Total Savings Tracking:** Automatically calculates cumulative lifetime savings by comparing each scenario against the most expensive baseline.

* **Dynamic Tab Sync:** Seamlessly switch between scenarios while keeping sidebar controls, validation messages, and minimum payment stats in lockstep.

### 🧩 Custom Event Blocks

* **Lump Sum:** Apply one-time principal prepayments at any month during the mortgage timeline (including upfront **Month 0** prepayments).

* **Payment Change:** Permanently increase or adjust regular payments to pay down principal faster.

* **Rate Change:** Model interest rate shifts for term renewals, refinancing, or variable rate fluctuations.

* **Smart Event Grouping:** Supports multiple simultaneous events executed in the exact same month.

### 🛡️ Financial Safety & Validation

* **Negative Amortization Floor:** Automatically calculates the minimum required payment based on principal, interest, and amortization. Payment changes that fall below this floor are blocked with immediate UI warnings.

* **Dual-Stat Anchor Bar:** Displays both the **Minimum Monthly Payment** anchor and the frequency-adjusted **Minimum Schedule Payment** (e.g., Bi-Weekly or Weekly).

### 📈 Interactive Charting

* **Zero-Anchored Y-Axis:** Locks the bottom of the principal axis to $\$0$ to maintain visual clarity and scale.

* **Dual-Scale X-Axis:** Displays clean yearly milestones ($Year\ 0, Year\ 1, Year\ 2\dots$) on the timeline while allowing exact month tracking.

## 🇨🇦 Canadian Mortgage Calculation Rules

Unlike US mortgages, which typically compound monthly, **Canadian fixed-rate mortgages compound semi-annually by law** ($C = 2$).

Mortgage Lab accurately incorporates Canadian compounding conventions into its core engine (`AmortizationService`):

### 1. Effective Periodic Interest Rate Formula

$$
\text{Rate per Period } (i) = \left(1 + \frac{r}{2}\right)^{\frac{2}{N}} - 1
$$

* $r$: Nominal Annual Interest Rate

* $2$: Compounding periods per year in Canada

* $N$: Number of payment periods per year

### 2. Supported Payment Schedules ($N$)

| Schedule Type | Payments per Year ($N$) | Ratio Factor | 
| ----- | ----- | ----- | 
| **Monthly** | 12 | $12 / 12$ | 
| **Semi-Monthly** | 24 | $12 / 24$ | 
| **Bi-Weekly** | 26 | $12 / 26$ | 
| **Accelerated Bi-Weekly** | 26 | $13 / 26$ | 
| **Weekly** | 52 | $12 / 52$ | 
| **Accelerated Weekly** | 52 | $13 / 52$ | 

## 📚 Canadian Mortgage Resources & Official Guidance

Understanding mortgage terms and regulatory guidelines helps when configuring scenarios. Below are official resources from Canadian financial housing authorities:

### 🏠 Canada Mortgage and Housing Corporation (CMHC)

* [CMHC Consumer Information Center](https://www.cmhc-schl.gc.ca/consumers/owning-a-home/mortgage-management) — Official guide to managing your mortgage, understanding amortization, and term renewals.

* [Prepayment Information Guide](https://www.cmhc-schl.gc.ca/professionals/project-funding-and-mortgage-financing/securitization/nha-mbs/terminology-and-calculations-for-mortgage-backed-securities/calculating-prepayment-rates) — Explains how lump sums and increased payments shorten loan terms.

### 🏛️ Government of Canada - Mortgages

* [Mortgages Resource Hub](https://www.canada.ca/en/financial-consumer-agency/services/mortgages.html) — Consumer protection guidelines regarding prepayment privileges, interest penalties, and rights upon renewal.

* [Mortgage Terms Glossary](https://www.canada.ca/en/financial-consumer-agency/services/mortgages/mortgage-terms-amortization.html) — Standardized definitions for principal, interest rate, term, and amortization.

### 🏦 Bank of Canada

* [Policy Interest Rate Track](https://www.bankofcanada.ca/core-functions/monetary-policy/key-interest-rate/) — Track historical and current policy rates to simulate realistic **Rate Change** blocks upon term renewal.

## 🛠️ Tech Stack & Architecture

* **Backend:** Python 3, Flask, Pandas (`AmortizationService` engine)

* **Frontend:** HTML5, CSS3 (CSS Variables, Flexbox/Grid), JavaScript (Vanilla ES6 modules)

* **Data Visualization:** Chart.js (visualization tool for website)

* **User Onboarding:** Intro.js (interactive step-by-step tour)

## 🚀 Getting Started

### Prerequisites

* Python 3.9+

* `pip` package manager

### Installation

1. **Clone the repository:**

   ```
   git clone https://github.com/your-username/financial-lab.git
   cd financial-lab
   
   
   ```

2. **Set up a virtual environment:**

   ```
   python3 -m venv .venv
   source .venv/bin/activate
   
   
   ```

3. **Install dependencies:**

   ```
   pip install -r requirements.txt
   
   
   ```

4. **Run the application:**

   ```
   python app.py
   
   
   ```

5. **Access the Dashboard:**
   Open your browser and navigate to `http://127.0.0.1:5000/mortgage-lab`.

## 🤝 Contributing & License

Contributions, bug reports, and feature requests are welcome! Feel free to check the issues page or submit a pull request.

*Distributed under the MIT License.*
