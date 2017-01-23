"""In this file, we define the set-up procedure of the model"""
__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

import agents
import random
import firms
import functions

def setupAgents(initMoney, initBidAskSpread, initMemorySize,seed ,amountOfAgents=3):
	"""This returns an initialized agent set"""
	random.seed(seed)
	agentset = []
	for agent in range(amountOfAgents):
		agentset.append(agents.Trader(id=agent, 
								money=randomizeInitVariable(initMoney[0], initMoney[1]), 
								bidAskSpread=randomizeInitVariable(initBidAskSpread[0], initBidAskSpread[1]), 
								memorySize=randomizeInitVariable(initMemorySize[0], initMemorySize[1]))) 
	return agentset

def setupFirms(initBookValue, initProfit, initprofitHistory, seed, amountOfFirms=1):
    """This returns an initialized firm set"""
    random.seed(seed)
    firmSet = []
    for firm in range(amountOfFirms):
        firmSet.append(firms.Firm(id=firm ,bookValue=randomizeInitVariable(initBookValue[0], initBookValue[1]),
                            profit=randomizeInitVariable(initProfit[0], initProfit[1]),
                            profitHistory = initprofitHistory, 
                            # this makes sure that individual firms have a different seed every simulation
                            seed=random.randint(0,10000), 
                            dividendRate = 1))
    return firmSet
 
def setupStocks(setOfFirms, faceValue):
    stockSet = []
    for firm in setOfFirms:
        stockSet.append(functions.create_stocks(firm, faceValue))
    return stockSet
 
def randomizeInitVariable(minamount, maxamount):
	amount = random.randint(minamount, maxamount)
	return amount
	
