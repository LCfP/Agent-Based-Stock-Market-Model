"""In this file, we define the benchmark stock market model agent classes"""
from stockmarket import switchingstrategies

class Trader:
    """a base class for Traders"""
    def __init__(self, name, money, bid_ask_spread, memory, ma_short, ma_long, valuation_function, propensity_to_switch,
                 switching_strategy=switchingstrategies.adaptive_switching,
                 ):
        """Creates a new trader"""
        self.name = name
        self.money = money
        self.money_history = [money]
        self.stocks = StockDict()
        self.portfolio_history = []
        self.portfolio_value_history = [0]
        self.memory_size = memory
        # bid ask spread is measured in basis points
        self.bid_ask_spread = bid_ask_spread / 100
        self.function = valuation_function
        self.function_history = []
        self.ma_short = ma_short
        self.ma_long = ma_long
        self.switching_strategy = switching_strategy
        self.propensity_to_switch = propensity_to_switch
        self.return_on_assets = []

    def valuate_stocks(self, stock):
        """Returns value of a stock.

        Returns the value the Trader thinks `stock` has.

        Parameters
        ----------
        stock : :obj:`stock`
            Stock to be valuated.

        Returns
        -------
        scalar
            The value of `stock`.

        """
        # calls valuation function currently assigned to the Trader.
        return self.function(stock=stock, memory=self.memory_size, s=self.ma_short, l=self.ma_long)

    def sell(self, stock, amount, price):
        """Sells stocks

        Sells `amount` of stocks for a total of `price`

        Parameters
        ----------
        stock : :obj:`stock`
            Stock that is sold.
        amount : int
            Number of stocks sold.
        price : scalar
            Total price for stocks.

        Raises
        ------
        ValueError
            If `amount` is higher than the amount of `stock` hold by `self`.

        """
        if self.stocks[stock] < amount:
            raise ValueError("not enough stocks to sell this amount")
        self.stocks[stock] -= amount
        self.money += price

    def buy(self, stock, amount, money):
        """Buys stocks

        Parameters
        ----------
        stock : :obj:`stock`
            Stock that is bought.
        amount : int
            Number of stocks bought.
        price : scalar
            Total price for stocks.

        Raises
        ------
        ValueError
            If `price` is higher than money of `self`.

        """
        if self.money < money:
            raise ValueError("not enough money to buy this amount of stocks")
        try:
            self.stocks[stock] += amount
        except KeyError:
            self.stocks[stock] = amount
        self.money -= money

    def update_strategy(self, market_return):
        self.function = self.switching_strategy(self, self.propensity_to_switch,
                                                self.return_on_assets[-1], market_return)

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
    """A dictionary that returns 0 when key doesn't exist"""
    def __missing__(self, key):
        return 0
