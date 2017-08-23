"""In this file, we define the benchmark stock market model agent classes"""

from stockmarket.functions import div0

class Marketmaker:
    """a base class for Traders"""
    def __init__(self, name, money, bid_ask_spread, price_to_earnings_window, inventory_sensitivity,
                 inventory_buffer_target, standard_order_size):
        """Creates a new market maker"""
        self.name = name
        self.money = money
        self.money_history = [money]
        self.stocks = StockDict()
        self.portfolio_history = []
        self.portfolio_value_history = [0]
        # bid ask spread is measured in basis points
        self.bid_ask_spread = bid_ask_spread / 100
        self.return_on_assets = []
        self.price_to_earnings_window = price_to_earnings_window
        self.inventory_sensitivity = inventory_sensitivity
        self.inventory_buffer_target = inventory_buffer_target
        self.standard_order_size = standard_order_size

    def determine_spread(self, current_price, stock):
        """

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
        inventory = self.stocks[stock]
        inventory_deviation_from_target = inventory - self.inventory_buffer_target
        inventory_mark_up_factor = self.inventory_sensitivity * div0(abs(inventory_deviation_from_target), self.inventory_buffer_target)
        if inventory_deviation_from_target > 0:
            multiplication_factor = 1 - inventory_mark_up_factor
        else:
            multiplication_factor = 1 + inventory_mark_up_factor
        core_price = current_price * multiplication_factor
        bid_price = core_price - self.bid_ask_spread
        ask_price = core_price + self.bid_ask_spread
        return bid_price, ask_price

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
