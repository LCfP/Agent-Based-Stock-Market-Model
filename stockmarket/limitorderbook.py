"""In this file, we define limit orderbook classes"""

import bisect
import operator


class LimitOrderBook:
    """Base limit order book """
    def __init__(self, stock, last_price, order_expiration):
        """Creates a new trader"""
        self.stock = stock
        self.transaction_prices = []
        self.transaction_volumes = []
        self.matched_bids = []
        self.order_expiration = order_expiration
        self.bids = []
        self.asks = []
        self.unresolved_orders_history = []
        self.transaction_prices_history = []
        self.transaction_volumes_history = []
        self.matched_bids_history = []

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
        # store and clean unresolved orders
        self.unresolved_orders_history.append((self.bids, self.asks))
        self.bids = []
        self.asks = []
        # store and clean recorded transaction prices
        if len(self.transaction_prices):
            self.transaction_prices_history.append(self.transaction_prices)
        self.transaction_prices = []
        # store and clean recorded transaction volumes
        self.transaction_volumes_history.append(self.transaction_volumes)
        self.transaction_volumes = []
        # store and clean matched bids
        self.matched_bids_history.append(self.matched_bids)
        self.matched_bids = []


    def match_orders(self):
        """Return a price, volume, bid and ask and delete them from the order book if volume of either reaches zero"""
        market_maker_orders_available = (True, None)
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
                # TODO check if a bid or ask was from a market_maker
                bid_or_ask = [repr(self.bids[-1].owner), repr(self.asks[-1].owner)]
                for idx, order in enumerate(bid_or_ask):
                    legend = ['bid', 'ask']
                    if 'maker' in order:
                        market_maker_orders_available = (False, legend[idx])
                # remove these elements from list
                del self.bids[-1]
                del self.asks[0]
            else:
                # decrease volume for both bid and ask
                self.asks[0].volume -= volume
                self.bids[-1].volume -= volume
                # delete the empty bid or ask
                if min_index == 0:
                    if 'maker' in repr(self.bids[-1].owner):
                        market_maker_orders_available = (False, 'bid')
                    del self.bids[-1]
                else:
                    if 'maker' in repr(self.asks[0].owner):
                        market_maker_orders_available = (False, 'ask')
                    del self.asks[0]
            self.transaction_prices.append(price)
            self.transaction_volumes.append(volume)
            self.matched_bids.append((winning_bid, winning_ask))

            def find_market_maker_order(book):
                for idx, bid in enumerate(book):
                    if 'maker' in repr(bid.owner):
                        return idx

            # if one of the market maker orders was depleted, look for the other and delete it.
            if market_maker_orders_available[1] == 'bid':
                i = find_market_maker_order(self.bids)
                if i is not None:
                    del self.bids[i]
            if market_maker_orders_available[1] == 'ask':
                i = find_market_maker_order(self.asks)
                if i is not None:
                    del self.asks[i]

            return price, volume, winning_bid, winning_ask, market_maker_orders_available[0]

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
