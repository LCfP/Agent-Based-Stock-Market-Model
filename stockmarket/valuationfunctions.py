"""In this file, we define the stock valuation functions of the agents"""

import numpy as np
from stockmarket.functions import npv_growing_perpetuity
from stockmarket.functions import moving_average


def extrapolate_average_profit(stock, memory, **_):
    # TODO
    """

    Parameters
    ----------
    stock
    memory
    _

    Returns
    -------

    """
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


def extrapolate_ma_price(stock, s, l, **_):
    # TODO
    """

    Parameters
    ----------
    stock
    s
    l
    _

    Returns
    -------

    """
    price_history = stock.price_history
    if len(price_history) >= l:
        short_ma = sum(price_history[-s:]) / s
        long_ma = sum(price_history[-l:]) / l
        return short_ma+((short_ma-long_ma)/(l-s))
    else:
        return None


def predict_by_moving_avg_growth(stock, s, **_):
    """Returns predicted value of a stock

    Predicts the next price of a stock by extrapolating the moving average and its growth.

    Parameters
    ----------
    stock : :obj:`stock`
        Stock to be predicted.
    s : int
         Number of data points used to calculate a moving average.

    Returns
    -------
    int
        Predicted next price of the stock


    Notes
    _____
    The moving average lags behind by n/2 + 0.5 periods when not centered around the mean.

    """
    stockPriceHistory = len(stock.price_history)
    if stockPriceHistory < s+1:
        return None
    else:
        ma = sum(stock.price_history[-s:]) / s
        growth = ma - sum(stock.price_history[-s-1:-1]) / s
        predicted = ma + (s/2+0.5)*growth
        if predicted > 0:
            return predicted
        else:
            return 0


