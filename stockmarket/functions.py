"""In this file, we define general functions for the benchmark stock market model"""

import numpy as np
import copy
from stockmarket import stocks, firms

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


def transaction(buyer, seller, stock, amount_of_product, amount_of_money):
    """This function makes a buyer and seller agent perform a transaction with each other"""
    # TODO Do a proper test before transaction is done. This implementation is very rigid.
    if buyer.transact(stock, amount_of_product, "money", amount_of_money):
        seller.transact("money", amount_of_money, stock, amount_of_product)

def calculate_npv(dividend, discount_rate=0.05, growth_rate=0):
    """Fill in this function to calculate NPV"""
    # TODO growth rate cannot be higher than discount rate
    npv = dividend / (discount_rate - growth_rate)
    return npv


def valuation_extrapolate_average(memory, firm):
    prof_history = firm.profit_history
    expected_profit = np.mean(prof_history[len(prof_history)-memory:len(prof_history)])
    value = calculate_npv(expected_profit * firm.dividend_rate)
    return value


def valuation_extrapolate_growth_average(memory, firm):
    profit_growth_history = firm.profit_growth_history
    expected_growth = np.mean(profit_growth_history[len(profit_growth_history)-memory:len(profit_growth_history)])
    value = calculate_npv(firm.profit * firm.dividend_rate, growth_rate=expected_growth)
    return value


def create_stocks(firm, face_value):
    amount_of_stocks = firm.book_value / face_value
    return stocks.Stock(firm.name, firm, face_value, amount_of_stocks)
    
    
def test_method():
    test_firm = firms.Firm(1, 1000, 10000, [8000, 10000, 9000, 10000])
    value = valuation_extrapolate_average(3, test_firm)
    value_g = valuation_extrapolate_growth_average(3, test_firm)
    print(value)
    print(value_g)

def distribute_initial_stocks(stocks, agents):
    local_agents = copy.copy(agents)
    local_stocks = copy.copy(stocks)
    for stock in local_stocks:
        amount = stock.amount
        distribute_to_agent = 1
        while amount > 0:
            for agent in local_agents:
                if stock in agent.stocks:
                    agent.stocks[stock] += distribute_to_agent
                else:
                    agent.stocks[stock] = distribute_to_agent
                amount += -distribute_to_agent
                if amount == 0:
                    break

    return (local_stocks, local_agents)

def print_setup(agents, firms, stocks):
    for agent in agents:
        print(repr(agent) + " has $ " + str(agent.money) + "and stocks:", agent.stocks, "and memory of ",
              agent.memory_size, " finally the bid-ask spread size is ", agent.bid_ask_spread)
    for firm in firms:
        print(repr(firm) + " has a book value of " + str(firm.book_value) + " profit of ", firm.profit,
              "profit history of ", firm.profit_history, " and a divididend ratio of ", firm.dividend_rate)
    for stock in stocks:
        print(repr(stock) + ", amount " + str(stock.amount) + " links to Firm ", stock.firm)


def print_quarterly_data(agents, firms):
    print("Info on firms.")
    for firm in firms:
        firm.show()

    print("Info on agents.")
    for agent in agents:
        agent.show()