"""In this file, we define the benchmark stock market model stock classes"""
__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

class Stock():
	"""a base class for Stocks"""
	def __init__(self, id ,firm, faceValue):
        """Creates a new trader"""
		self.id = id
		self.firm = firm
		self.faceValue = faceValue