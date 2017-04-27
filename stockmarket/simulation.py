"""This file is our main simulation file it includes the set-up and time loop"""

import sqlite3
import random
from stockmarket import functions, setup, marketmechanisms, randomset, database

parameter_space = {
    'simulationTime': 100, 'record_data': True, 'experiment_id': 1, 'amount_of_agents': 12, 'amount_of_firms': 3,
    'observable_set_size': 3, 'initial_money': (100, 200), 'initial_bid_ask': (5, 5), 'initial_memory_size': (1, 4),
    'initial_profit': (200, 200), 'initial_book_value': (10000, 10000), 'initial_profit_history': [150, 170, 190],
    'initial_stock_amount': 200, 'seed': 1
}

random.seed(parameter_space['seed'])
RECORD_DATA = parameter_space['record_data']

"""
Setup 
"""
agents = setup.setup_agents(init_money=parameter_space['initial_money'],
                            init_bid_ask_spread=parameter_space['initial_bid_ask'],
                            init_memory_size=parameter_space['initial_memory_size'],
                            seed=parameter_space['seed'], amount_of_agents=parameter_space['amount_of_agents'])
firms = setup.setup_firms(init_book_value=parameter_space['initial_book_value'],
                          init_profit=parameter_space['initial_profit'],
                          init_profit_history=parameter_space['initial_profit_history'],
                          seed=parameter_space['seed'], amount_of_firms=parameter_space['amount_of_firms'])
stocks = setup.setup_stocks(firms, amount=parameter_space['initial_stock_amount'])

# distribute the initial stocks to the agents equally 1 per 1 until non left. (slow)
agents = functions.distribute_initial_stocks(stocks, agents)

if RECORD_DATA:
    conn = sqlite3.connect('dataBaseOffline.sqlite')
    cur = conn.cursor()
    database.create_tables(cur)

"""
Print set-up
"""
functions.print_setup(agents, firms, stocks)

"""
Simulation

Process overview and scheduling from the ODD
1. Update profits
2. Update expected price and spread
3. Market mechanism
4. Store market prices t-1 
"""

for quarter in range(parameter_space["simulationTime"]):

    if RECORD_DATA:
        recordInfo = {'cur': cur, 'experiment_id': parameter_space['experiment_id'],
                      'seed': parameter_space['seed'], 'period': quarter}
    else:
        recordInfo = {}

    # 1 update dividends
    for firm in firms:
        firm.update_profits(lowestpercentage=95, variance=10)
        if RECORD_DATA:
            database.record_statevariables(cur=cur, experiment_id=parameter_space['experiment_id'],
                                       seed=parameter_space['seed'], period=quarter, agent=firm)

    # 2 market mechanism
    for stock in stocks:
        agents = marketmechanisms.market_mechanism(agents, parameter_space['observable_set_size'], stock,
                                                   randomset.subset_traders,
                                                   record=RECORD_DATA, recordInfo=recordInfo)
        if RECORD_DATA:
            database.record_statevariables(cur=cur, experiment_id=parameter_space['experiment_id'],
                                           seed=parameter_space['seed'], period=quarter, agent=stock)

    # 3 record agent-state variables
    if RECORD_DATA:
        for agent in agents:
            database.record_statevariables(cur=cur, experiment_id=parameter_space['experiment_id'],
                                           seed=parameter_space['seed'], period=quarter, agent=agent)

if RECORD_DATA:
    conn.commit()
    cur.close()