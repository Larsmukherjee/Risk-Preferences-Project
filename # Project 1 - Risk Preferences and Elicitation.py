# Project 1:  Risk Preferences and Elicitation 

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


# Step Two: Design and code lottery data structure  

def input_lottery():
    """Builds a lottery from user input
    
        returns:  lottery, a list of dictionaries
            each dictionary has keys 'out' (outcome) and 'prob' (probability)
        
        Test case:
            If user inputs a 2-outcome lottery with outcomes 10 (prob 0.4) and 20 (prob 0.6), the function should return:
            [{'out': 10.0, 'prob': 0.4}, {'out': 20.0, 'prob': 0.6}]
    """
    tol = 1e-9 #small tolerance I got from class to deal with rounding error
    lottery = [] #starts empty list to hold lottery outcomes

    while True:
        try:
            num_outcomes = int(input("How many outcomes in this lottery? (integer >= 1): "))
            if num_outcomes >= 1:
                break
            else:
                print("Please enter an integer >= 1.\n")
        except ValueError as e:
            print(f"Input error: {e}. Please try again.\n") #keeps asking until valid input
    remaining_prob = 1.0 
    for outcome_number in range(1, num_outcomes+1): #loops through each outcome
        while True: #asks user to specify outcome type until valid input
            type = input(f"Outcome {outcome_number}: type 'n' for numeric payoff, 'l' for nested lottery: ").strip() #gets user input for outcome type and removes whitespace
            if type in ("n", "l"): #checks if input is valid
                break
            print("Please type 'n' or 'l'.\n") #prompts user to re-enter if input invalid
        if type == "n":
            while True:
                try:
                    out_val = float(input(f"Enter payoff for outcome {outcome_number}: ")) #asks user for numeric payoff
                    break
                except ValueError as e:
                    print(f"Input error: {e}. Please try again.\n") #prompts user to re-enter if input invalid. payoff must be a number >= 1
        else:
            print(f"Building nested (compound) lottery for outcome {outcome_number}...") 
            out_val = input_lottery() #calls input_lottery function recursively to build nested lottery. This means the outcome itself is another lottery.
        if outcome_number < num_outcomes: #for all but last outcome, ask for probability
             while True: #asks user to specify probability until valid input
                try:
                    prob_val = float(input(f"Enter probability for outcome {outcome_number} (remaining {remaining_prob:.6f}): ")) #asks user for probability and tells user remaining probability with 6 decimal places
                    if prob_val < 0:
                        print("Probability must be >= 0.\n") 
                    elif prob_val > remaining_prob + tol: #checks if probability exceeds remaining probability plus tolerance
                        print(f"Probability cannot exceed the remaining {remaining_prob:.6f}.\n") #prompts user to re-enter if probability too large
                    else:
                        remaining_prob -= prob_val #updates remaining probability
                        break
                except ValueError as e:
                    print(f"Input error: {e}. Please try again.\n") 
        else:
            prob_val = remaining_prob #for last outcome, set probability to remaining
            if prob_val < -tol or prob_val > 1 + tol: #checks if final probability is valid within tolerance
                raise ValueError("Probabilities do not sum to 1. Please restart the lottery input.") #raises error if probabilities dont sum to 1
            prob_val = max(0.0, min(1.0, prob_val)) #clamps prob_val between 0 and 1
            print(f"Setting probability for outcome {outcome_number} to the remaining {prob_val:.6f} so total sums to 1.") #prints auto-set message
        lottery.append({'out': out_val, 'prob': prob_val}) #adds outcome and probability to lottery list
    return lottery 
print("Your lottery:", input_lottery())


