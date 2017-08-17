"""In this file, we define the benchmark stock market model firm classes"""

import math
import numpy as np
import numpy.random as nrand

class Firm:
    """a base class for Firms"""

    def __init__(self, name, book_value, profits,
                 mu=0.058, brownian_delta=0.00396825396, brownian_sigma=0.125, dividend_rate=1):
        """Creates a new trader"""
        self.name = name
        self.book_value = book_value
        self.profit = profits[-1]
        self.dividend_rate = dividend_rate
        self.profit_history = profits
        self.drift_mu = mu
        self.brownian_delta = brownian_delta
        self.brownian_sigma = brownian_sigma
        self.accounting_rate_of_return = profits[-1] / float(book_value)

    def determine_profit(self):
        """
        Geometric Brownian motion to determine the next profit.

        Parameters
        ----------
        trend : float
            Trend rate of growth
        mean_reversion: float
            Mean reversion parameter
        error_delta: float
            delta brownian motion error process
        error_dt: float
            dt for brownian motion error process

        Returns
        -------
        Float :
            Growth rate of the accounting rate of return of the firm

        """
        sqrt_delta_sigma = math.sqrt(self.brownian_delta) * self.brownian_sigma
        brownian_motion = nrand.normal(loc=0, scale=sqrt_delta_sigma)
        sigma_pow_mu_delta = (self.drift_mu - 0.5 * math.pow(self.brownian_sigma, 2.0)) * self.brownian_delta
        geometric_brownian_motion_log_return = brownian_motion + sigma_pow_mu_delta
        retur = np.exp(geometric_brownian_motion_log_return)
        next_profit = self.profit_history[-1] * retur
        return next_profit

    def update_profits(self, next_profit):
        """Update the firms profit

        Calculates the next profit given the `growth`, updates the profit and stores the last profit
        in the `profit_history`.

        Parameters
        ----------
        new_arr : scalar
            Growth rate of the profit as a decimal.

        """
        self.profit = next_profit
        self.profit_history.append(next_profit)

    def __repr__(self):
        return 'firm_' + str(self.name)

    def __str__(self):
        return str(self.name)

    def show(self):
        print("Name:", self.name)
        print("Profit history:", self.profit_history)
        print("")


