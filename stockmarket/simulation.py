import pandas as pd
import numpy as np
from stockmarket import baselinemodel
import sqlite3

Transactions, Transactors, Statevariables, Variabletypes, Objects = baselinemodel.stockMarketSimulation(seed=0, simulation_time=100,
                                    amount_fundamentalists=9, amount_chartists=90, amount_firms=1,
                                    initial_money=(100, 200), initial_bid_ask=(0,0), initial_memory=(3,7),
                                    initial_ma_short=(1,3), initial_ma_long=(6,7), initial_profit=(200,200),
                                    initial_book_value=(10000, 10000), initial_stock_amount=400, observable_set_size=3
                                    )

