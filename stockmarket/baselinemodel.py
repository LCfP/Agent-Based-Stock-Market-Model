"""This file is our main simulation file it includes the set-up and time loop"""

import random
import numpy as np
from stockmarket.limitorderbook import *
from stockmarket import setup, marketmechanisms, marketmaker
from stockmarket.functions import div0

def stockMarketSimulation(seed,
                          simulation_time,
                          init_backward_simulated_time,
                          number_of_agents,
                          share_chartists,
                          share_mean_reversion,
                          amount_of_firms,
                          initial_total_money,
                          initial_profit,
                          discount_rate,
                          init_price_to_earnings_window,
                          order_expiration_time,
                          agent_order_price_variability,
                          agent_order_variability,
                          agent_ma_short,
                          agent_ma_long,
                          agents_hold_thresholds,
                          agent_volume_risk_aversion,
                          agent_propensity_to_switch,
                          firm_profit_mu,
                          firm_profit_delta,
                          firm_profit_sigma,
                          profit_announcement_working_days,
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

    # divide total money into (approximately) money per agent
    initial_money = (int(initial_total_money[0] / number_of_agents), int(initial_total_money[1] / number_of_agents))
    # calculate the amount of different types of traders
    amount_technical_traders = int(number_of_agents * (share_chartists))
    amount_noise_traders = number_of_agents - amount_technical_traders
    amount_mean_reversion = int(share_mean_reversion * amount_technical_traders)
    amount_momentum = amount_technical_traders - amount_mean_reversion

    agents = setup.setup_agents_with_noise_traders(init_money=initial_money,
                                                   init_bid_ask_spread=agent_order_price_variability,
                                                   init_ma_s=agent_ma_short,
                                                   init_ma_l=agent_ma_long,
                                                   trader_volume_risk_aversion=agent_volume_risk_aversion,
                                                   momentum_traders=amount_momentum,
                                                   reversion_traders=amount_mean_reversion,
                                                   noise_traders=amount_noise_traders,
                                                   init_propensity_to_switch=agent_propensity_to_switch,
                                                   init_price_to_earnings_window=init_price_to_earnings_window)


    firms = setup.setup_firms(init_book_value=(10000,10000),
                              init_profit=initial_profit,
                              firm_profit_mu=firm_profit_mu,
                              firm_profit_delta=firm_profit_delta,
                              firm_profit_sigma=firm_profit_sigma,
                              backward_simulated_time=init_backward_simulated_time,
                              amount_of_firms=amount_of_firms
                              )

    # initialise the amount of stocks so that buy and sell orders are roughly equal for noise trader baseline
    init_firm_value = initial_profit[1] / discount_rate
    initial_stock_amount = np.sqrt(initial_total_money[1] * init_firm_value * number_of_agents)
    stocks = setup.setup_stocks(firms, amount=initial_stock_amount)

    order_books = []
    for stock in stocks:
        order_books.append(LimitOrderBook(stock, stock.price_history[-1], order_expiration_time, agent_order_price_variability))

    setup.distribute_initial_stocks(stocks, agents)

    """
    Simulation

    Process overview and scheduling from the ODD
    1. Update profits
    2. Update expected price and spread
    3. Market mechanism
    4. Store market prices t-1
    """

    for day in range(simulation_time):
        if printProgress:
            print('period: ', day)
        # 1 update profits after a number of working days or update profit history with the current profit
        for firm in firms:
            if day % profit_announcement_working_days == 0:
                profit = firm.determine_profit()
            else:
                profit = firm.profit
            firm.update_profits(profit)

        # 2-3 continuous double auction market mechanism - market maker quotes, traders trade
        market_returns = []
        for idx, stock in enumerate(stocks):
            agents, stock, order_books[idx] = marketmechanisms.continuous_double_auction(agents, stock,
                                                                                         order_books[idx],
                                                                                         marketmechanisms.orders_based_on_sentiment_and_fundamentals,
                                                                                         agents_hold_thresholds, agent_order_variability)
            current = stock.price_history[-1]
            previous = stock.price_history[-2]
            diff = div0((current - previous), previous) if current != 0 else 0.0

            market_returns.append(diff)

        av_market_return = np.mean(market_returns)
        current_market_price = stock.price_history[-1]
        earnings_per_stock = stock.firm.profit / stock.amount
        current_price_to_earnings_ratio = current_market_price / earnings_per_stock
        stock.price_to_earnings_history.append(current_price_to_earnings_ratio)

        # 4 record and update variables + switching strategies
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
            # 4 update strategies
            agent.update_strategy(av_market_return, current_price_to_earnings_ratio)


    return agents, firms, stocks, order_books