import random #import random module for generating random numbers
def make_random_lotteries(number=2, max_pay = 100, compound=False, negative=False):
    """Builds a random list of lotteries
    
        Lottery payoffs are random draws beteen min_pay and max_pay,
        Lottery probabilities are random uniform draws that sum to one.
    
        args:
            number = int > 0, number of lotteries in list.
            compound = bool, if True allows compound lotteries one deep,
            negative = bool, if False min_pay = 0, if True min_pay = -max_pay. 
            max_pay = float > 0, maximum payoff in lottery.
        returns:
            lotteries, list of lotteries (each lottery is a list of dictionaries with keys 'out' and 'prob')
        
        Test case:
            make_random_lotteries(number=2, max_pay=100, compound=False, negative=False) might return:
            [[{'out': 23.5, 'prob': 0.3}, {'out': 75.2, 'prob': 0.7}], [{'out': 10.1, 'prob': 0.5}, {'out': 90.4, 'prob': 0.5}]]
    """
    min_pay = -float(max_pay) if negative else 0.0 #min_pay will be the negative of max_pay if it's negative
    max_pay = float(max_pay)
    def _simple_lottery():
        num_outcomes = random.randint(2, 10) #2-10 possible outcomes
        payoffs = [random.uniform(min_pay, max_pay) for _ in range(num_outcomes)] #random payoffs between min_pay and max_pay. Makes (num_outcomes) payoffs. Not using the loop number, so I wrote _
        weights = [random.random() for _ in range(num_outcomes)] #generates random weights for each outcome. Makes (num_outcomes) weights. Not using the loop number, so I wrote _
        total = sum(weights)
        probs = [w / total for w in weights] #normalizes weights to sum to 1
        return [{'out': payoffs[num_outcomes], 'prob': probs[num_outcomes]} for num_outcomes in range (num_outcomes)] #returns list of dictionaries for the simple lottery
    lotteries = [] #list to hold all lotteries
    for _ in range(number): #loops to create 'number' lotteries
        lot = _simple_lottery() #creates a simple lottery
        if compound: #if compound is True, makes one outcome a nested lottery
            outcome_idx = random.randrange(len(lot)) #selects random index in lottery
            lot[outcome_idx]['out'] = _simple_lottery() #replaces outcome at that index with another simple lottery
        lotteries.append(lot) #adds the lottery to the list of lotteries
    
    return lotteries
from pprint import pprint #import pprint for pretty-printing complex structures
pprint(make_random_lotteries())
print() #print a blank line for readability
pprint(make_random_lotteries(number=3, max_pay=50, compound=True, negative=True))


# Step Three: Code an expected value function and expected utility function

def expected_value(lottery):
    """Calculate expected value of a lottery
    
        arg:
            lottery, list of dictioaries
        
        returns:
            ev, float, expected value of the lottery
    """
    ev = 0.0 #starting the expected value at 0.0 to add to through the code
    for dict in lottery: #loops through each dictionary in the lottery list
        out = dict['out'] #gets the outcome from the dictionary
        prob = dict['prob'] #gets the probability from the dictionary
        if isinstance(out, list): #if (out) is a list, this outcome is a compound or nested lottery
            ev += prob * expected_value(out) #getting the expected value of the inner lottery (out) and multilping it by the outcomes probabiliy p. This is the weight added to the running total ev
        else:
            ev += prob * float(out) #here (out) is just a number so I made it a float and multiplied by probablility to get weight to add to ev
        
    #TODO Expected Value Calculation
    return ev

# Text expected value function
lottery = [{'out':0, 'prob':0.5}, {'out':10, 'prob':0.5}]
print(f"expected value = {expected_value(lottery)}")
compound_lottery = [{'out':lottery, 'prob':0.5}, {'out':10, 'prob':0.5}]
print(f"expected value = {expected_value(compound_lottery)}")


# You can always assign a variable to a function and pass a function to a function.  Here is an example.

def u(m, f):
    return f(m)
    
m = 10
util = linear_utility
print(type(util), util)

print(f"utility of {m} = {u(m, util)}")
print('or')
print(f"utility of {m} = {u(m, linear_utility)}")


