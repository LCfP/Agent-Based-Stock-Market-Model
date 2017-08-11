"""In this file, we define the benchmark stock market model firm classes"""

import random
import math
from scipy.stats import norm
import numpy.random as nrand

class Firm:
    """a base class for Firms"""

    def __init__(self, name, book_value, profits, drift_alpha, drift_mu, brownian_delta, brownian_sigma, dividend_rate=1):
        """Creates a new trader"""
        self.name = name
        self.book_value = book_value
        self.profit = profits[-1]
        self.dividend_rate = dividend_rate
        self.profit_history = profits
        self.drift_alpha = drift_alpha
        self.drift_mu = drift_mu
        self.brownian_delta = brownian_delta
        self.brownian_sigma = brownian_sigma
        self.accounting_rate_of_return = profits[-1] / float(book_value)

    def determine_growth(self):
        """
        Accounting rate of return growth process inspired by:
        Feenstra, D., Huijgen, C. and Wang, H., 2000. An evaluation of the accounting rate of return.

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
        # random component through brownian motion
        sqrt_delta_sigma = math.sqrt(self.brownian_delta) * self.brownian_sigma
        brownian_motion = nrand.normal(loc=0, scale=sqrt_delta_sigma)
        randomness = math.sqrt(self.accounting_rate_of_return) * brownian_motion
        # drift component
        drift = self.drift_alpha * (self.drift_mu * self.accounting_rate_of_return) * self.brownian_delta
        return self.accounting_rate_of_return + drift + randomness

    def update_profits(self, new_arr):
        """Update the firms profit

        Calculates the next profit given the `growth`, updates the profit and stores the last profit
        in the `profit_history`.

        Parameters
        ----------
        new_arr : scalar
            Growth rate of the profit as a decimal.

        """
        self.accounting_rate_of_return = new_arr
        self.profit = int(self.accounting_rate_of_return * self.book_value) #int(self.profit * growth)
        self.profit_history.append(self.profit)

    def __repr__(self):
        return 'firm_' + str(self.name)

    def __str__(self):
        return str(self.name)

    def show(self):
        print("Name:", self.name)
        print("Profit history:", self.profit_history)
        print("")


