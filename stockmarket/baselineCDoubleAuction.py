"""This file is our main simulation file it includes the set-up and time loop"""

import random
from stockmarket.limitorderbook import *
from stockmarket import setup, marketmechanisms, database


def stockMarketSimulation(seed,
                          simulation_time,
                          amount_fundamentalists,
                          amount_chartists,
                          amount_firms,
                          initial_money,
                          initial_bid_ask,
                          initial_memory,
                          initial_ma_short,
                          initial_ma_long,
                          initial_profit,
                          initial_book_value,
                          initial_stock_amount,
                          order_expiration_time,
                          printProgress=False):
    """Returns a set of agents at time stockMarketSimulationParameterSet['simuatlion_time'] and the values
    of their state variables for every time step in stockMarketSimulationParameterSet['simuatlion_time'].

    Arguments
    ----------
    seed : integer
        Seed used to set the pseudo number generator for experiment reproduction
    simulation_time : integer
        Amount of periods over which the simulation takes place
    amount_fundamentalists: integer
        Sets the amount of fundamentalist type agents
    amount_chartists : integer
        Sets the amount of chartist type agents
    amount_firms: integer
        Sets the amount of firms
    initial_money: tuple
        Integer range (low, high) for the initial amount of money for every trader
    initial_bid_ask: tuple
        Integer range (Low, high) for the initial bid-ask spread for every trader
    initial_memory: tuple
        Integer range (Low, high) for the initial memory size for every trader
    initial_ma_short: tuple
        Integer range (Low, high) for the MA memory size for every trader who uses the chartist strategy
    initial_ma_long: tuple
        Integer range (Low, high) for the MA memory size for every trader who uses the chartist strategy
    initial_profit: tuple
        Integer range (Low, high) for the initial profit for every firm
    initial_book_value: tuple
        Integer range (Low, high) for the initial book_value for every firm
    initial_stock_amount: tuple
        Integer range (Low, high) for the initial amount of stocks distributed for every firm
    observable_set_size: integer
        The amount of suppliers observable in the market mechanism
    record_data: boolean
        This can be switched of for bigger models so that no data is recorder
    database_name: string
        Name of the database saved

    Returns
    -------
    list
        Pandas dataframes with records of all agent state variables and transactions over the simulation
    """

    random.seed(seed)

    """
    Setup
    """
    agents = setup.setup_agents(init_money=initial_money,
                                init_bid_ask_spread=initial_bid_ask,
                                init_memory_size=initial_memory,
                                init_ma_s=initial_ma_short,
                                init_ma_l=initial_ma_long,
                                fundamentalist=amount_fundamentalists,
                                chartist=amount_chartists)

    firms = setup.setup_firms(init_book_value=initial_book_value,
                              init_profit=initial_profit,
                              amount_of_firms=amount_firms)

    stocks = setup.setup_stocks(firms, amount=initial_stock_amount)

    order_books = []
    for stock in stocks:
        order_books.append(LimitOrderBook(stock, stock.price_history[-1], order_expiration_time))

    setup.distribute_initial_stocks(stocks, agents)

    # Create databases and initialize objects
    Transactions, Transactors, Statevariables, Variabletypes, Objects = database.stock_market_baseline_tables()

    """
    Print set-up
    """
    #if (printProgress):
    #    functions.print_setup(agents, firms, stocks)

    """
    Simulation

    Process overview and scheduling from the ODD
    1. Update profits
    2. Update expected price and spread
    3. Market mechanism
    4. Store market prices t-1
    """

    for quarter in range(simulation_time):
        if printProgress:
            print('period: ', quarter)
        # 1 update dividends
        for firm in firms:
            firm.update_profits(firm.determine_growth())
            Statevariables, Variabletypes, Objects = database.df_update_statevariables(seed, quarter,
                                                                                       firm, Statevariables,
                                                                                       Variabletypes, Objects)

        # 2 market mechanism
        for idx, stock in enumerate(stocks):
            # marketmechanisms.continuousDoubleAuction
            agents, stock, order_books[idx], \
            Transactions, Transactors, Objects = marketmechanisms.continuous_double_auction(agents, stock,
                                                                                            order_books[idx],
                                                                                            quarter, seed,
                                                                                            Transactions,
                                                                                            Transactors, Objects)

            Statevariables, Variabletypes, Objects = database.df_update_statevariables(seed, quarter,
                                                                                       stock, Statevariables,
                                                                                       Variabletypes, Objects)


        # 3 record all agent-state variables
        for agent in agents:
            Statevariables, Variabletypes, Objects = database.df_update_statevariables(seed, quarter,
                                                                                       agent, Statevariables,
                                                                                       Variabletypes, Objects)

    return Transactions, Transactors, Statevariables, Variabletypes, Objects







