"""In this file, we provide functions for creating and updating the database"""

import sqlite3
import pandas as pd
import stockmarket.parameters as par

conn = sqlite3.connect(par.database_name)
cur = conn.cursor()

def stockMarketBaselineTables():
    Transactions = pd.DataFrame(columns= ['id', 'seed', 'period', 'amount_of_product', 'amount_of_money'])
    Transactors = pd.DataFrame(columns= ['transaction_id', 'transactor_id', 'role'])
    Statevariables = pd.DataFrame(columns= ['id', 'seed', 'period', 'variable_id', 'owner_id', 'value'])
    Variabletypes = pd.DataFrame(columns=['id', 'variable_type'])
    Objects = pd.DataFrame(columns=['id', 'object_name', 'object_type'])
    Experiments = pd.DataFrame(columns=['id', 'object_name', 'object_type'])
    return Transactions, Transactors, Statevariables, Variabletypes, Objects, Experiments

def create_tables():
    cur.executescript('''
    DROP TABLE IF EXISTS Transactions;
    DROP TABLE IF EXISTS Statevariables;
    DROP TABLE IF EXISTS Variabletypes;
    DROP TABLE IF EXISTS Objects;
    DROP TABLE IF EXISTS Experiments;
    DROP TABLE IF EXISTS Transactors;

    CREATE TABLE Transactions (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        experiment_id INTEGER,
        seed INTEGER,
        period INTEGER,
        amount_of_product REAL,
        amount_of_money REAL
    );

    CREATE TABLE Transactors(
        transaction_id INTEGER NOT NULL,
		transactor_id INTEGER NOT NULL,
		role REAL,
		PRIMARY KEY (transaction_id, transactor_id)
    );

    CREATE TABLE Statevariables (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        experiment_id INTEGER,
        seed INTEGER,
        period INTEGER,
        variable_id INTEGER,
        owner_id INTEGER,
        value REAL
    );

    CREATE TABLE Variabletypes (
        id  INTEGER NOT NULL PRIMARY KEY
            AUTOINCREMENT UNIQUE,
        variable_type TEXT  UNIQUE
    );

    CREATE TABLE Objects (
        id  INTEGER NOT NULL PRIMARY KEY
            AUTOINCREMENT UNIQUE,
        object_name TEXT  UNIQUE,
        object_type TEXT
    );

    CREATE TABLE Experiments (
        id  INTEGER NOT NULL PRIMARY KEY
            AUTOINCREMENT UNIQUE,
        experiment TEXT  UNIQUE,
        parameter_space TEXT
    );

    ''')

def df_update_statevariables(seed, period, agent, Statevariables, Variabletypes, Objects):
    """Records all state variables for this agent in provided Statevariable and related tables and returns them"""
    variables = vars(agent)
    varTypes, objects, statevariables = [Variabletypes], [Objects], [Statevariables]
    for variable in variables:
        # store the variable type into the variabletypes table
        if str(variable) not in Variabletypes['variable_type'].values:
            variable_type_id = len(Variabletypes) + (len(varTypes) - 1)
            varTypes.append(pd.DataFrame.from_records([(variable_type_id, str(variable))], columns=Variabletypes.columns.values))
            #Variabletypes.loc[variable_type_id] = [variable_type_id, str(variable)]
        else:
            variable_type_id = list(Variabletypes['variable_type'].values).index(str(variable))
        # store the agent and type of agent in the objects table
        if repr(agent) not in Objects['object_name'].values:
            owner_id = len(Objects) + (len(objects) - 1)
            objects.append(pd.DataFrame.from_records([(owner_id, repr(agent), repr(agent)[:repr(agent).find('_')])], columns=Objects.columns.values))
            #Objects.loc[owner_id] = owner_id, repr(agent), repr(agent)[:repr(agent).find('_')]
        else:
            owner_id = list(Objects['object_name'].values).index(repr(agent))
        # store the state variables
        statevariables.append(pd.DataFrame.from_records([(len(Statevariables), seed, period, variable_type_id, owner_id, str(variables[variable]))], columns=Statevariables.columns.values))

        #Statevariables.loc[len(Statevariables)] = len(Statevariables), seed, period, variable_type_id, owner_id, str(variables[variable])

    return pd.concat(statevariables, ignore_index=True), pd.concat(varTypes, ignore_index=True), pd.concat(objects, ignore_index=True)

