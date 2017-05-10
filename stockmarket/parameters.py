# Simulation
simulation_time = 100

experiment_id = 1
seed = 1  # doesn't work yet, has to be implemented in setup

# Number of agents
amount_fundamentalists = 100
amount_chartists = 100
amount_firms = 4

# Trader parameters
initial_money = (100, 200)  # in the range from
initial_bid_ask = (5, 5)
initial_memory = (1, 4)
initial_ma_short = (2, 4)
initial_ma_long = (7, 9)

# Firm parameters
initial_profit = (200, 200)
initial_book_value = (10000, 10000)
initial_stock_amount = 200

# Trading parameters
observable_set_size = 3

# Analysis
record_data = True

# Database
database_name = 'dataBaseOffline.sqlite'
