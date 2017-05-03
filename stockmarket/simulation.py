"""This file is our main simulation file it includes the set-up and time loop"""

import sqlite3
import random
from stockmarket import functions, setup, marketmechanisms, randomset, database
from stockmarket.parameters import Parameters

p = Parameters()
random.seed(p.seed)
RECORD_DATA = p.record_data

"""
Setup 
"""
agents = setup.setup_agents(init_money=p.initial_money,
                            init_bid_ask_spread=p.initial_bid_ask,
                            init_memory_size=p.initial_memory,
                            seed=p.seed, fundamentalist=p.amount_fundamentalists,
                            chartist=p.amount_chartists)
firms = setup.setup_firms(init_book_value=p.initial_book_value,
                          init_profit=p.initial_profit,
                          seed=p.seed, amount_of_firms=p.amount_firms)
stocks = setup.setup_stocks(firms, amount=p.initial_stock_amount)

# distribute the initial stocks to the agents equally 1 per 1 until non left. (slow)
functions.distribute_initial_stocks(stocks, agents)

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

for quarter in range(p.simulation_time):

    if RECORD_DATA:
        recordInfo = {'cur': cur, 'experiment_id': p.experiment_id,
                      'seed': p.seed, 'period': quarter}
    else:
        recordInfo = {}

    # 1 update dividends
    for firm in firms:
        firm.update_profits(firm.determine_growth())
        if RECORD_DATA:
            database.record_statevariables(cur=cur, experiment_id=p.experiment_id,
                                       seed=p.seed, period=quarter, agent=firm)

    # 2 market mechanism
    for stock in stocks:
        marketmechanisms.market_mechanism(agents, p.observable_set_size, stock,
                                                   randomset.subset_traders,
                                                   record=RECORD_DATA, recordInfo=recordInfo)
        if RECORD_DATA:
            database.record_statevariables(cur=cur, experiment_id=p.experiment_id,
                                           seed=p.seed, period=quarter, agent=stock)

    # 3 record agent-state variables
    if RECORD_DATA:
        for agent in agents:
            database.record_statevariables(cur=cur, experiment_id=p.experiment_id,
                                           seed=p.seed, period=quarter, agent=agent)

if RECORD_DATA:
    conn.commit()
    cur.close()
