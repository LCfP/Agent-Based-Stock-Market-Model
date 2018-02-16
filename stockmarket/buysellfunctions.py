"""In this file, we define buy / sell / hold functions of the agents"""

import numpy as np


def mean_reversion(prices, shortMA, longMA, upper_threshold, lower_threshold):
    """
    Buy or sell against the trend
    :param prices: list of prices
    :param shortMA: integer short moving average
    :param longMA: integer long moving average
    :param upper_threshold:
    :param lower_threshold:
    :return: string buy, sell or hold
    """
    shortMA = int(shortMA)
    longMA = int(longMA)
    short_ma = sum(prices[len(prices) - shortMA:]) / shortMA
    long_ma = sum(prices[len(prices) - longMA:]) / longMA
    momentum = short_ma / long_ma
    if momentum > upper_threshold:
        return 'sell'
    elif momentum < lower_threshold:
        return 'buy'
    else:
        return 'hold'


def momentum(prices, shortMA, longMA, upper_threshold, lower_threshold):
    """
    If momentum is positive, buy, if momentum is negative, sell, otherwise hold
    :param prices: list of prices
    :param shortMA: integer short moving average
    :param longMA: integer long moving average
    :param upper_threshold:
    :param lower_threshold:
    :return: string buy, sell or hold
    """
    short_ma = sum(prices[len(prices)-shortMA:]) / shortMA
    long_ma = sum(prices[len(prices)-longMA:]) / longMA
    momentum = short_ma / long_ma
    if momentum > upper_threshold:
        return 'buy'
    elif momentum < lower_threshold:
        return 'sell'
    else:
        return 'hold'

def noise_trading(prices, shortMA, longMA, upper_threshold, lower_threshold):
    """
    buy / sell at random
    :param prices: list of prices
    :param shortMA: integer short moving average
    :param longMA: integer long moving average
    :param upper_threshold:
    :param lower_threshold:
    :return: string buy, sell or hold
    """
    probability_to_buy = np.random.randint(0, 100)
    probability_to_buy = probability_to_buy / 100

    return np.random.choice(['buy', 'sell'], p=[probability_to_buy, (1-probability_to_buy)])
