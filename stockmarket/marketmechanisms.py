"""In this file, we define market matching mechanism functions. These functions take in agent sets and output matched pairs of agents"""

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

import math
import random

from stockmarket.functions import transaction


def market_mechanism(agentset, observablesetsize, stock, set_of_traders_function,
                     record=False, recordInfo={}):
    """return set of matched agents"""
    # copy the agentset and shuffle the set to get different order of traders every time
    randomized_agent_set = list(agentset)
    random.shuffle(randomized_agent_set)

    # every demand agent observes a subset of other agents from which it picks the cheapest supplier
    for demander in randomized_agent_set:
        # find the observable set for the demanding agent
        observable_set = set_of_traders_function(demander, randomized_agent_set, observablesetsize)

        # Find cheapest supplier and save the price
        best_supplier_and_price = (None, math.inf)

        for supplier in observable_set:
            supplier_price = supplier.valuate_stocks(stock=stock) \
                             * (1 + (supplier.bid_ask_spread / 200))

            if suitable_trade(demander, supplier, best_supplier_and_price, stock):
                best_supplier_and_price = (supplier, supplier_price)

        # If we found a trade, make the actual trade.
        if best_supplier_and_price[0] is not None:
            price = best_supplier_and_price[0].valuate_stocks(stock=stock) \
                    * (1 + (best_supplier_and_price[0].bid_ask_spread / 200))
            amount_demander_can_buy = math.floor(demander.money / price)
            amount_supplier_can_sell = supplier.stocks[stock]

            if amount_demander_can_buy < amount_supplier_can_sell:
                amount = amount_demander_can_buy
            else:
                amount = amount_supplier_can_sell

            if amount > 0:
                transaction(demander, supplier, stock, amount, amount * price, record=record, recordInfo=recordInfo)

    return randomized_agent_set

def suitable_trade(demander, supplier, best_supplier_and_price, stock):
    """
    Evaluates if a trade can take place

    If the price the demanding trader is willing to pay is bigger than the supplier price,
    the supplier price is cheaper than the current cheapest price, and the supplier has stocks to sell:
    return True. Otherwise, returns False.
    """
    demander_price = demander.valuate_stocks(stock=stock) \
                     * (1 - (demander.bid_ask_spread / 200))  # /2 and / 100 for percent
    supplier_price = supplier.valuate_stocks(stock=stock) \
                     * (1 + (supplier.bid_ask_spread / 200))

    priceIsRight = (demander_price > supplier_price)
    priceIsBest = (supplier_price < best_supplier_and_price[1])
    thereAreStocks = (supplier.stocks[stock] > 0)

    if priceIsRight and priceIsBest and thereAreStocks:
        return True
    else:
        return False

