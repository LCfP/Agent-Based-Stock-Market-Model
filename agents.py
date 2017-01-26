"""In this file, we define the benchmark stock market model agent classes"""

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


class Trader:
    """a base class for Traders"""
    def __init__(self, name, money, bid_ask_spread, memory_size):
        """Creates a new trader"""
        self.name = name
        self.money = money
        self.stocks = {}
        # bid ask spread is an integer
        self.bid_ask_spread = bid_ask_spread
        self.memory_size = memory_size

    def valuate_stocks(self, stock, valuation_function):
        # TODO test this function
        npv_firm = valuation_function(self.memory_size, stock.firm)
        # evaluate the below calculation (currently additional stocks dilute value directly)
        stock_value = npv_firm / (stock.firm.bookvalue / stock.facevalue)
        return stock_value
    
    def transact(self, inflow_item, inflow_amount, outflow_item, outflow_amount):
        """This allows an agent to transact stocks and money"""
        if (inflow_item == "stocks") & (outflow_item == "money") & (outflow_amount <= self.money):
            self.stocks += inflow_amount
            self.money -= outflow_amount
            print (self, "I just purchased stocks")  # for debugging purposes
        elif (inflow_item == "money") & (outflow_item == "stocks") & (outflow_amount <= self.stocks):
            self.money += inflow_amount
            self.stocks -= outflow_amount
            print (self, "I just sold stocks")
        else: 
            print ("No transaction possible ")

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)
