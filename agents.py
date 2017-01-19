"""In this file, we define the benchmark stock market model agent classes"""
__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

import functions
import stocks

class Trader:
    """a base class for Traders"""
    def __init__(self, id, money, stocks, bidAskSpread, memorySize, riskAversion, extrapolation):
        """Creates a new trader"""
		self.id = id
        self.money = money
        self.stocks = stocks
        self.bidAskSpread = bidAskSpread
		self.memorySize = memorySize
		self.riskAversion = riskAversion
		self.extrapolation	= extrapolation
	
	def valuateStocks(stock, valuationFunction):
		# TODO test this function
		npvFirm = valuationFunction(self.memorySize, stock.firm)
		# evaluate the below calculation (currently additional stocks dillute value directly)
		stockvalue = npvFirm / (stock.firm.bookValue / stock.faceValue)
		return stockValue
	
	def transact(self, inflowItem, inflowAmount, outflowItem, outflowAmount):
		"""This allows an agent to transact stocks and money"""
        if ((inflowItem == "stocks") & (outflowItem == "money") & (outflowAmount <= self.money)):
            self.stocks += inflowAmount
            self.money -= outflowAmount
            print (self, "I just purchased stocks") # for debugging purposes
        elif ((inflowItem == "money") & (outflowItem == "stocks") & (outflowAmount <= self.stocks)):
            self.money += inflowAmount
            self.stocks -= outflowAmount
            print (self, "I just sold stocks")
        else: 
            print ("No transaction possible ")