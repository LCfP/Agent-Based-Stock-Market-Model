"""In this file, we define the set-up procedure of the model"""
__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

import agents


def setupAgents(amountOfAgents=3, seed):
	"""This returns an initialized agent set"""
	agentset = []
	for agent in range(amountOfAgents):
		agentset.append(Trader(money=, stocks=, bidAskSpread=, memorySize=, riskAversion=, extrapolation=)) 
	return agentset