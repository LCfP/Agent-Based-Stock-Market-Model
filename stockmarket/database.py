"""In this file, we provide functions for creating and updating the database"""

import sqlite3
import pandas as pd


def stock_market_baseline_tables():
    Transactions = pd.DataFrame(columns= ['id', 'seed', 'period', 'amount_of_product', 'amount_of_money'])
    Transactors = pd.DataFrame(columns= ['transaction_id', 'transactor_id', 'role'])
    Statevariables = pd.DataFrame(columns= ['id', 'seed', 'period', 'variable_id', 'owner_id', 'value'])
    Variabletypes = pd.DataFrame(columns=['id', 'variable_type'])
    Objects = pd.DataFrame(columns=['id', 'object_name', 'object_type'])
    return Transactions, Transactors, Statevariables, Variabletypes, Objects


def create_CDA_tables(cur, seed):
    script = '''\
            DROP TABLE IF EXISTS Statevariables{seed};
            DROP TABLE IF EXISTS Variabletypes{seed};
            DROP TABLE IF EXISTS Objects{seed};

            CREATE TABLE Statevariables{seed} (
                id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                seed INTEGER,
                period INTEGER,
                variable_id INTEGER,
                owner_id INTEGER,
                value REAL
            );

            CREATE TABLE Variabletypes{seed} (
                id  INTEGER NOT NULL PRIMARY KEY
                    AUTOINCREMENT UNIQUE,
                variable_type TEXT  UNIQUE
            );

            CREATE TABLE Objects{seed} (
                id  INTEGER NOT NULL PRIMARY KEY
                    AUTOINCREMENT UNIQUE,
                object_name TEXT  UNIQUE,
                object_type TEXT
            );

            '''

    seeds = {'seed': str(seed)}
    scr = script.format(**seeds)
    cur.executescript(scr)