def expected_utility(lottery, u):
    """Calculate expected utility of a lottery
    
        arg:
            lottery, list of dictioaries containing 
                     keys, values {'prob': pr, 'outcome': out}
                         pr, float between 0.0 and 1.0 inclusive
                         out, either another lottery or a float payoff
                     
            u, utility function, returns utility of a payoff outcome
        
        returns:
            eu, float, expected utility of the lottery
    """
    eu = 0.0 #starting expected utility at 0.0 to add to through the code
    for dict in lottery: #loops through each dictionary in the lottery list
        prob = dict['prob'] #gets the probability from the dictionary
        out = dict.get('out') # gets the outcome from the dictionary 
        if isinstance(out, list): #if (out) is another lottery
            eu += prob * expected_utility(out, u) #if (out) is another lottery, this is recursion
        else: 
            eu += prob * u(float(out)) #calculates utility of outcome and weights by probability to add to expected utility

    # TODO: Insert Code Here
    return eu


#Test for the expected utility function
lottery = [{'out': 0, 'prob': 0.5}, {'out': 10, 'prob': 0.5}]
print(f"expected utility = {expected_utility(lottery, linear_utility)}")

compound_lottery = [{'out': lottery, 'prob': 0.5}, {'out': 10, 'prob': 0.5}]
print(f"expected utility = {expected_utility(compound_lottery, linear_utility)}")


# Step Four: complementary functions


def reduce_lottery(lottery):
    """ Reduces compound lottery to a simple lottery.
    
        A compound lottery has sub-lotteries as outcomes.
        A simple lottery only has payoffs as outcomes.
        
        args:
            lottery, list of dictionaries. Each dictionary has keys:
                'out': either a float payoff or another lottery (list of dictionaries)
                'prob': float probability of this outcome.
        returns:
            simple_lottery, list of dictionaries with no sub-lottery.
    """
    payoff_prob = {} #starts a dictionary to hold payoffs and their total probabilities

    def walk(Lot, weight): #walks down each sub-lottery and multiplies probabilities until it gets to a numerical value instead of another sub-lottery
        for outcome in Lot: #for each outcome dictionary in this lottery list
            prob = outcome['prob'] * weight #multipy the probability on each sub branch by the probability that we got already (weight)
            out = outcome['out'] #gets the outcome from the dictionary
            if isinstance(out, list):#if the outcome is another lottery, go deeper, and carry the multiplied probablility 
                walk(out, prob) #recursion to go deeper into the sub-lottery
            else:
                x = float(out) #when the outcome is a number instead of a sub-lottery, convert to float
                payoff_prob[x] = payoff_prob.get(x, 0.0) + prob #if the payoff is a number, add the probability to the total for that payoff in the dictionary
    walk(lottery, 1.0) #starts the walking process with initial weight of 1.0

    simple_lottery = [{'out': x, 'prob': payoff_prob[x]} for x in sorted(payoff_prob)] #builds the simple lottery list of dictionaries from the payoff_prob dictionary
    return simple_lottery


#example for reduced lottery above
inside_lottery = [{'out': 0, 'prob': 0.5}, {'out': 10, 'prob': 0.5}]

outside_lottery = [{'out': inside_lottery, 'prob': 0.6}, {'out': 10, 'prob': 0.4}]

print(reduce_lottery(outside_lottery))

"""What is happening in the output?
since the walk starts with a weight of 1, it is multiplied by the first probability of 0.6 for the outside lottery, giving 0.6*0.5 = 0.3 for the outcome of 0, and 0.6*0.5 = 0.3 for the outcome of 10 from the inside lottery.
Then, the second outcome of the outside lottery is just a direct outcome of 10 with probability 0.4.
For the final simple lottery, the outcome of 0 has probability 0.3, and the outcome of 10 has total probability 0.3 + 0.4 = 0.7.
"""


