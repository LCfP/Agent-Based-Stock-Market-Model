"""In this file, we define the benchmark stock market model stock classes"""

import numpy as np
from stockmarket.functions import npv_growing_perpetuity

class Stock:
    """a base class for Stocks"""
    def __init__(self, firm, amount):
        """Creates a new stock"""
        self.name = firm.name
        self.firm = firm
        self.face_value = firm.book_value / amount
        self.amount = amount
        priceHistoryOnValue = np.array([npv_growing_perpetuity(prof_his * firm.dividend_rate) for prof_his in firm.profit_history])
        priceHistPerStock = np.divide(priceHistoryOnValue, amount)
        self.price_history = list(priceHistPerStock)
        self.price_to_earnings_history = []

    def add_price(self, vol, price):
        """Adds the average stock price of the period to the price history of the stock

        Calculates the average price of all trades of `self` in the period, weighted by amount, and adds it
        to the `price_history` of the stock.

        Parameters
        ----------
        vol : int
            Total amount of stocks traded in the period.
        price : scalar
            Total price for all stocks in the period.

        """
        if vol > 0:
            self.price_history.append(price / vol)
        elif self.price_history:
            self.price_history.append(self.price_history[-1])

    def __str__(self):
        return "Stock of " + str(self.firm)

    def __repr__(self):
        return "stock_" + repr(self.name)
