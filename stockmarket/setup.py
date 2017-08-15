"""In this file, we define the set-up procedure of the model"""

import random
import itertools
from stockmarket import firms, stock, valuationfunctions, switchingstrategies
from stockmarket.agent import Trader


def setup_agents(init_money, init_bid_ask_spread, init_memory_size, init_ma_s, init_ma_l, init_propensity_to_switch, fundamentalist=3, chartist=3):
    """This returns an initialized agent set"""
    agent_set = []
    init_agent = lambda x, y: agent_set.append(
                                Trader(name=x,
                                       money=randomize_init_variable(init_money[0], init_money[1]),
                                       bid_ask_spread=randomize_init_variable(init_bid_ask_spread[0], init_bid_ask_spread[1]),
                                       memory=randomize_init_variable(init_memory_size[0], init_memory_size[1]),
                                       ma_short=randomize_init_variable(init_ma_s[0], init_ma_s[1]),
                                       ma_long=randomize_init_variable(init_ma_l[0], init_ma_l[1]),
                                       valuation_function=y, propensity_to_switch=init_propensity_to_switch,
                                       switching_strategy=switchingstrategies.adaptive_switching))
    for agent in range(fundamentalist):
        init_agent(agent, valuationfunctions.extrapolate_average_profit)
    for agent in range(fundamentalist, chartist+fundamentalist):
        init_agent(agent, valuationfunctions.predict_by_moving_avg_growth)
    return agent_set


def setup_firms(init_book_value,
                init_profit,
                firm_profit_mu,
                firm_profit_delta,
                firm_profit_sigma,
                amount_of_firms=1):
    """This returns an initialized firm set"""
    firm_set = []
    for firm in range(amount_of_firms):
        firm_set.append(firms.Firm(name=firm,
                                   book_value=randomize_init_variable(init_book_value[0], init_book_value[1]),
                                   profits=[randomize_init_variable(init_profit[0], init_profit[1])],
                                   mu=firm_profit_mu,
                                   brownian_delta=firm_profit_delta,
                                   brownian_sigma=firm_profit_sigma,
                                   dividend_rate=1))
    for firm in firm_set:
        # creates a profit history for the last 6 periods.
        for _ in itertools.repeat(None, 6):
            firm.update_profits(firm.determine_profit())

    return firm_set


def setup_stocks(set_of_firms, amount):
    stock_set = []
    for firm in set_of_firms:
        stock_set.append(stock.Stock(firm, amount))
    return stock_set


def randomize_init_variable(min_amount, max_amount):
    return random.randint(min_amount, max_amount)


def distribute_initial_stocks(stocks, agents):
    for stock in stocks:
        agent_number = len(agents)
        amount_each = stock.amount // agent_number
        rest = int(stock.amount % agent_number)
        for x in range(0, rest):
            agents[x].stocks[stock] = amount_each + 1
            agents[x].portfolio_value_history[0] += stock.price_history[-1]
        for x in range(rest, agent_number):
            agents[x].stocks[stock] = amount_each
            agents[x].portfolio_value_history[0] += stock.price_history[-1]
        # initialize the agents portfolio value history
