"""This file is our main simulation file it includes the set-up and time loop"""

import random
from stockmarket import functions, setup, marketmechanisms, randomset, database
import stockmarket.parameters as p

random.seed(p.seed)
RECORD_DATA = p.record_data

"""
Setup
"""
agents = setup.setup_agents(init_money=p.initial_money,
                            init_bid_ask_spread=p.initial_bid_ask,
                            init_memory_size=p.initial_memory,
                            init_ma_s=p.initial_ma_short,
                            init_ma_l=p.initial_ma_long,
                            fundamentalist=p.amount_fundamentalists,
                            chartist=p.amount_chartists)

firms = setup.setup_firms(init_book_value=p.initial_book_value,
                          init_profit=p.initial_profit,
                          amount_of_firms=p.amount_firms)

stocks = setup.setup_stocks(firms, amount=p.initial_stock_amount)

setup.distribute_initial_stocks(stocks, agents)

if RECORD_DATA:
    database.create_tables()

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

    # 1 update dividends
    for firm in firms:
        firm.update_profits(firm.determine_growth())
        if RECORD_DATA:
            database.record_statevariables(period=quarter, agent=firm)

    # 2 market mechanism
    for stock in stocks:
        marketmechanisms.trade_stock(agents, p.observable_set_size, stock, randomset.subset_traders, quarter)
        if RECORD_DATA:
            database.record_statevariables(period=quarter, agent=stock)

    # 3 record agent-state variables
    if RECORD_DATA:
        for agent in agents:
            database.record_statevariables(period=quarter, agent=agent)

if RECORD_DATA:
    database.commit()
    database.close()
