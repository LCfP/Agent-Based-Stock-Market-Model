from stockmarket import baselinemodel

agents, firms, stocks, order_books, market_maker = baselinemodel.stockMarketSimulation(seed=0, simulation_time=100,
                                                                                       amount_momentum=0,
                                                                                       amount_mean_reversion=0,
                                                                                       amount_noise_traders=100,
                                                                                       amount_firms=1,
                                                                                       initial_money=(100, 200),
                                                                                       initial_bid_ask=(1,1),
                                                                                       initial_memory=(3,7),
                                                                                       initial_ma_short=(20,40),
                                                                                       initial_ma_long=(120,150),
                                                                                       initial_profit=(200,200),
                                                                                       initial_book_value=(10000, 10000),
                                                                                       initial_stock_amount=4000,
                                                                                       order_expiration_time=120,
                                                                                       init_propensity_to_switch=1.1,
                                                                                       init_price_to_earnings_window=((4, 7), (10, 14)),
                                                                                       firm_profit_mu=0.058,
                                                                                       firm_profit_delta=0.00396825396,
                                                                                       firm_profit_sigma=0.125,
                                                                                       profit_announcement_working_days=20,
                                                                                       init_market_maker_money=5000,
                                                                                       market_maker_bid_ask_spread=3,
                                                                                       market_maker_price_to_earnings_window=(5,13),
                                                                                       market_maker_inventory_sensitivity=0.01,
                                                                                       market_maker_inventory_buffer_of_total_target=0.10,
                                                                                       m_m_standard_order_percentage_total=0.05,
                                                                                       agents_hold_thresholds=(0.9995, 1.0005),
                                                                                       init_share_of_stocks_to_market_maker=0.4,
                                                                                       init_backward_simulated_time=200,
                                                                                       trader_volume_risk_aversion=0.1,
                                                                                       printProgress=True
                                                                                       )


print(order_books[0].buy_orders_history)

print(order_books[0].sell_orders_history)