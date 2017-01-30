"""In this file, we define market matching mechanism functions. These functions take in agent sets and output matched pairs of agents"""

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

import random
import math


def market_mechanism(agentset, observablesetsize, stock, valuation_function, set_of_traders_function, seed):
    """return set of matched agents"""
    set_of_matched_agents = []
    random.seed(seed)

    # copy the agentset and shuffle the set to get different order of traders every time
    randomized_agent_set = list(agentset)
    random.shuffle(randomized_agent_set)

    # every demand agent observes a subset of other agents from which it picks the cheapest supplier
    for demander in randomized_agent_set:

        # find the observable set for the demanding agent
        observable_set = set_of_traders_function(demander, randomized_agent_set, observablesetsize)

        # Find cheapest supplier and safe the price
        best_supplier_and_price = (None, math.inf)

        for supplier in observable_set:
            supplier_price = supplier.valuate_stocks(stock=stock, valuation_function=valuation_function) \
                             * (1 + (supplier.bid_ask_spread / 200))

            if suitable_trade(demander, supplier, best_supplier_and_price, stock, valuation_function):
                best_supplier_and_price = (supplier, supplier_price)

        # If the minimum price of all suppliers is lower than the ask price, make deal with demander
        set_of_matched_agents.append((demander, best_supplier_and_price[0]))

    return set_of_matched_agents
    # observe random set and take highest


def suitable_trade(demander, supplier, best_supplier_and_price, stock, valuation_function):
    demander_price = demander.valuate_stocks(stock=stock, valuation_function=valuation_function) \
                     * (1 - (demander.bid_ask_spread / 200))  # /2 and / 100 for percent
    supplier_price = supplier.valuate_stocks(stock=stock, valuation_function=valuation_function) \
                     * (1 + (supplier.bid_ask_spread / 200))

    # If the demander price is lower than what the supplier wants for the stock, no trade is possible
    if demander_price < supplier_price:
        return False

    # A trade is only possible if the supplier price is the lowest, and there's stock available.
    if supplier_price < best_supplier_and_price[1] and supplier.stocks["1"] > 0:
        return True
