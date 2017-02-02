"""In this file, we provide functions for creating and updating the database"""
import sqlite3
import time

def create_tables(cur):
    cur.executescript('''
    DROP TABLE IF EXISTS Transactions;
    DROP TABLE IF EXISTS Statevariables;
    DROP TABLE IF EXISTS Variabletypes;
    DROP TABLE IF EXISTS Objects;
    DROP TABLE IF EXISTS Experiments;

    CREATE TABLE Transactions (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        unix_time REAL UNIQUE,
        experiment_id INTEGER,
        seed INTEGER,
        period INTEGER,
        amount_of_product REAL,
        amount_of_money REAL,
        buyer_id INTEGER,
        seller_id INTEGER,
        stock_id INTEGER
    );

    CREATE TABLE Statevariables (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        experiment_id INTEGER,
        seed INTEGER,
        period INTEGER,
        variable_type TEXT,
        owner_id TEXT,
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

def write_to_statevariables(cur, experiment_id, seed, period, agentSets=[]):
    """Writes all variables of all agents in the dataset to the Statevariables table"""
    for agentSet in agentSets:
        for agent in agentSet:
            variables = vars(agent)
            for variable in variables:
                cur.execute("INSERT INTO Statevariables (unix_time, experiment_id, seed, period, variable_type, owner_id, value) VALUES (?,?,?,?,?,?,?)",
                            (time.time(), experiment_id, seed, period, str(variable), repr(agent), str(variables[variable])))
                time.sleep(1)

def record_statevariables(cur, experiment_id, seed, period, agent, record=True):
    """Records all state variables for this agent in the Statevariables table"""
    if record:
        variables = vars(agent)
        for variable in variables:
            cur.execute("INSERT INTO Statevariables (experiment_id, seed, period, variable_type, owner_id, value) VALUES (?,?,?,?,?,?)",
                    ( experiment_id, seed, period, str(variable), repr(agent), str(variables[variable])))