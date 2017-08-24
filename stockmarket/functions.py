"""In this file, we define general functions for the benchmark stock market model"""

import numpy as np


def npv_growing_perpetuity(dividend, discount_rate=0.11, growth_rate=0):
    """Returns the present value of a growing perpetuity.

    Parameters
    ----------
    dividend : scalar
        Value of the first dividend.
    discount_rate : scalar
        Rate of interest as decimal per period.
    growth_rate : scalar
        Rate of growth of the dividend as decimal per period.

    Returns
    -------
    scalar
        Present value
    """
    if discount_rate <= growth_rate:
        raise ValueError('discount rate <= growth rate', 'dc = ' + str(discount_rate), 'gr = ' + str(growth_rate))
    return np.divide(dividend, (discount_rate - growth_rate))


def moving_average(x, n):
    """Returns the moving averages as a list.

    Calculates the simple moving averages using the last `n` data points for each entry.

    Parameters
    ----------
    x : array_like
        Input array.
    n : int
        Number of data points used to calculate a moving average.

    Returns
    -------
    array
        Returns a new array holding the moving averages.
    """
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[n:] - cumsum[:-n]) / n


def div0(a, b):
    """
    ignore / 0, div0( [-1, 0, 1], 0 ) -> [0, 0, 0]
    credits to Dennis @ https://stackoverflow.com/questions/26248654/numpy-return-0-with-divide-by-zero
    """
    #with np.errstate(divide='ignore', invalid='ignore'):
    answer = np.true_divide(a, b)
    if not np.isfinite(answer):
        answer = 0
    #c[~ np.isfinite(c)] = 0  # -inf inf NaN
    return answer


def print_setup(agents, firms, stocks):
    for agent in agents:
        print(repr(agent) + " has $ " + str(agent.money) + "and stocks:", agent.stocks, "and memory of ",
              agent.memory_size, " finally the bid-ask spread size is ", agent.bid_ask_spread)
    for firm in firms:
        print(repr(firm) + " has a book value of " + str(firm.book_value) + " profit of ", firm.profit,
              "profit history of ", firm.profit_history, " and a divididend ratio of ", firm.dividend_rate)
    for stock in stocks:
        print(repr(stock) + ", amount " + str(stock.amount) + " links to Firm ", stock.firm)


def print_quarterly_data(agents, firms):
    print("Info on firms.")
    for firm in firms:
        firm.show()

    print("Info on agents.")
    for agent in agents:
        agent.show()