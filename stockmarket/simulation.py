from stockmarket import baselineCDA

agents, firms, stocks, order_books = baselineCDA.stockMarketSimulation(seed=0, simulation_time=100, amount_fundamentalists=40,
                                                                       amount_chartists=40, amount_firms=1, initial_money=(100, 200),
                                                                       initial_bid_ask=(1,1), initial_memory=(3,7),
                                                                       initial_ma_short=(1,3), initial_ma_long=(6,7),
                                                                       initial_profit=(200,200), initial_book_value=(10000, 10000),
                                                                       initial_stock_amount=400, order_expiration_time=120, init_propensity_to_switch=1.1,
                                                                       firm_profit_drift_alpha=0.0109,
                                                                       firm_profit_drift_mu=0.02,
                                                                       firm_profit_error_delta=0.25,
                                                                       firm_profit_error_dt=0.1
                                                                       )
