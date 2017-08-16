"""This file is our main simulation file it includes the set-up and time loop"""

import random
import numpy as np
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
                          init_propensity_to_switch,
                          firm_profit_mu,
                          firm_profit_delta,
                          firm_profit_sigma,
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
        agents, firms, stocks, and orderbooks
    """

    random.seed(seed)
    np.random.seed(seed)

    """
    Setup
    """
    agents = setup.setup_agents(init_money=initial_money,
                                init_bid_ask_spread=initial_bid_ask,
                                init_memory_size=initial_memory,
                                init_ma_s=initial_ma_short,
                                init_ma_l=initial_ma_long,
                                fundamentalist=amount_fundamentalists,
                                chartist=amount_chartists, init_propensity_to_switch=init_propensity_to_switch)

    firms = setup.setup_firms(init_book_value=initial_book_value,
                              init_profit=initial_profit,
                              firm_profit_mu=firm_profit_mu,
                              firm_profit_delta=firm_profit_delta,
                              firm_profit_sigma=firm_profit_sigma,
                              amount_of_firms=amount_firms
                              )

    stocks = setup.setup_stocks(firms, amount=initial_stock_amount)

    order_books = []
    for stock in stocks:
        order_books.append(LimitOrderBook(stock, stock.price_history[-1], order_expiration_time))

    setup.distribute_initial_stocks(stocks, agents)

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
            firm.update_profits(firm.determine_profit())

        # 2 market mechanism
        market_returns = []
        for idx, stock in enumerate(stocks):
            # marketmechanisms.continuousDoubleAuction
            agents, stock, order_books[idx] = marketmechanisms.continuous_double_auction(agents, stock,
                                                                                         order_books[idx])
            current = stock.price_history[-1]
            previous = stock.price_history[-2]
            diff = (current - previous) / previous if previous != 0 else (current - (previous + 0.00001)) / (
                previous + 0.00001) if current != 0 else 0.0
            market_returns.append(diff)
        av_market_return = np.mean(market_returns)

        # 3 record and update variables
        for agent in agents:
            # record agent stocks
            agent.portfolio_history.append(agent.stocks.copy())
            # evaluate and record agent returns
            money = agent.money
            portfolio_value = 0
            for stock in stocks:
                portfolio_value += agent.stocks[stock] * stock.price_history[-1]
            income = money - agent.money_history[-1] + portfolio_value - agent.portfolio_value_history[-1]
            average_total_assets = np.mean([money,agent.money_history[-1]]) + \
                                   np.mean([portfolio_value, agent.portfolio_value_history[-1]])
            agent.return_on_assets.append(income / average_total_assets)
            agent.money_history.append(money)
            agent.portfolio_value_history.append(portfolio_value)
            agent.function_history.append(agent.function)
            # update strategies
            agent.update_strategy(av_market_return)


    return agents, firms, stocks, order_books







