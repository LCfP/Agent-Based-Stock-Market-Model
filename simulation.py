"""This file is our main simulation file it includes the set-up and time loop"""

import random
random.seed(1)
from stockmarket import functions, setup, marketmechanisms, randomset

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

"""
Define initial variables and parameters
"""
AMOUNT_OF_AGENTS = 6
AMOUNT_OF_FIRMS = 2
OBSERVABLE_SET_SIZE = 3

SEED = 1

INIT_MONEY = (100, 200)
INIT_BID_ASK = (5, 5)
INIT_MEMORY_SIZE = (1, 4)

INIT_PROFIT = (200, 200)
INIT_BOOK_VALUE = (10000, 10000)
INIT_PROFIT_HISTORY = [150, 170, 190]

INIT_FACE_VALUE = 50

parameter_space = {"simulationTime": 100}

"""
Setup 
"""
agents = setup.setup_agents(init_money=INIT_MONEY, init_bid_ask_spread=INIT_BID_ASK, init_memory_size=INIT_MEMORY_SIZE,
                            seed=SEED, amount_of_agents=AMOUNT_OF_AGENTS)
firms = setup.setup_firms(init_book_value=INIT_BOOK_VALUE, init_profit=INIT_PROFIT, init_profit_history=INIT_PROFIT_HISTORY,
                          seed=SEED, amount_of_firms=AMOUNT_OF_FIRMS)
stocks = setup.setup_stocks(firms, face_value=INIT_FACE_VALUE)

# distribute the initial stocks to the agents equally 1 per 1 until non left. (slow)
stocks, agents = functions.distribute_initial_stocks(stocks, agents)

"""
Print set-up
"""
functions.print_setup(agents, firms, stocks)

"""
Simulation

Process overview and scheduling from the ODD
1. Update profits
2. Update expected price and spread
3. Market mechanism
4. Store market prices t-1 
"""

for quarter in range(parameter_space["simulationTime"]):

    # functions.print_quarterly_data(agents, firms)

    #1 update dividends
    for firm in firms:
        firm.update_profits(lowestpercentage=95, variance=10)

    #2 market mechanism
    for stock in stocks:
        marketmechanisms.market_mechanism(agents, OBSERVABLE_SET_SIZE, stock, functions.valuation_extrapolate_average, randomset.subset_traders,
                         SEED)

