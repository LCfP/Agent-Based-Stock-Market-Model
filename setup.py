"""In this file, we define the set-up procedure of the model"""
__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

import agents
import random

def setupAgents(amountOfAgents=3, seed):
	"""This returns an initialized agent set"""
	random.seed(seed)
	agentset = []
	for agent in range(amountOfAgents):
		# TODO
		agentset.append(Trader(money=initialMoney(), stocks=, bidAskSpread=, memorySize=, riskAversion=, extrapolation=)) 
	return agentset
	
def initialMoney():
	money = 10000 * random.int
	return money