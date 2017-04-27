"""In this file, we define the set-up procedure of the model"""

import random
import itertools
from stockmarket import agents, firms, stocks, valuationfunctions

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


def setup_agents(init_money, init_bid_ask_spread, init_memory_size, seed, amount_of_agents=3):
    """This returns an initialized agent set"""
    agent_set = []
    for agent in range(amount_of_agents):
        memory = randomize_init_variable(init_memory_size[0], init_memory_size[1])
        agent_set.append(agents.Trader(name=agent,
                                       money=randomize_init_variable(init_money[0], init_money[1]),
                                       bid_ask_spread=randomize_init_variable(init_bid_ask_spread[0], init_bid_ask_spread[1]),
                                       memory_size=memory,
                                       function=lambda x: valuationfunctions.valuation_extrapolate_average(x, memory)))
    return agent_set


def setup_firms(init_book_value, init_profit, seed, amount_of_firms=1):
    """This returns an initialized firm set"""
    firm_set = []
    for firm in range(amount_of_firms):
        firm_set.append(firms.Firm(name=firm,
                                   book_value=randomize_init_variable(init_book_value[0], init_book_value[1]),
                                   profits=[randomize_init_variable(init_profit[0], init_profit[1])],
                                   # this makes sure that individual firms have a different seed every simulation
                                   seed=random.randint(0, 10000),
                                   dividend_rate=1))
    for firm in firm_set:
        # creates a profit history for the last 3 periods.
        for _ in itertools.repeat(None, 3):
            firm.update_profits(firm.determine_growth())

    return firm_set


def setup_stocks(set_of_firms, amount):
    stock_set = []
    for firm in set_of_firms:
        stock_set.append(stocks.Stock(firm, amount))
    return stock_set


def randomize_init_variable(min_amount, max_amount):
    return random.randint(min_amount, max_amount)

