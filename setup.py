"""In this file, we define the set-up procedure of the model"""

import agents
import random
import firms
import functions

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


def setup_agents(init_money, init_bid_ask_spread, init_memory_size, seed, amount_of_agents=3):
    """This returns an initialized agent set"""
    random.seed(seed)
    agent_set = []
    for agent in range(amount_of_agents):
        agent_set.append(agents.Trader(name=agent,
                                       money=randomize_init_variable(init_money[0], init_money[1]),
                                       bid_ask_spread=randomize_init_variable(init_bid_ask_spread[0], init_bid_ask_spread[1]),
                                       memory_size=randomize_init_variable(init_memory_size[0], init_memory_size[1])))
    return agent_set


def setup_firms(init_book_value, init_profit, init_profit_history, seed, amount_of_firms=1):
    """This returns an initialized firm set"""
    random.seed(seed)
    firm_set = []
    for firm in range(amount_of_firms):
        firm_set.append(firms.Firm(name=firm,
                                   book_value=randomize_init_variable(init_book_value[0], init_book_value[1]),
                                   profit=randomize_init_variable(init_profit[0], init_profit[1]),
                                   profit_history=init_profit_history,
                                   # this makes sure that individual firms have a different seed every simulation
                                   seed=random.randint(0, 10000),
                                   dividend_rate=1))
    return firm_set


def setup_stocks(set_of_firms, face_value):
    stock_set = []
    for firm in set_of_firms:
        stock_set.append(functions.create_stocks(firm, face_value))
    return stock_set


def randomize_init_variable(min_amount, max_amount):
    return random.randint(min_amount, max_amount)

