"""In this file, we define general functions for the benchmark stock market model"""
__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

import numpy as np
import firms
import stocks

def transaction(buyer, seller, buyerWants, sellerWants, amountOfProduct, amountOfMoney):
    """This function makes a buyer and seller agent perform a transaction with each other"""
    buyer.transact(buyerWants, amountOfProduct, sellerWants, amountOfMoney)
    seller.transact(sellerWants, amountOfMoney, buyerWants, amountOfProduct)
	
def calculateNPV(dividend, discountRate=0.05, growthRate=0):
	"""Fill in this function to calculate NPV"""
	# TODO growth rate cannot be higher than discount rate 
	NPV = dividend / (discountRate - growthRate)
	return NPV 
	
def valuationExtrapolateAverage(memory, firm):
	profHistory = firm.profitHistory
	expectedDividend = np.mean(profHistory[len(profHistory)-memory:len(profHistory)])
	value = calculateNPV(firm.profit * firm.dividendRate)
	return value
	
def valuationExtrapolateGrowthAverage(memory, firm):
	profitGrowthHistory = firm.profitGrowthHistory
	expectedGrowth = np.mean(profitGrowthHistory[len(profitGrowthHistory)-memory:len(profitGrowthHistory)])
	value = calculateNPV(firm.profit * firm.dividendRate, growthRate=expectedGrowth)
	return value
    
def create_stocks(firm, faceValue):
    # bookvalue / faceValue = amountOfStocks
    amountOfStocks = firm.bookValue / faceValue
    return stocks.Stock(firm.id, firm, faceValue, amountOfStocks)
    
    
def testMethod():
	testFirm = firms.Firm(1, 1000, 10000, [8000, 10000, 9000, 10000],seed = 1)
	value = valuationExtrapolateAverage(3, testFirm)
	valueG = valuationExtrapolateGrowthAverage(3, testFirm)
	print(value)
	print(valueG)
	
#testMethod()