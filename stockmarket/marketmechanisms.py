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

    total_volumn = 0
    total_money = 0

    for demander in randomized_agent_set:

        observable_set = set_of_traders_function(demander, randomized_agent_set, observablesetsize)
        
        sup = best_supplier(observable_set, stock)
        if sup is not None:
            vol = find_volume(demander, sup, stock)
            if vol > 0:
                price = selling_price(stock, sup)
                transaction(demander, sup, stock, vol, vol * price, record, recordInfo)
                total_volumn += vol
                total_money += vol * price

    stock.add_price(total_volumn, total_money)


def find_volume(demander, supplier, stock):
    sp = selling_price(stock, supplier)
    bp = buying_price(stock, demander)
    if bp is not None and sp is not None and sp <= bp:
        return min(supplier.stocks[stock], math.floor(demander.money / sp))
    else:
        return 0


def best_supplier(suppliers, stock):
    current_supplier = None
    current_price = None
    for supplier in suppliers:
        price = selling_price(stock, supplier)
        if price is not None and supplier.stocks[stock] > 0:
            if current_price is None or current_price > price:
                current_supplier = supplier
                current_price = price
    return current_supplier


def buying_price(stock, demander):
    price = demander.valuate_stocks(stock)
    if price is not None:
        return demander.valuate_stocks(stock) * (1 - (demander.bid_ask_spread / 200))
    else:
        return None


def selling_price(stock, supplier):
    price = supplier.valuate_stocks(stock)
    if price is not None:
        # TODO: Edge case: valuated at zero
        return supplier.valuate_stocks(stock) * (1 + (supplier.bid_ask_spread / 200))
    else:
        return None
