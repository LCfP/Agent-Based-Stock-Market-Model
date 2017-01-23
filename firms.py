"""In this file, we define the benchmark stock market model firm classes"""
__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

import random
import stocks

class Firm():
	"""a base class for Firms"""
	
	def __init__(self, id ,bookValue, profit, profitHistory, seed, dividendRate = 1):
		"""Creates a new trader"""
		self.id = id
		self.bookValue = bookValue
		self.profit = profit
		self.dividendRate = dividendRate
		self.profitHistory = profitHistory
		self.profitHistory.append(profit)
		self.profitGrowthHistory = [(j/float(i))-1 for i, j in zip(self.profitHistory[:-1], self.profitHistory[1:])]
		random.seed(seed)
		
	def update_profits(self):
		# TODO update 
		growth = 95 + random.randint(0,10)
		self.profit = int((self.profit * growth) / 100)
		self.profitGrowthHistory.append((growth - 100) / 100)
		self.profitHistory.append(self.profit)
        
def testMethod():
	testFirm = Firm(1, 1000, 10000, [10000, 10000], seed = 1)
	print(testFirm.profitHistory)
	print(testFirm.profitGrowthHistory)
	print(testFirm.profit)
	testFirm.update_profits()
	print(testFirm.profit)
	print(testFirm.profitHistory)
	print(testFirm.profitGrowthHistory)
	
#testMethod()