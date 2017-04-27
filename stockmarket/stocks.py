"""In this file, we define the benchmark stock market model stock classes"""

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


class Stock:
    """a base class for Stocks"""
    def __init__(self, firm, amount):
        """Creates a new stock"""
        self.name = firm.name
        self.firm = firm
        self.face_value = firm.book_value / amount
        self.amount = amount
        self.price_history = []

    def __str__(self):
        return "Stock of " + str(self.firm)

    def __repr__(self):
        return "stock_" + repr(self.name)
