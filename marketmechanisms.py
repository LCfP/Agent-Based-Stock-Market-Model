"""In this file, we define market matching mecahnism functions. These functions take in agent sets and output matched pairs of agents"""

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

import random
import math

def bounded_best_price(agentset, observablesetsize, stock, valuation_function, seed):
    """return set of matched agents"""
    setOfMatchedAgents = []
    random.seed(seed)
    randomizedAgentSet = list(agentset)
    random.shuffle(randomizedAgentSet)

    # every demand agent observes a subset of other agents from which it picks the cheapest supplier
    for demander in randomizedAgentSet:
        demanderPrice = demander.valuate_stocks(stock=stock, valuation_function=valuation_function) \
                        * (1-(demander.bid_ask_spread/200)) # /2 and / 100 for percent
        totalObservableSet = list(randomizedAgentSet)
        totalObservableSet.remove(demander)
        observableSet = [totalObservableSet[i] for i in sorted(random.sample(range(len(totalObservableSet)),
                                                                             observablesetsize))]
        # Find cheapest supplier and safe the price
        minSupplierandPrice = (None, math.inf)

        for supplier in observableSet:
            supplierPrice = supplier.valuate_stocks(stock=stock, valuation_function=valuation_function) \
            * (1 + (supplier.bid_ask_spread / 200))

            if supplierPrice < minSupplierandPrice[1]:
                minSupplierandPrice = (supplier, supplierPrice)

        # If the minimum price of all suppliers is lower than the ask price, make deal with demander
        if minSupplierandPrice[1] <= demanderPrice:
            setOfMatchedAgents.append((demander, minSupplierandPrice[0]))

    return setOfMatchedAgents
    # observe random set and take highest