def record_statevariables(period, agent):
    """Records all state variables for this agent in the Statevariable and related tables"""
    variables = vars(agent)
    for variable in variables:
        # store the variable type into the variabletypes table
        cur.execute("INSERT OR IGNORE INTO Variabletypes (variable_type) VALUES (?)", (str(variable), ))
        cur.execute("SELECT id FROM Variabletypes WHERE variable_type = ?", (str(variable),))
        variable_type_id = cur.fetchone()[0]

        # store the agent and type of agent in the objects table
        cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)", (repr(agent), repr(agent)[:repr(agent).find('_')]))
        cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(agent),))
        owner_id = cur.fetchone()[0]

        # store the state variables in the state variables table
        cur.execute("INSERT INTO Statevariables (experiment_id, seed, period, "
                    "variable_id, owner_id, value) VALUES (?,?,?,?,?,?)",
                    (par.experiment_id, par.seed, period, variable_type_id, owner_id, str(variables[variable])))

def df_update_transactions(seed, period, buyer, seller, stock, amount_of_product, amount_of_money, Transactions, Transactors, Objects):
    transactions, transactors, objects = [Transactions], [Transactors], [Objects]
    # store the buyer in the objects table
    if repr(buyer) not in Objects['object_name'].values:
        buyer_id = len(Objects)
        objects.append(pd.DataFrame.from_records([(buyer_id, repr(buyer), repr(buyer)[:repr(buyer).find('_')])],
                                                 columns=Objects.columns.values))
        #Objects.loc[buyer_id] = buyer_id, repr(buyer), repr(buyer)[:repr(buyer).find('_')]
    else:
        buyer_id = list(Objects['object_name'].values).index(repr(buyer))
    # store the seller in the objects table
    if repr(seller) not in Objects['object_name'].values:
        seller_id = len(Objects)
        objects.append(pd.DataFrame.from_records([(seller_id, repr(seller), repr(seller)[:repr(seller).find('_')])],
                                                 columns=Objects.columns.values))
        #Objects.loc[seller_id] = seller_id, repr(seller), repr(seller)[:repr(seller).find('_')]
    else:
        seller_id = list(Objects['object_name'].values).index(repr(seller))
    # Store the stock in the objects table
    if repr(stock) not in Objects['object_name'].values:
        stock_id = len(Objects)
        objects.append(pd.DataFrame.from_records([(stock_id, repr(stock), repr(stock)[:repr(stock).find('_')])],
                                                 columns=Objects.columns.values))
        #Objects.loc[stock_id] = stock_id, repr(stock), repr(stock)[:repr(stock).find('_')]
    else:
        stock_id = list(Objects['object_name'].values).index(repr(stock))
    # Store the transaction details in the Transactions Table
    transactions.append(pd.DataFrame.from_records([(len(Transactions), seed, period, amount_of_product, amount_of_money)],
                                             columns=Transactions.columns.values))
    #Transactions.loc[len(Transactions)] = len(Transactions), seed, period, amount_of_product, amount_of_money
    transaction_id = len(Transactions)

    # for the transaction update the buyer, seller and type of item traded in the transactors column
    for actor_id, role in list(zip([buyer_id, seller_id, stock_id],['buyer', 'seller', 'stock'])):
        transactors.append(pd.DataFrame.from_records([(transaction_id, actor_id, role)], columns=Transactors.columns.values))
        #Transactors.loc[len(Transactors)] = transaction_id, actor_id, role

    return pd.concat(transactions, ignore_index=True), pd.concat(transactors, ignore_index=True), pd.concat(objects, ignore_index=True)


def record_transaction(buyer, seller, stock, amount_of_product, amount_of_money, quarter):
    # store the buyer in the objects table
    cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)",
                (repr(buyer), repr(buyer)[:repr(buyer).find('_')]))
    cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(buyer),))
    buyer_id = cur.fetchone()[0]

    # store the seller in the objects table
    cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)",
                (repr(seller), repr(seller)[:repr(seller).find('_')]))
    cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(seller),))
    seller_id = cur.fetchone()[0]

    # Store the stock in the objects table
    cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)",
                (repr(stock), repr(stock)[:repr(stock).find('_')]))
    cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(stock),))
    stock_id = cur.fetchone()[0]

    # Store the transaction details in the Transactions Table
    cur.execute("INSERT INTO Transactions (experiment_id, seed, period, amount_of_product, "
                "amount_of_money) VALUES (?,?,?,?,?)",
                (par.experiment_id, par.seed, quarter,
                 amount_of_product, amount_of_money))
    cur.execute("SELECT MAX(id) FROM Transactions")
    transaction_id = cur.fetchone()[0]

    cur.execute("INSERT OR IGNORE INTO Transactors (transaction_id, transactor_id, role) VALUES (?,?,?)",
                (transaction_id, buyer_id, 'buyer'))
    cur.execute("INSERT OR IGNORE INTO Transactors (transaction_id, transactor_id, role) VALUES (?,?,?)",
                (transaction_id, seller_id, 'seller'))
    cur.execute("INSERT OR IGNORE INTO Transactors (transaction_id, transactor_id, role) VALUES (?,?,?)",
                (transaction_id, stock_id, 'stock'))


def commit():
    conn.commit()


def close():
    cur.close()
