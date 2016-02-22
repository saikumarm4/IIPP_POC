"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import random

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(40)

import poc_clicker_provided as provided

# Constants
#SIM_TIME = 10000000000.0
SIM_TIME  = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        """
        This will instantiate the ClickerState object with default 
        State of the game
        """
        self._total_cookies = 0.0
        self._cookies_in_hand = 0.0
        self._game_time = 0.0
        self._current_cps = 1.0
        # history is a tuple of Time, An Item purchase or None, Cost, Total no of Cookies
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Total Cookies : %f\nCookies in Hand : %f\nGame Time : %f\nCurrent CPS : %f\n" %\
    (round(self._total_cookies, 1), round(self._cookies_in_hand, 1), self._game_time, self._current_cps)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cookies_in_hand
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._game_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history[:]

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._cookies_in_hand >= cookies:
            return 0.0 
        return math.ceil(abs(cookies - self._cookies_in_hand) / self._current_cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._game_time += time
            cookies = time * self._current_cps
            self._cookies_in_hand += cookies
            self._total_cookies += cookies
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._cookies_in_hand >= cost:
            self._cookies_in_hand -= cost
            self._current_cps += additional_cps
            self._history.append((self._game_time, item_name,\
                                cost, self._total_cookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    state = ClickerState()
    build_info_clone = build_info.clone()
    item_to_purchase = None
    while state.get_time() <= duration:
        item_to_purchase = strategy(state.get_cookies(), state.get_cps(),\
                                    state.get_history(), duration - state.get_time(),\
                                    build_info_clone)
        if item_to_purchase == None:
            break
        
        time_to_elapse = state.time_until(build_info_clone.get_cost(item_to_purchase))

        #print time_to_elapse, state.get_cps(), build_info_clone.get_cost(item_to_purchase),

        #print time_to_elapse
        if state.get_time() + time_to_elapse > duration:
            break
        state.wait(time_to_elapse)
        #print state.get_cookies(), state.get_time()
        while state.get_cookies() >= build_info_clone.get_cost(item_to_purchase):
            state.buy_item(item_to_purchase,\
                           build_info_clone.get_cost(item_to_purchase),\
                           build_info_clone.get_cps(item_to_purchase))
            build_info_clone.update_item(item_to_purchase)
    
    #print state, build_info_clone.get_cost(item_to_purchase)
    print
    #print duration - state.get_time()
    if state.get_time() < duration:
        state.wait(duration - state.get_time())
    return state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    cookies_generatable = cps * time_left + cookies
    cheap_cost = float('inf')
    item_to_purchase = []
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        if cost < cheap_cost and cost <= cookies_generatable:
            cheap_cost = cost
            item_to_purchase = [item, ]
        elif cost == cheap_cost:
            item_to_purchase.append(item)
    if item_to_purchase == []:
        return None
    return 	item_to_purchase[random.randrange(len(item_to_purchase))]

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    cookies_generatable = cps * time_left + cookies
    exp_cost = float('-inf')
    item_to_purchase = []
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        if cost > exp_cost and cost <= cookies_generatable:
            exp_cost = cost
            item_to_purchase = [item, ]
        elif cost == exp_cost:
            item_to_purchase.append(item)            
    if item_to_purchase == []:
        return None
    return 	item_to_purchase[random.randrange(len(item_to_purchase))]

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":\n", state
    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()