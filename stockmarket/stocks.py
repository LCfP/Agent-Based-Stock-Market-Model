"""In this file, we define the benchmark stock market model stock classes"""

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


class Stock:
    """a base class for Stocks"""
    def __init__(self, name, firm, face_value, amount):
        """Creates a new stock"""
        self.name = name
        self.firm = firm
        self.face_value = face_value
        self.amount = amount

    def __str__(self):
        return "Stock of " + str(self.firm)

    def __repr__(self):
        return "stock_" + repr(self.firm)