def certainty_equivalent(lottery, u):
    """ Returns the certainty equivalent (ce) of a lottery.
    
        u(ce) = expected_utility(lottery, u)
        
        args:
            lottery, list of dictionaries.
            u, utility function defined over payoffs.
        returns:
            ce, float, certainty equivalent
    """
    eu = expected_utility(lottery, u) #eu is the probablility weighted average of utilities of all outcomes in the lottery

    simple = reduce_lottery(lottery) #from the previous code block, gets rid of any sub-lotteries
    low = min(outcome['out'] for outcome in simple) #go through all the outcomes in the simple and find the minimum
    high = max(outcome['out'] for outcome in simple) #go through all the outcomes in the simple and find the maximum

    if abs(high-low) < 1e-12: #if the max and min found above are the same (within tolerance), the certainty equivalent will just be that payoff
        return float(low) #returns the payoff as a float
    
    for _ in range(100): #using _ since we don't need the loop index and just want to repeat 100 times
        mid = 0.5 * (low + high) #finding the middle point between low and high 
        if u(mid) < eu: #if the mid point is less than expected utility, the payoff is too low
            low = mid #move the low up to mid to create a new lower bound
        else:
            high = mid #this means payoff is too high so we move high down to mid point to create a new upper bound
        if (high - low) < 1e-9: #if the interval between the max and min tests gets small enough, return the midpoint as the certainty equivalent
            break
    return 0.5 * (low + high)


#example for certainty equivalent
def linear_utility(m, a=5, b=0.75):
    return a + b*m
lottery = [{'out': 0, 'prob': 0.5}, {'out': 10, 'prob': 0.5}]

print(certainty_equivalent(lottery, linear_utility))

def risk_premium(lottery, u):
    """ Returns the risk premium (rp) of a lottery.
    
        rp = expected_value(lottery) - certainty_equivalent(lottery, u)
        
        args:
            lottery, list of dictionaries.
            u, utility function defined over payoffs.
        returns:
            rp, float, risk premium
    """
    ev = expected_value(lottery) #expected value of the lottery
    tol = 1e-9 #tolerance to deal with rounding error
    ce = certainty_equivalent(lottery, u)

    rp = ev - ce #risk premium is expected value minus certainty equivalent
    if abs(rp) < tol: #if risk premium is very close to 0 within tolerance
        rp = 0.0 #sets risk premium to exactly 0.0
    return float (rp) 



# Step Five:  Lottery choice function


def lottery_choice(lottery_list, u):
    """Calculate expected utility of a lottery
    
        arg:
            lottery_list, list of lotteries 
            u, utility function, returns utility of a payoff outcome
        
        returns:
            lottery_index, eu  expected utility of the lottery
        
            the index of the lottery in lottery_list with the highest expected utility and its expected utility value
    """
    eu = 0.0 #stores the expected utility of the best lottery
    lottery_index = None #stores the index of the best lottery in None

    best_eu = float("-inf") #stores the best EU at negative infinity so it's lower than any possible expected utility
    best_idx = None #stores the index of the best lottery at None

    for lot_idx, lot in enumerate(lottery_list): #loops through each lottery in the lottery list
        eu_current = expected_utility(lot, u) #goes through each lottery and computes the expected utility with expected_utility
        if eu_current > best_eu: #if the expected utility of this lottery is more than the best found so far
            best_eu = eu_current #updates the best expected utility found
            best_idx = lot_idx #if the current eu is more than the previous biggest, replace it
    lottery_index = best_idx
    eu = float(best_eu)
    return lottery_index, eu



# Step Six:  The Holt-Laury procedure



def build_holt_laury():
    """Returns list of Holt-Laury lottery pairs.
    
        returns:
            holt_laury_lotteries, list of lists
                inner list is a pair of lotteries for choice
        
    Each pair has two lotteries, A and B. Lottery A is the safer option,
    paying 6 with probability prob, else 4. Lottery B is the riskier option,
    paying 10 with probability prob, else 1. The probability prob varies from
    0.1 to 1.0 in increments of 0.1 across the 10 pairs.
    
    """
    high_A, low_A = 6.0, 4.0 #these are the payoffs, safer option A pays 6 with the probability p, else 4
    high_B, low_B = 10.0, 1.0 #same concept as above but riskier
    
    pairs = [] #starts an empty list to hold all the lottery pairs
    for prob_increment in range(1,11): #loops through 1 to 10 to create probabilities from 0.1 to 1.0
        prob = prob_increment / 10.0 #this is looping through 1-10 to make the probabilities 0.1,0.2...1.0

        option_A = [
            {'prob': prob, 'out': high_A}, #lottery A paying 6 with probability prob
            {'prob': 1-prob, 'out': low_A}, #lottery A paying 4 with probability 1-prob
        ]

        option_B = [
            {'prob': prob, 'out': high_B}, #lottery B paying 10 with probability prob
            {'prob': 1-prob, 'out': low_B}, #lottery B paying 1 with probability 1-prob
        ]

        pairs.append([option_A, option_B]) #adds the pair of lotteries to the list of pairs
    return pairs


