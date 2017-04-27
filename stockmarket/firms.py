"""In this file, we define the benchmark stock market model firm classes"""

import random

class Firm:
    """a base class for Firms"""

    def __init__(self, name, book_value, profits, seed, dividend_rate=1):
        """Creates a new trader"""
        self.name = name
        self.book_value = book_value
        self.profit = profits[-1]
        self.dividend_rate = dividend_rate
        self.profit_history = profits

    def determine_growth(self, sd=5):
        return (random.randint(100-sd, 100+sd)) / 100

    def update_profits(self, growth):
        self.profit = int(self.profit * growth)
        self.profit_history.append(self.profit)

    def __repr__(self):
        return 'firm_' + str(self.name)

    def __str__(self):
        return str(self.name)

    def show(self):
        print("Name:", self.name)
        print("Profit history:", self.profit_history)
        print("")


