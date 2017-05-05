"""In this file, we define the stock valuation functions of the agents"""

import numpy as np
from stockmarket.functions import npv_growing_perpetuity

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


def extrapolate_average_profit(stock, memory, **_):
    prof_history = stock.firm.profit_history[-memory:]
    expected_profit = np.mean(prof_history)
    value = npv_growing_perpetuity(expected_profit * stock.firm.dividend_rate)
    return np.divide(value, stock.amount)


def extrapolate_growth_average_profit(stock, memory, **_):
    pass
    # profit_growth_history = stock.firm.profit_growth_history
    # expected_growth = np.mean(profit_growth_history[len(profit_growth_history)-memory:len(profit_growth_history)])
    # value = calculate_npv(stock.firm.profit * stock.firm.dividend_rate, growth_rate=expected_growth)
    #  return np.divide(value, stock.amount)


def extrapolate_moving_average_price(stock, memory, **_):
    price_history = stock.price_history[-memory:]
    if price_history:
        return np.mean(price_history)
    else:
        return None

