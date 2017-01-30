"""This file is our main simulation file it includes the set-up and time loop"""

import setup

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


"""
Define initial variables and parameters
"""
AMOUNT_OF_AGENTS = 3
AMOUNT_OF_FIRMS = 2

SEED = 1

INIT_MONEY = (100, 200)
INIT_BID_ASK = (5, 5)
INIT_MEMORY_SIZE = (2, 3)

INIT_PROFIT = (200, 200)
INIT_BOOK_VALUE = (10000, 10000)
PROFIT_HISTORY = [150, 170, 190]

INIT_FACE_VALUE = 50

"""
Setup 
"""
agents = setup.setup_agents(init_money=INIT_MONEY, init_bid_ask_spread=INIT_BID_ASK, init_memory_size=INIT_MEMORY_SIZE,
                            seed=SEED, amount_of_agents=AMOUNT_OF_AGENTS)
firms = setup.setup_firms(init_book_value=INIT_BOOK_VALUE, init_profit=INIT_PROFIT, init_profit_history=PROFIT_HISTORY,
                          seed=SEED, amount_of_firms=AMOUNT_OF_FIRMS)
stocks = setup.setup_stocks(firms, face_value=INIT_FACE_VALUE)
# distribute the initial stocks to the agents equally 1 per 1 until non left. (slow)
for stock in stocks:
    amount = stock.amount
    distribute_to_agent = 1
    while amount > 0:
        for agent in agents:
            if stock in agent.stocks:
                agent.stocks[stock] += distribute_to_agent
            else:
                agent.stocks[stock] = distribute_to_agent
            amount += -distribute_to_agent
            if amount == 0:
                break

parameter_space = {"simulationTime": 10}
for agent in agents:
    print(repr(agent) + " has " + str(agent.money) + "$ and stocks:")
    print(agent.stocks)
for firm in firms:
    print(repr(firm) + " has a book value of " + str(firm.book_value))
for stock in stocks:
    print(repr(stock) + ", amount " + str(stock.amount))

"""
Simulation

Process overview and scheduling from the ODD
1. Update profits
2. Update expected price and spread
3. Market mechanism
4. Store market prices t-1 
"""

# for quarter in range(parameter_space["simulationTime"]):
#     1 update dividends
#
#     2 update expected price and spread
#
#     3 market mechanism
#     For actingTrader in Traders:
#         Observe random subset of traders
#
#         Calculate best deal and trade with that trader (buy or sell)
#
#         Write data on counter party + quantity + price to data set
#
#     4 store market prices
