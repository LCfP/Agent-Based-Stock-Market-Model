"""In this file, we define the stock valuation functions of the agents"""

import numpy as np
from stockmarket.functions import calculate_npv

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


def valuation_extrapolate_average(stock, memory, **_):
    prof_history = stock.firm.profit_history
    expected_profit = np.mean(prof_history[len(prof_history)-memory:len(prof_history)])
    value = calculate_npv(expected_profit * stock.firm.dividend_rate)
    return np.divide(value, stock.amount)


def valuation_extrapolate_growth_average(stock, memory, **_):
    profit_growth_history = stock.firm.profit_growth_history
    expected_growth = np.mean(profit_growth_history[len(profit_growth_history)-memory:len(profit_growth_history)])
    value = calculate_npv(stock.firm.profit * stock.firm.dividend_rate, growth_rate=expected_growth)
    return np.divide(value, stock.amount)


def price_trend(stock, memory, **_):
    pass