def holt_laury_choices(lottery_list, u = None):
    """Returns list of lottery choices from lottery_list
    
        If u == None, human makes choices, otherwise
            lottery choice(inner_list, u) makes choices.
    
        args:
            lottery_list = [[lottery, ..., lottery], ..., 
                            [lottery, ..., lottery]]
            u, utility function over payoffs, or None
        returns:
            lottery_list_choices
                list of integers, 0 or 1, for each pair in lottery_list
            
    """
    choices = [] #starts an empty list to hold the choices made
    for row_idx, pair in enumerate(lottery_list): #Go through each holt laury pair 
        if u is None: #if no utility function is provided, ask the user to make the choice
            while True: #keeps asking until valid input
                resp = input(f"Row {row_idx}: choose 0 (left) or 1 (right): ").strip() #asks user to choose which lottery it wants and removes whitespace
                if resp in ("0", "1"): #checks if input is valid
                    choices.append(int(resp)) #asks user to choose which lottery it wants and appends their choice to the list choices 
                    break
                else: 
                    print("Please enter 0 or 1.") #prompts user to re-enter if input invalid
        else:
            idx, _eu = lottery_choice(pair, u) #uses previous function to choose the higher eu lottery in the row. Used _eu to ignore the second return value since we don't need it here
            choices.append(idx) #append the chosen index to the choices list
    return choices
lottery_list = build_holt_laury() 
def linear_utility(m): 
    return m #simple linear utility function for testing
choices = holt_laury_choices(lottery_list, u=linear_utility) 
print(choices)



# Step Seven:  Stepwise elicitation algorithm



import math
from typing import Callable, List, Tuple, Optional #Type hints to improve code readability

def stepwise_elicitation(min_pay: float, max_pay: float, num_questions: int = 10, get_ce: Optional[Callable[[float, float], float]] = None):  #Optional... means either none or a function that takes two floats and returns a float. 
    """
    Run the stepwise elicitation procedure.

    Args: 
        min_pay (float): Minimum payoff value (x_min). 
        max_pay (float): Maximum payoff value. (x_max).
        num_questions (int): how many CE questions to ask. 
        get_ce: Function to get certainty equivalent for a given low and high payoff (x, y).
                If None, prompts user for input.
    
    Returns:
        points: a sorted list of (x, U(x)) including min and max and all elicited points.
        U(min_pay) = 0.0, U(max_pay) = 100.0
        U(ce) = 0.5*U(x) + 0.5*U(y)

    """

    points = [(min_pay, 0.0), (max_pay, 100.0)] #starts with the min and max payoffs and their utilities 

    segments = [(min_pay, max_pay)] #starts with one segment from min to max payoff

    def ask_ce(low_payoff: float, high_payoff: float):
        """ Ask for certainty equivalent between low_payoff and high_payoff.
        
            If get_ce function is provided, use it to get the CE.
            Otherwise, prompt user for input.
        """
        if get_ce is not None: #if a function is provided to get certainty equivalent
            return float(get_ce(low_payoff, high_payoff)) #calls the provided function to get the certainty equivalent
        while True:
            try:
                resp = float(input(f"Certainty equivalent for lottery [{low_payoff}, 0.5; {high_payoff}, 0.5]? Enter a number between {low_payoff} and {high_payoff}: ")) #asks user for certainty equivalent between low and high payoff
                if low_payoff <= resp <= high_payoff: #if low payoff is less than or equal to response and response is less than or equal to high payoff
                    return resp #returns the response
            except ValueError: 
                pass #if input is invalid, just passes to the next line
            print(f"Please enter a number between {low_payoff} and {high_payoff}.") #prompts user to re-enter if input invalid

    def utility_at_exact(payoff_value: float):
        """
        Return U(payoff_value) for an already-known payoff in 'points'.
        Raises ValueError if payoff_val not in points.
        """
        for payoff, utility_value in points: #loops through each (payoff, utility) tuple in points
            if payoff == payoff_value: #if the payoff matches the requested payoff value
                return utility_value #returns the corresponding utility value
        raise ValueError(f"utility_at_exact requested for a point not yet in 'points'.") #raises error if payoff value not found in points
    
    def widest_segment() -> Tuple[float, float]:
        """
        Remove and return the segment with the largest (left, right) width from 'segments'.

        """
        segments.sort(key=lambda seg: seg[1] - seg[0], reverse=True) #sorts the segments by width in descending order.Lambda means an anonymous function that takes a tuple seg and returns the width seg[1] - seg[0]
        return segments.pop(0) #removes and returns the widest segment
    
    for _ in range(num_questions):

        left_payoff, right_payoff = widest_segment() #gets the widest segment to ask about

        ce_payoff = ask_ce(left_payoff, right_payoff) #asks for the certainty equivalent between the left and right payoffs

        ce_utility = 0.5 * utility_at_exact(left_payoff) + 0.5 * utility_at_exact(right_payoff) #calculates the utility at the certainty equivalent using the utilities of the left and right payoffs

        points.append((ce_payoff, ce_utility)) #adds the new (payoff, utility) point to the list of points
        points.sort(key=lambda p: p[0]) #sorts the points by payoff value. Lambda means an anonymous function that takes a tuple p and returns the first element p[0]

        if ce_payoff - left_payoff > 1e-9: #if the new certainty equivalent is significantly greater than the left payoff
            segments.append((left_payoff, ce_payoff)) #adds a new segment from left payoff to certainty equivalent
        if right_payoff - ce_payoff > 1e-9: #if the new certainty equivalent is significantly less than the right payoff
            segments.append((ce_payoff, right_payoff)) #adds a new segment from certainty equivalent to right payoff
    return points


