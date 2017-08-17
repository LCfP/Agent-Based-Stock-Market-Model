"""In this file, we define buy / sell / hold functions of the agents"""

import numpy as np


def mean_reversion(prices, shortMA, upper_threshold, lower_threshold):
    """Buy or sell against the trend"""
    prices = prices[(len(prices)-shortMA):]
    t = np.array(range(len(prices)))
    A = np.vstack([t, np.ones(len(t))]).T
    # estimate linear regression
    m, c = np.linalg.lstsq(A, prices)[0]
    trend = m*t + c
    if trend[-1] / prices[-1] > upper_threshold:
        return 'buy'
    elif trend[-1] / prices[-1] < lower_threshold:
        return 'sell'
    else:
        return 'hold'


def momentum(prices, shortMA, longMA, upper_threshold, lower_threshold):
    """If momentum is positive, buy, if momentum is negative, sell, otherwise hold"""
    short_ma = sum(prices[-shortMA:]) / shortMA
    long_ma = sum(prices[-longMA:]) / longMA
    momentum = short_ma / long_ma
    if momentum > upper_threshold:
        return 'buy'
    elif momentum < lower_threshold:
        return 'sell'
    else:
        return 'hold'