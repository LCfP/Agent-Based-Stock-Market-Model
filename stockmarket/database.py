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


def record_statevariables(cur, experiment_id, seed, period, agent):
    """Records all state variables for this agent in the Statevariable and related tables"""
    variables = vars(agent)
    for variable in variables:
        # store the variable type into the variabletypes table
        cur.execute("INSERT OR IGNORE INTO Variabletypes (variable_type) VALUES (?)", (str(variable), ))
        cur.execute("SELECT id FROM Variabletypes WHERE variable_type = ?", (str(variable),))
        variable_type = cur.fetchone()[0]

        # store the agent and type of agent in the objects table
        cur.execute("INSERT OR IGNORE INTO Objects (object_name, object_type) VALUES (?,?)", (repr(agent), repr(agent)[:repr(agent).find('_')]))
        cur.execute("SELECT id FROM Objects WHERE object_name = ?", (repr(agent),))
        owner_id = cur.fetchone()[0]

        cur.execute("INSERT INTO Statevariables (experiment_id, seed, period, "
                    "variable_type, owner_id, value) VALUES (?,?,?,?,?,?)",
                    ( experiment_id, seed, period, variable_type, owner_id, str(variables[variable])))