def build_piecewise_utility(points: List[Tuple[float, float]]):
    """ 
    Given a sorted list of (payoff, utility_value) points, return a function U_hat(payoff) that linearly interpolates between the points and clamps outside the range.
    """

    sorted_points = sorted(points, key=lambda p: p[0]) #sorts the points by payoff value. Lambda means an anonymous function that takes a tuple p and returns the first element p[0]

    def U_hat(payoff: float):

        if payoff <= sorted_points[0][0]: #if the payoff is less than or equal to the minimum payoff in the points
            return sorted_points[0][1] #returns the utility value at the minimum payoff
        if payoff >= sorted_points[-1][0]: #if the payoff is greater than or equal to the maximum payoff in the points
            return sorted_points[-1][1] #returns the utility value at the maximum payoff

        for (x_left, u_left), (x_right, u_right) in zip(sorted_points, sorted_points[1:]): #loops through each pair of consectutive points. Zip pairs each point with the next point in the list
            if abs(x_right - x_left) < 1e-12: #if the two payoffs are effectively the same within tolerance
                return u_left #returns the utility value at the left payoff
            weight = (payoff-x_left) / (x_right - x_left) #calculates the weight for linear interpolation between the two points
            return u_left + weight * (u_right - u_left) #returns the interpolated utility value between the two points
        return sorted_points[-1][1] #fallback return the maximum utility value
    return U_hat

#Test code for stepwise elicitation and piecewise utility
if __name__ == "__main__": #only runs when this file is executed directly, not when imported as a module
    points = stepwise_elicitation(min_pay=0.0, max_pay=100.0, num_questions=10, get_ce=None) #runs stepwise elicitation with user input for 10 questions between payoffs 0 and 100
    print("\nElicited (payoff, U):") #prints header for the elicited points
    for payoff, utility in points: #loops through each (payoff, utility) tuple in points
        print(f"({payoff:.6g}, {utility:.6g})") #prints each elicited point with 6 significant digits

    U_hat = build_piecewise_utility(points)
    
    # Example call to show it works:
    print("\nExample: U_hat(50) =", U_hat(50.0))
    print("U_hat(35) =", U_hat(35.0)) #prints the utility at payoff 35 using the piecewise utility function