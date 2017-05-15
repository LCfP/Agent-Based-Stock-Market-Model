from stockmarket import baselinemodel

baselinemodel.stockMarketSimulation(seed=1, simulation_time=100,
                                    amount_fundamentalists=40, amount_chartists=40, amount_firms=4,
                                    initial_money=(100, 200), initial_bid_ask=(5,5), initial_memory=(1,4),
                                    initial_ma_short=(1,3), initial_ma_long=(6,7), initial_profit=(200,200),
                                    initial_book_value=(10000, 10000), initial_stock_amount=400, observable_set_size=3
                                    )
