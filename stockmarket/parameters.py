class Parameters:
    # Simulation
    simulation_time = 100

    experiment_id = 1
    seed = 1

    # Number of agents
    amount_fundamentalists = 12
    amount_chartists = 12
    amount_firms = 3

    # Trader parameters
    initial_money = (100, 200)  # in the range from
    initial_bid_ask = (5, 5)
    initial_memory = (1, 4)

    # Firm parameters
    initial_profit = (200, 200)
    initial_book_value = (10000, 10000)
    initial_stock_amount = 200

    # Trading parameters
    observable_set_size = 3

    # Analysis
    record_data = True

