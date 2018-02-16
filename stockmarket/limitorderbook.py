"""In this file, we define limit orderbook classes"""

import bisect
import operator
import numpy as np


class LimitOrderBook:
    """Base limit order book """
    def __init__(self, stock, last_price, order_expiration, initial_bid_ask):
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
        self.highest_bid_price = last_price - (initial_bid_ask[-1] / 100) # init bid_ask is measured in basis points
        self.highest_bid_price_history = []
        self.lowest_ask_price = last_price + (initial_bid_ask[-1] / 100) # init bid_ask is measured in basis points
        self.lowest_ask_price_history = []
        self.m_m_orders_available_after_cleaning = False
        self.sell_orders_today = 0
        self.buy_orders_today = 0
        self.sell_orders_history = []
        self.buy_orders_history = []

    def add_bid(self, price, volume, agent):
        """Add a bid to the (price low-high, age young-old) sorted bids book"""
        bisect.insort_left(self.bids, Order(order_type='b', owner=agent, price=price, volume=volume))
        self.update_bid_ask_spread('bid')

    def add_ask(self, price, volume, agent):
        """Add an ask to the (price low-high, age old-young) sorted asks book"""
        bisect.insort_right(self.asks, Order(order_type='a', owner=agent, price=price, volume=volume))
        self.update_bid_ask_spread('ask')

    def clean_book(self):
        """Increase age of orders and clean those past their expiration date"""
        self.m_m_orders_available_after_cleaning = True
        new_bids = []
        for bid in self.bids:
            bid.age += 1
            if bid.age < self.order_expiration:
                new_bids.append(bid)
            else:
                # notify the owner of that bid that it no longer has an order in the market
                bid.owner.order_in_market = False

        new_asks = []
        for ask in self.asks:
            ask.age += 1
            if ask.age < self.order_expiration:
                new_asks.append(ask)
            else:
                # notify the owner of that bid that it no longer has an order in the market
                ask.owner.order_in_market = False

        self.bids = new_bids
        self.asks = new_asks
        # update current highest bid and lowest ask
        for order_type in ['bid', 'ask']:
            self.update_bid_ask_spread(order_type)

    def cleanse_book(self):
        """
        store and clean unresolved orders
        :return: None
        """
        if len(self.transaction_prices):
            self.transaction_prices_history.append(self.transaction_prices)
        self.transaction_prices = []
        # store and clean recorded transaction volumes
        self.transaction_volumes_history.append(self.transaction_volumes)
        self.transaction_volumes = []
        # store and clean matched bids
        self.matched_bids_history.append(self.matched_bids)
        self.matched_bids = []
        # record the total bids and asks submitted that day
        self.buy_orders_history.append(self.buy_orders_today)
        self.buy_orders_today = 0
        self.sell_orders_history.append(self.sell_orders_today)
        self.sell_orders_today = 0
        # in this model not all orders are deleted at the end of the day
        #self.bids = []
        #self.asks = []

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
                # notify owner it no longer has an order in the market
                for order in [winning_bid, winning_ask]:
                    order.owner.order_in_market = False
                # remove these elements from list
                del self.bids[-1]
                del self.asks[0]
                # update current highest bid and lowest ask
                for order_type in ['bid', 'ask']:
                    self.update_bid_ask_spread(order_type)
            else:
                # decrease volume for both bid and ask
                self.asks[0].volume -= volume
                self.bids[-1].volume -= volume
                # delete the empty bid or ask
                if min_index == 0:
                    if 'maker' in repr(self.bids[-1].owner):
                        market_maker_orders_available = (False, 'bid')
                    self.bids[-1].owner.order_in_market = False
                    del self.bids[-1]
                    # update current highest bid
                    self.update_bid_ask_spread('bid')
                else:
                    if 'maker' in repr(self.asks[0].owner):
                        market_maker_orders_available = (False, 'ask')
                    self.asks[0].owner.order_in_market = False
                    del self.asks[0]
                    # update lowest ask
                    self.update_bid_ask_spread('ask')
            self.transaction_prices.append(price)
            self.transaction_volumes.append(volume)
            self.matched_bids.append((winning_bid, winning_ask))

            return price, volume, winning_bid, winning_ask, market_maker_orders_available[0]

    def update_bid_ask_spread(self, order_type):
        """update the current highest bid or lowest ask and store previous values"""
        if ('ask' not in order_type) and ('bid' not in order_type):
            raise ValueError("unknown order_type")

        if order_type == 'ask' and self.asks:
            self.lowest_ask_price_history.append(self.lowest_ask_price)
            self.lowest_ask_price = self.asks[0].price
        if order_type == 'bid' and self.bids:
            self.highest_bid_price_history.append(self.highest_bid_price)
            self.highest_bid_price = self.bids[-1].price

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
