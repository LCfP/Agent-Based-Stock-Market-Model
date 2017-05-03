"""In this file, we define the benchmark stock market model agent classes"""


class Trader:
    """a base class for Traders"""
    def __init__(self, name, money, bid_ask_spread, memory, function):
        """Creates a new trader"""
        self.name = name
        self.money = money
        self.stocks = StockDict()
        # bid ask spread is an integer
        self.memory_size = memory
        self.bid_ask_spread = bid_ask_spread
        self.function = function

    def valuate_stocks(self, stock):
        return self.function(stock=stock, memory=self.memory_size)

    def sell(self, stock, amount, price):
        if self.stocks[stock] < amount:
            raise ValueError("not enough stocks to sell this amount")
        self.stocks[stock] -= amount
        self.money += price

    def buy(self, stock, amount, price):
        if self.money < price:
            raise ValueError("not enough money to buy this amount of stocks")
        try:
            self.stocks[stock] += amount
        except KeyError:
            self.stocks[stock] = amount
        self.money -= price

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return "trader_" + str(self.name)

    def show(self):
        print("Name:", self.name)
        print("Money:", self.money)
        print("Stocks:", self.stocks)
        print("")


class StockDict(dict):
    def __getitem__(self, key):
        try:
            return self.__dict__[key]
        except KeyError:
            return 0

    def __setitem__(self, key, value):
        self.__dict__[key] = value
