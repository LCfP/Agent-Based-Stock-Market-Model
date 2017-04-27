"""In this file, we define the stock valuation functions of the agents"""

import numpy as np
from stockmarket.functions import npv_growing_perpetuity

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


def valuation_extrapolate_average(stock, memory, **_):
    prof_history = stock.firm.profit_history
    if memory < len(prof_history):
        expected_profit = np.mean(prof_history[-memory:])
    else:
        expected_profit = np.mean(prof_history)
    value = npv_growing_perpetuity(expected_profit * stock.firm.dividend_rate)
    return np.divide(value, stock.amount)


def valuation_extrapolate_growth_average(stock, memory, **_):
    pass
    # profit_growth_history = stock.firm.profit_growth_history
    # expected_growth = np.mean(profit_growth_history[len(profit_growth_history)-memory:len(profit_growth_history)])
    # value = calculate_npv(stock.firm.profit * stock.firm.dividend_rate, growth_rate=expected_growth)
    #  return np.divide(value, stock.amount)


def price_trend(stock, ma_short, ma_long, min_profit, max_loss, **_):
    val_mashort = np.mean(stock.price_history[-ma_short:])
    val_malong = np.mean(stock.price_history[-ma_long:])
    # if MAshort is greater than MAlong the chartists thinks the price will increase.
    if val_mashort > val_malong:
        return stock.price_history[-1] * min_profit
    # if MAshort is smaller than MAlong the chartists thinks the price will decrease.
    elif val_mashort < val_malong:
        return stock.price_history[-1] * max_loss
    else:
        return stock.price_history[-1]

