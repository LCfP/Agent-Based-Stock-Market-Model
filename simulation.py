"""This file is our main simulation file it includes the set-up and time loop"""
__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

import agents
import functions
import setup

"""
Define initial variables and parameters
"""
AMOUNTOFAGENTS = 3
AMOUNTOFFIRMS = 1

SEED = 1

INITMONEY = (100,200)
INITBIDASK = (5,5)
INITMEMORYSIZE = (2,3)

INITPROFIT = (200, 200)
INITBOOKVALUE = (10000,10000)
PROFITHISTORY = [150, 170, 190]

INITFACEVALUE = 50

"""
Setup 
"""
agents = setup.setupAgents(initMoney=INITMONEY, initBidAskSpread=INITBIDASK, initMemorySize=INITMEMORYSIZE, seed=SEED, amountOfAgents=AMOUNTOFAGENTS)
firms = setup.setupFirms(initBookValue=INITBOOKVALUE, initProfit=INITPROFIT, initprofitHistory=PROFITHISTORY, seed=SEED, amountOfFirms=AMOUNTOFFIRMS)
stocks = setup.setupStocks(firms, faceValue=INITFACEVALUE)
# distribute the initial stocks to the agents
for stock in stocks:
    for agent in agents:
        agent.stocks.append([stock, 0])
    amount = stock.amount
    while (amount > 0):   
        for agent in agents:
            agent.stocks[stock.id][1] += 1

parameterspace = {"simulationTime" : 10}
for agent in agents:
    print(agent.money)
    print(agent.stocks)
for firm in firms:
    print(firm.bookValue)
for stock in stocks:
    print(stock.firm)
    print(stock.amount)

"""
Simulation

Process overview and scheduling from the ODD
1. Update dividendspy
2. Update expected price and spread
3. Market mechanism
4. Store market prices t-1 
"""

#for quarter in range(parameterspace["simulationTime"]):
	# 1 update dividends
	
	# 2 update expected price and spread

	# 3 market mechanism
	#For actingTrader in Traders:
		#Observe random subset of traders
		
		#Calculate best deal and trade with that trader (buy or sell) 
		
		#Write data on counterparty + quantity + price to dataset
	
	# 4 store market prices