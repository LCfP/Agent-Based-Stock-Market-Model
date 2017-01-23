"""In this file, we define the benchmark stock market model firm classes"""

import random

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


class Firm:
    """a base class for Firms"""

    def __init__(self, name, book_value, profit, profit_history, seed, dividend_rate=1):
        """Creates a new trader"""
        self.name = name
        self.book_value = book_value
        self.profit = profit
        self.dividend_rate = dividend_rate
        self.profit_history = profit_history
        self.profit_history.append(profit)
        self.profit_growth_history = [(j / float(i)) - 1 for i, j in zip(self.profit_history[:-1],
                                                                         self.profit_history[1:])]
        random.seed(seed)

    def update_profits(self):
        # TODO update
        growth = 95 + random.randint(0, 10)
        self.profit = int((self.profit * growth) / 100)
        self.profit_growth_history.append((growth - 100) / 100)
        self.profit_history.append(self.profit)

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)


def test_method():
    test_firm = Firm(12, 1000, 10000, [10000, 10000], seed=1)
    print(test_firm.profit_history)
    print(test_firm.profit_growth_history)
    print(test_firm.profit)
    test_firm.update_profits()
    print(test_firm.profit)
    print(test_firm.profit_history)
    print(test_firm.profit_growth_history)
    print(test_firm)
