"""In this file, we define general functions for the benchmark stock market model"""

import numpy as np
import copy
import sqlite3
from stockmarket import stocks, firms

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


def transaction(buyer, seller, stock, amount_of_product, amount_of_money, record=False, recordInfo={}):
    """This function makes a buyer and seller agent perform a transaction with each other"""
    # TODO Do a proper test before transaction is done. This implementation is very rigid.
    if buyer.transact(stock, amount_of_product, "money", amount_of_money):
        seller.transact("money", amount_of_money, stock, amount_of_product)
    # record the transaction
    if record:
        cur = recordInfo['cur']
        cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)",
                    (repr(buyer), repr(buyer)[:repr(buyer).find('_')]))
        cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(buyer),))
        buyer_id = cur.fetchone()[0]

        cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)",
                    (repr(seller), repr(seller)[:repr(seller).find('_')]))
        cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(seller),))
        seller_id = cur.fetchone()[0]

        cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)",
                    (repr(stock), repr(stock)[:repr(stock).find('_')]))
        cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(stock),))
        stock_id = cur.fetchone()[0]

        cur.execute("INSERT INTO Transactions (experiment_id, seed, period, amount_of_product, "
                    "amount_of_money) VALUES (?,?,?,?,?)",
                    (recordInfo['experiment_id'], recordInfo['seed'], recordInfo['period'],
                     amount_of_product, amount_of_money))
        cur.execute("SELECT MAX(id) FROM Transactions")
        transaction_id = cur.fetchone()[0]

        cur.execute("INSERT OR IGNORE INTO Transactors (transaction_id, transactor_id, role) VALUES (?,?,?)",
                    (transaction_id, buyer_id, 'buyer'))
        cur.execute("INSERT OR IGNORE INTO Transactors (transaction_id, transactor_id, role) VALUES (?,?,?)",
                    (transaction_id, seller_id, 'seller'))
        cur.execute("INSERT OR IGNORE INTO Transactors (transaction_id, transactor_id, role) VALUES (?,?,?)",
                    (transaction_id, stock_id, 'stock'))


def calculate_npv(dividend, discount_rate=0.05, growth_rate=0):
    """Fill in this function to calculate NPV"""
    # TODO growth rate cannot be higher than discount rate
    if discount_rate < growth_rate:
        raise ValueError('discount rate < growth rate', 'dc = ' + str(discount_rate), 'gr = ' + str(growth_rate))
    npv = dividend / (discount_rate - growth_rate)
    return npv


def create_stocks(firm, face_value):
    amount_of_stocks = firm.book_value / face_value
    return stocks.Stock(firm.name, firm, face_value, amount_of_stocks)

def distribute_initial_stocks(stocks, agents):
    local_agents = copy.copy(agents)
    local_stocks = copy.copy(stocks)
    for stock in local_stocks:
        amount = stock.amount
        distribute_to_agent = 1
        while amount > 0:
            for agent in local_agents:
                if repr(stock) in agent.stocks:
                    agent.stocks[repr(stock)] += distribute_to_agent
                else:
                    agent.stocks[repr(stock)] = distribute_to_agent
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