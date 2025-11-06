# Step 1: Code Utility Funtions
def linear_utility(m, a=5, b=.75):
    """linear utility of money
    
        args: m, float, amount of money.
              a, float, intercept.
              b, float, slope.
              
        returns: util, float, utility of money m.    
    """
    util = a + b*m
    return util

# test functions

m1 = 0
m2 = 10
p1 = .5
p2 = .5

# test linear_utility function
print(linear_utility(m2))
print(f"expected value = {p1*m1 + p2*m2}, expected utility = {p1*linear_utility(m1) + p2*linear_utility(m2)}")


# Additional utility functions

# 1. CARA (Constant Absolute Risk Aversion)
# 2. CRRA (Constant Relative Risk Aversion)
# 3. Quadratic utility


import math
def cara(m, a=0.5):
    """Exponential Utility Constant Absolute Risk Aversion (CARA): u(m) = 1 - exp(-a*m)

        args:
            m(float): amount of money (payoff)
            a(float): >0, absolute risk aversion parameter (larger a, more risk averse)
        
        returns:
            util: float, utility of money m

        raises:
            ValueError: if a <= 0

        Test case: 
            cara(10, a=0.5) should return approximately 0.9932620530009145
            cara(5, a=1.0) should return approximately 0.9932620530009145
    """
    if a <=0:
        raise ValueError("Parameter 'a' must be > 0.")
    util = 1 - math.exp(-a * m)
    return util #this is the CARA utility returning the utility of money
while True:
    try:
        m_val = float(input("Enter m (Money/Payoff): "))
        a_val = float(input("Enter a (> 0, risk-aversion parameter): "))
        u = cara(m_val, a=a_val)
        print(f"u(m) = {u}")
        break
    except ValueError as e:
        print(f"Input error: {e}. Please try again.\n")

import math

def crra(m, gamma=2.0):
    """Power Utility Constant Relative Risk Aversion (CRRA). 

        u(m) = (m^(1-gamma)-1) / (1 - gamma)        if gamma != 1
            = ln(m)                                if gamma ==1  
        args:
            m (float): > 0, money/wealth
            gamma (float): > 0, coefficient of relative risk aversion (larger gamma, more risk averse)

        returns: 
            util (float): utility of money m
        
        raises:
            ValueError: if m <= 0 or gamma <= 0

        Test cases:
            crra(10, gamma=2) should return approximately  -0.9
            crra(10, gamma=1) should return approximately 2.302585092
    """
    if m <= 0:
        raise ValueError("Parameter 'm' must be > 0 for CRRA utility.")
    if gamma <= 0:
        raise ValueError("Parameter 'gamma must be > 0.")
    if gamma == 1:
        return math.log(m)
    util = (m**(1 - gamma) - 1) / (1 - gamma)
    return util  #returns the normal CRRA utility when gamma not equal to 1
while True:
    try:
        m_val = float(input("Enter m (> 0, money/wealth): ")) #input for money/wealth converts to float
        gamma_val = float(input("Enter gamma (> 0, relative risk aversion): ")) #input for gamma converts to float
        utility = crra(m_val, gamma=gamma_val) #calls crra function with user inputs
        print(f"u(m) = {utility}") #prints the utility value
        break #exits the loop if successful
    except ValueError as e: #catches ValueError exceptions and inputs the error message from above
        print(f"Input error: {e} Please try again.\n")


def quadratic(m, a=1.0, b=0.1):
    """Quadratic utility: u(m) = a*m - 0.5*b*m^2
    
    args:
        m (float): money/payoff
        a (float): slope at zero wealth
        b (float): > 0, curvature parameter (keeps the function concave)
        
    returns:
        util (float): utility of money m

    raises:
        ValueError: if b <= 0 (would break concavity)
        ValueError: if a - b*m <= 0 (would make marginal utility non-positive)

    Test cases:
        quadratic(5, a=1.0, b=0.1) should return 3.75
        quadratic(15, a=2.0, b=0.2) should return 7.0
    """

    if b <= 0:
        raise ValueError("Parameter 'b' must be > 0 to keep utility concave.")
    if a - b*m <= 0:
        raise ValueError("Inputs result in non-positive marginal utility (a - b*m <= 0). Choose smaller m or larger a, or smaller b.")
    util = a*m - 0.5*b*(m**2)
    return util

while True:
    try:
        m_val = float(input("Enter m (money/payoff): "))
        a_val = float(input("Enter a (baseline slope): "))
        b_val = float(input("Enter b (> 0, curvature): "))

        utility = quadratic(m_val, a=a_val, b=b_val)
        print(f"u(m) = {utility}")
        break
    except ValueError as e:
        print(f"Input error: {e}. Please try again. \n")