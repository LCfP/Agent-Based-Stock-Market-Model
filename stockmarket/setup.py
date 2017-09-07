"""In this file, we define the set-up procedure of the model"""

import random
import itertools
from stockmarket import firms, stock, valuationfunctions, switchingstrategies, buysellfunctions
from stockmarket.agent import Trader


def setup_agents(init_money, init_bid_ask_spread, init_ma_s, init_ma_l, init_propensity_to_switch,
                 init_price_to_earnings_window, trader_volume_risk_aversion, momentum_traders=3, reversion_traders=3):
    """This returns an initialized agent set"""
    agent_set = []
    init_agent = lambda x, y: agent_set.append(
                                Trader(name=x,
                                       money=randomize_init_variable(init_money[0], init_money[1]),
                                       bid_ask_spread=randomize_init_variable(init_bid_ask_spread[0], init_bid_ask_spread[1]),
                                       ma_short=randomize_init_variable(init_ma_s[0], init_ma_s[1]),
                                       ma_long=randomize_init_variable(init_ma_l[0], init_ma_l[1]),
                                       valuation_function=y, propensity_to_switch=init_propensity_to_switch,
                                       price_to_earnings_window=(randomize_init_variable(init_price_to_earnings_window[0][0],
                                                                                        init_price_to_earnings_window[0][1]),
                                                                 randomize_init_variable(init_price_to_earnings_window[1][0],
                                                                                         init_price_to_earnings_window[1][1])),
                                       trader_volume_risk_aversion=trader_volume_risk_aversion,
                                       switching_strategy=switchingstrategies.adaptive_switching))
    for agent in range(momentum_traders):
        init_agent(agent, buysellfunctions.momentum)
    for agent in range(momentum_traders, reversion_traders+momentum_traders):
        init_agent(agent, buysellfunctions.mean_reversion)
    return agent_set


def setup_agents_with_noise_traders(init_money, init_bid_ask_spread, init_ma_s, init_ma_l,
                                    init_propensity_to_switch, init_price_to_earnings_window,
                                    trader_volume_risk_aversion,
                                    momentum_traders=3, reversion_traders=3, noise_traders=3):
    """This returns an initialized agent set"""
    agent_set = []
    init_agent = lambda x, y: agent_set.append(
        Trader(name=x,
               money=randomize_init_variable(init_money[0], init_money[1]),
               bid_ask_spread=randomize_init_variable(init_bid_ask_spread[0], init_bid_ask_spread[1]),
               ma_short=randomize_init_variable(init_ma_s[0], init_ma_s[1]),
               ma_long=randomize_init_variable(init_ma_l[0], init_ma_l[1]),
               valuation_function=y, propensity_to_switch=init_propensity_to_switch,
               price_to_earnings_window=(randomize_init_variable(init_price_to_earnings_window[0][0],
                                                                 init_price_to_earnings_window[0][1]),
                                         randomize_init_variable(init_price_to_earnings_window[1][0],
                                                                 init_price_to_earnings_window[1][1])),
               trader_volume_risk_aversion=trader_volume_risk_aversion,
               switching_strategy=switchingstrategies.adaptive_switching))
    for agent in range(momentum_traders):
        init_agent(agent, buysellfunctions.momentum)
    for agent in range(momentum_traders, reversion_traders + momentum_traders):
        init_agent(agent, buysellfunctions.mean_reversion)
    for agent in range(reversion_traders + momentum_traders, reversion_traders + momentum_traders + noise_traders):
        init_agent(agent, buysellfunctions.noise_trading)
    return agent_set


def setup_firms(init_book_value,
                init_profit,
                firm_profit_mu,
                firm_profit_delta,
                firm_profit_sigma,
                backward_simulated_time,
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
        for _ in itertools.repeat(None, backward_simulated_time):
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
            agents[x].stocks[stock] += amount_each + 1
            agents[x].portfolio_value_history[0] += agents[x].stocks[stock] * stock.price_history[-1]
        for x in range(rest, agent_number):
            agents[x].stocks[stock] += amount_each
            agents[x].portfolio_value_history[0] += agents[x].stocks[stock] * stock.price_history[-1]
        # initialize the agents portfolio value history

