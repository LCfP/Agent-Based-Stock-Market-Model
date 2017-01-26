"""In this file, we define market matching mecahnism functions. These functions take in agent sets and output matched pairs of agents"""

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'

import random

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
        supplierAndPrice = {}
        for supplier in observableSet:
            supplierPrice = supplier.valuate_stocks(stock=stock, valuation_function=valuation_function) \
            * (1 + (supplier.bid_ask_spread / 200))
            supplierAndPrice[str(supplier)] = supplierPrice

        min_value = min(supplierAndPrice.values())
        min_keys = sorted([k for k in supplierAndPrice if supplierAndPrice[k] == min_value])
        cheapestSupplier = random.choice(min_keys)

        if supplierAndPrice[cheapestSupplier] <= demanderPrice:
            setOfMatchedAgents.append((demander, cheapestSupplier))


    return setOfMatchedAgents
    # observe random set and take highest