"""In this file, we define limit orderbook classes"""

import bisect
import operator

class LimitOrderBook:
    """Base limit order book """
    def __init__(self, stock, last_price, order_expiration):
        """Creates a new trader"""
        self.stock = stock
        self.transaction_prices = [last_price]
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
        for bid in self.bids:
            bid.age += 1
            if bid.age < self.order_expiration:
                new_bids.append(bid)

        new_asks = []
        for ask in self.asks:
            ask.age += 1
            if ask.age < self.order_expiration:
                new_asks.append(ask)

        self.bids = new_bids
        self.asks = new_asks

    def cleanse_book(self):
        self.bids = []
        self.asks = []

    def match_orders(self):
        """Return a price, volume, bid and ask and delete them from the order book if volume of either reaches zero"""
        # first make sure that neither the bids or asks books are empty
        if not (self.bids and self.asks):
            return None
        # then match highest bid with lowest ask
        if (self.bids[-1].price >= self.asks[0].price):
            winning_bid = self.bids[-1]
            winning_ask = self.asks[0]
            price = winning_ask.price
            # volume is the min of the bid and ask, # both bid and ask are then reduced by that volume, if 0, then removed
            min_index, volume = min(enumerate([winning_bid.volume, winning_ask.volume]), key=operator.itemgetter(1))
            if winning_bid.volume == winning_ask.volume:
                # remove these elements from list
                del self.bids[-1]
                del self.asks[0]
            else:
                # decrease volume for both bid and ask
                self.asks[0].volume -= volume
                self.bids[-1].volume -= volume
                # delete the empty bid or ask
                if min_index == 0:
                    del self.bids[-1]
                else:
                    del self.asks[0]
                #del [self.bids[-1], self.asks[0]][min_index]
            self.transaction_prices.append(price)
            return price, volume, winning_bid, winning_ask

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