def record_state_variables(cur, seed, agents, simulation_time, firms, stocks, order_books):
    """records all state variables from agents, firms, stocks and the orderbook in an SQL database"""
    # add agents variables to the SQL database
    for agent in agents:
        # 1 store the agent and type of agent in the objects table
        cur.execute("INSERT OR IGNORE INTO Objects{} (object_name, object_type) VALUES (?,?)".format(seed),
                    (repr(agent), repr(agent)[:repr(agent).find('_')]))
        cur.execute("SELECT id FROM Objects{} WHERE object_name = ?".format(seed), (repr(agent),))
        owner_id = cur.fetchone()[0]
        # for the agent-variables
        variables = vars(agent)
        for variable in variables:
            # store the variable type in the variable types table
            cur.execute("INSERT OR IGNORE INTO Variabletypes{} (variable_type) VALUES (?)".format(seed), (str(variable),))
            cur.execute("SELECT id FROM Variabletypes{} WHERE variable_type = ?".format(seed), (str(variable),))
            variable_type_id = cur.fetchone()[0]
            # store the variable content in the state variables table
            if not 'history' in str(variable):
                cur.execute(
                    "INSERT INTO Statevariables{} (seed, period, variable_id, owner_id, value) VALUES (?,?,?,?,?)".format(seed),
                    (seed, 0, variable_type_id, owner_id, str(variables[variable])))
            else:
                if len(variables[variable]) > simulation_time:
                    var = variables[variable][(len(variables[variable]) - simulation_time):]
                else:
                    var = variables[variable]
                for idx, element in enumerate(var):
                    cur.execute(
                        "INSERT INTO Statevariables{} (seed, period, variable_id, owner_id, value) VALUES (?,?,?,?,?)".format(seed),
                        (seed, idx, variable_type_id, owner_id, str(element)))
    # add stock variables to the SQL database
    for stock in stocks:
        # 1 store the stock and type of stock in the objects table
        cur.execute("INSERT OR IGNORE INTO Objects{} (object_name, object_type) VALUES (?,?)".format(seed),
                    (repr(stock), repr(stock)[:repr(stock).find('_')]))
        cur.execute("SELECT id FROM Objects{} WHERE object_name = ?".format(seed), (repr(stock),))
        owner_id = cur.fetchone()[0]
        # for the stock-variables
        variables = vars(stock)
        for variable in variables:
            # store the variable type in the variable types table
            cur.execute("INSERT OR IGNORE INTO Variabletypes{} (variable_type) VALUES (?)".format(seed), (str(variable),))
            cur.execute("SELECT id FROM Variabletypes{} WHERE variable_type = ?".format(seed), (str(variable),))
            variable_type_id = cur.fetchone()[0]
            # store the variable content in the state variables table
            if not 'history' in str(variable):
                cur.execute(
                    "INSERT INTO Statevariables{} (seed, period, variable_id, owner_id, value) VALUES (?,?,?,?,?)".format(seed),
                    (seed, 0, variable_type_id, owner_id, str(variables[variable])))
            # Mainly to store the price-to-earnings-history
            else:
                var = variables[variable]
                # store the prices, volumes and unresolved orders in the state variables table
                for idx, element in enumerate(var):
                    cur.execute(
                        "INSERT INTO Statevariables{} (seed, period, variable_id, owner_id, value) VALUES (?,?,?,?,?)".format(seed),
                        (seed, idx, variable_type_id, owner_id, str(element)))
    for firm in firms:
        # 1 store the firm and type of firm in the objects table
        cur.execute("INSERT OR IGNORE INTO Objects{} (object_name, object_type) VALUES (?,?)".format(seed),
                    (repr(firm), repr(firm)[:repr(firm).find('_')]))
        cur.execute("SELECT id FROM Objects{} WHERE object_name = ?".format(seed), (repr(firm),))
        owner_id = cur.fetchone()[0]
        # for the firm-variables
        variables = vars(firm)
        for variable in variables:
            # store the variable type in the variable types table
            cur.execute("INSERT OR IGNORE INTO Variabletypes{} (variable_type) VALUES (?)".format(seed), (str(variable),))
            cur.execute("SELECT id FROM Variabletypes{} WHERE variable_type = ?".format(seed), (str(variable),))
            variable_type_id = cur.fetchone()[0]
            # store the variable content in the state variables table
            if not 'history' in str(variable):
                cur.execute(
                    "INSERT INTO Statevariables{} (seed, period, variable_id, owner_id, value) VALUES (?,?,?,?,?)".format(seed),
                    (seed, 0, variable_type_id, owner_id, str(variables[variable])))
            else:
                if len(variables[variable]) > simulation_time:
                    var = variables[variable][(len(variables[variable]) - simulation_time):]
                else:
                    var = variables[variable]
                for idx, element in enumerate(var):
                    cur.execute(
                        "INSERT INTO Statevariables{} (seed, period, variable_id, owner_id, value) VALUES (?,?,?,?,?)".format(seed),
                        (seed, idx, variable_type_id, owner_id, str(element)))
    for book in order_books:
        # 1 store the book and type of book in the objects table
        cur.execute("INSERT OR IGNORE INTO Objects{} (object_name, object_type) VALUES (?,?)".format(seed),
                    (repr(book), repr(book)[:repr(book).find('_')]))
        cur.execute("SELECT id FROM Objects{} WHERE object_name = ?".format(seed), (repr(book),))
        owner_id = cur.fetchone()[0]
        # for the firm-variables
        variables = vars(book)
        for variable in variables:
            # store the variable type in the variable types table
            cur.execute("INSERT OR IGNORE INTO Variabletypes{} (variable_type) VALUES (?)".format(seed), (str(variable),))
            cur.execute("SELECT id FROM Variabletypes{} WHERE variable_type = ?".format(seed), (str(variable),))
            variable_type_id = cur.fetchone()[0]
            # store the variable content in the state variables table
            if not 'history' in str(variable):
                cur.execute(
                    "INSERT INTO Statevariables{} (seed, period, variable_id, owner_id, value) VALUES (?,?,?,?,?)".format(seed),
                    (seed, 0, variable_type_id, owner_id, str(variables[variable])))
            else:
                var = variables[variable]
                # store the prices, volumes and unresolved orders in the state variables table
                for idx, element in enumerate(var):
                    cur.execute(
                        "INSERT INTO Statevariables{} (seed, period, variable_id, owner_id, value) VALUES (?,?,?,?,?)".format(seed),
                        (seed, idx, variable_type_id, owner_id, str(element)))


