"""In this file, we define limit orderbook classes"""

import bisect

class LimitOrderBook:
    """Base limit order book """
    def __init__(self, stock, last_price, order_expiration):
        """Creates a new trader"""
        self.stock = stock
        self.last_price = last_price
        self.order_expiration = order_expiration
        self.bids = []
        self.asks = []

    def add_bid(self, price, volume, agent):
        """Add a bid to the (price low-high, age young-old) sorted bids book"""
        bisect.insort_left(self.bids, Order(order_type='b', owner=agent, price=price, volume=volume))

    def add_ask(self, price, volume, agent):
        """Add an ask to the (price low-high, age old-young) sorted asks book"""
        bisect.insort_right(self.asks, Order(order_type='a', owner=agent, price=price, volume=volume))

    def clean_book(self):
        """Increase age of orders and clean those past their expiration date"""
        new_bids = []
        for idx, bid in enumerate(self.bids):
            bid.age += 1
            if bid.age < self.order_expiration:
                new_bids.append(bid)

        new_asks = []
        for idx, ask in enumerate(self.asks):
            ask.age += 1
            if ask.age < self.order_expiration:
                new_asks.append(ask)

        self.bids = new_bids
        self.asks = new_asks

    def match_orders(self):
        """Return two bids for a possible transaction and delete them from the order book"""
        # check if either bids or asks is empty
        if not (self.bids or self.asks):
            return None
        # match highest bid with lowest ask
        if self.bids[-1].price >= self.asks[0].price:
            winningBid = self.bids[-1]
            winningAsk = self.asks[0]
            # remove these elements from list
            del self.bids[-1]
            del self.asks[0]
            return winningBid, winningAsk

    def __repr__(self):
        return "order_book_{}".format(self.stock)

class Order:
    """The order class can represent both bid or ask type orders"""
    def __init__(self, order_type, owner, price, volume):
        """order_type = 'b' for bid or 'a' for ask"""
        self.order_type = order_type
        self.owner = owner
        self.price = price
        self.volume = volume
        self.age = 0

    def __lt__(self, other):
        """Allows comparison to other orders based on price"""
        return self.price < other.price

    def __repr__(self):
        return 'Order_p={}_t={}_o={}_a={}'.format(self.price, self.order_type, self.owner, self.age)