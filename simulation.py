"""This file is our main simulation file it includes the set-up and time loop"""
__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

import agents
import functions

"""
Set-up the initial variables here
"""

SIMULATIONTIMEINQUARTERS = 10


"""
Timeline

Process overview and scheduling from the ODD
1. Update dividends
2. Update expected price and spread
3. Market mechanism
4. Store market prices t-1 
"""

for quarter in range(SIMULATIONTIMEINQUARTERS):
	# 1 update dividends
	
	# 2 update expected price and spread

	# 3 market mechanism
	For actingTrader in Traders:
		#Observe random subset of traders
		
		#Calculate best deal and trade with that trader (buy or sell) 
		
		#Write data on counterparty + quantity + price to dataset
	
	# 4 store market prices