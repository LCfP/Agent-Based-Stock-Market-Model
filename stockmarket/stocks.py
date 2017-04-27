"""In this file, we define the benchmark stock market model stock classes"""

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


class Stock:
    """a base class for Stocks"""
    def __init__(self, firm, face_value):
        """Creates a new stock"""
        self.name = firm.name
        self.firm = firm
        self.face_value = face_value
        self.amount = firm.book_value / face_value

    def __str__(self):
        return "Stock of " + str(self.firm)

    def __repr__(self):
        return "stock_" + repr(self.name)
