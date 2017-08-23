"""In this file, we provide functions for creating and updating the database"""

import sqlite3
import pandas as pd

#conn = sqlite3.connect(par.database_name)
#cur = conn.cursor()


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
    """records all state variables from agetns, firms, stocks and the orderbook in an SQL database"""
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


def df_update_statevariables(seed, period, agent, Statevariables, Variabletypes, Objects):
    """Records all state variables for this agent in provided Statevariable and related tables and returns them"""
    variables = vars(agent)
    varTypes, objects, statevariables = [Variabletypes], [Objects], [Statevariables]
    # store the agent and type of agent in the objects table
    if repr(agent) not in Objects['object_name'].values:
        owner_id = len(Objects) + (len(objects) - 1)
        objects.append(pd.DataFrame.from_records([(owner_id, repr(agent), repr(agent)[:repr(agent).find('_')])],
                                                 columns=Objects.columns.values))
    else:
        owner_id = list(Objects['object_name'].values).index(repr(agent))
    for variable in variables:
        # store the variable type into the variable types table
        if str(variable) not in Variabletypes['variable_type'].values:
            variable_type_id = len(Variabletypes) + (len(varTypes) - 1)
            varTypes.append(pd.DataFrame.from_records([(variable_type_id, str(variable))], columns=Variabletypes.columns.values))
        else:
            variable_type_id = list(Variabletypes['variable_type'].values).index(str(variable))
        # store the state variables
        variable_id = sum([len(x) for x in statevariables])
        statevariables.append(pd.DataFrame.from_records([(variable_id, seed, period, variable_type_id, owner_id, str(variables[variable]))], columns=Statevariables.columns.values))

    return pd.concat(statevariables, ignore_index=True), pd.concat(varTypes, ignore_index=True), pd.concat(objects, ignore_index=True)


def df_update_transactions(seed, period, buyer, seller, stock, amount_of_product, amount_of_money, Transactions, Transactors, Objects):
    transactions, transactors, objects = [Transactions], [Transactors], [Objects]
    # store the buyer in the objects table
    if repr(buyer) not in Objects['object_name'].values:
        buyer_id = len(Objects)
        objects.append(pd.DataFrame.from_records([(buyer_id, repr(buyer), repr(buyer)[:repr(buyer).find('_')])],
                                                 columns=Objects.columns.values))
    else:
        buyer_id = list(Objects['object_name'].values).index(repr(buyer))
    # store the seller in the objects table
    if repr(seller) not in Objects['object_name'].values:
        #seller_id = len(Objects)
        seller_id = sum([len(x) for x in objects])
        objects.append(pd.DataFrame.from_records([(seller_id, repr(seller), repr(seller)[:repr(seller).find('_')])],
                                                 columns=Objects.columns.values))
    else:
        seller_id = list(Objects['object_name'].values).index(repr(seller))
    # Store the stock in the objects table
    if repr(stock) not in Objects['object_name'].values:
        #stock_id = len(Objects)
        stock_id = sum([len(x) for x in objects])
        objects.append(pd.DataFrame.from_records([(stock_id, repr(stock), repr(stock)[:repr(stock).find('_')])],
                                                 columns=Objects.columns.values))
    else:
        stock_id = list(Objects['object_name'].values).index(repr(stock))
    # Store the transaction details in the Transactions Table
    transactions.append(pd.DataFrame.from_records([(len(Transactions), seed, period, amount_of_product, amount_of_money)],
                                             columns=Transactions.columns.values))
    transaction_id = len(Transactions)

    # for the transaction update the buyer, seller and type of item traded in the transactors column
    for actor_id, role in list(zip([buyer_id, seller_id, stock_id],['buyer', 'seller', 'stock'])):
        transactors.append(pd.DataFrame.from_records([(transaction_id, actor_id, role)], columns=Transactors.columns.values))

    return pd.concat(transactions, ignore_index=True), pd.concat(transactors, ignore_index=True), pd.concat(objects, ignore_index=True)


def commit():
    conn.commit()


def close():
    cur.close()
