"""In this file, we define general functions for the benchmark stock market model"""
__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

def transaction(buyer, seller, buyerWants, sellerWants, amountOfProduct, amountOfMoney):
    """This function makes a buyer and seller agent perform a transaction with each other"""
    buyer.transact(buyerWants, amountOfProduct, sellerWants, amountOfMoney)
    seller.transact(sellerWants, amountOfMoney, buyerWants, amountOfProduct)
	
	
def calculateNPV():
	"""Fill in this function to calculate NPV"""
	return NPV 