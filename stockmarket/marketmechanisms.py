"""In this file, we define market matching mechanism functions.
These functions take in agent sets and output matched pairs of agents"""

import math
import random
from stockmarket.database import df_update_transactions
from stockmarket.functions import div0
import numpy as np
import copy


def continuous_double_auction(market_maker, agentset, stock, orderbook, valuation_type_function, agents_hold_thresholds):
    """
    Agent, bids and asks are continuously submitted to the limit-order book. The resulting trades are executed.
    """
    # copy the agent set and shuffle the set to get different order of traders every time
    randomized_agent_set = list(agentset)
    random.shuffle(randomized_agent_set)

    # store total price and trade volume for the stock in the given period.
    total_volume = 0
    total_money = 0

    # establish the current price
    if len(orderbook.transaction_prices):
        current_price = (orderbook.transaction_prices[-1])[-1]
    elif len(orderbook.transaction_prices_history):
        current_price = (orderbook.transaction_prices_history[-1])[-1]
    else:
        current_price = stock.price_history[-1]

    # 2 Ask market maker to contribute initial bid and asks
    def add_market_maker_orders():
        market_maker_bid_price, market_maker_ask_price = market_maker.determine_spread(current_price=current_price, stock=stock)

        maker_bid_volume = min(market_maker.standard_order_size, int(div0(market_maker.money, market_maker_bid_price)))
        if maker_bid_volume > 0 and market_maker_bid_price > 0:
            orderbook.add_bid(market_maker_bid_price, maker_bid_volume, market_maker)

        maker_ask_volume = min(market_maker.standard_order_size, market_maker.stocks[stock])
        if maker_ask_volume > 0 and market_maker_ask_price > 0:
            orderbook.add_ask(market_maker_ask_price, maker_ask_volume, market_maker)

    add_market_maker_orders()
    market_maker_orders_available = True

    # 3 Continuous double auction trading
    for agent in randomized_agent_set:
        # add orders to the orderbook according to the type of valuation function
        buy_or_sell, price, volume = valuation_type_function(agent, orderbook, stock, agents_hold_thresholds)

        if volume > 0 and price > 0:
            if buy_or_sell == 'buy':
                orderbook.add_bid(price, volume, agent)
                orderbook.buy_orders_today += 1
            elif buy_or_sell == 'sell':
                orderbook.add_ask(price, volume, agent)
                orderbook.sell_orders_today += 1

        while True:
            matched_orders = orderbook.match_orders()
            if matched_orders is None:
                break
            # execute trade
            transaction(matched_orders[2].owner, matched_orders[3].owner ,stock,
                        matched_orders[1],
                        matched_orders[0] * matched_orders[1])
            total_volume += matched_orders[1]
            total_money += matched_orders[0] * matched_orders[1]
            # if the market maker orders where not depleted
            market_maker_orders_available = matched_orders[4]
            if not market_maker_orders_available:
                add_market_maker_orders()
                market_maker_orders_available = True
        # clean limit order book and check whether there are still market maker orders
        orderbook.clean_book()
        market_maker_orders_available_after_cleaning = orderbook.m_m_orders_available_after_cleaning
        if not market_maker_orders_available_after_cleaning:
            add_market_maker_orders()
            market_maker_orders_available = True

    # add average price to the stock's memory
    stock.add_price(total_volume, total_money)
    if total_volume <= 0:
        print('no volume')
    # at the end of the day, cleanse the order-book
    orderbook.cleanse_book()
    #market_maker_orders_available = True

    return agentset, stock, orderbook


def orders_based_on_sentiment_and_fundamentals(agent, orderbook, stock, agents_hold_thresholds):
    """Add orders to the orderbook based on stock price movement and deviation from fundamentals"""
    price = 0
    volume = 0
    # 1 establish the current price
    if len(orderbook.transaction_prices):
        current_price = orderbook.transaction_prices[-1]
    elif len(orderbook.transaction_prices_history):
        current_price = (orderbook.transaction_prices_history[-1])[-1]
    else:
        current_price = stock.price_history[-1]

    # determine wether to buy or sell suing the agents strategy
    price_series = stock.price_history + [current_price]
    buy_or_sell = agent.buy_sell_or_hold(price_series, shortMA=agent.ma_short, longMA=agent.ma_long,
                                             upper_threshold=agents_hold_thresholds[1],
                                             lower_threshold=agents_hold_thresholds[0])
    # 3 Determine price and volume of the order
    if buy_or_sell == 'buy':
        # bid price is above the max(lowest ask, last_price)
        lowest_ask_price = orderbook.lowest_ask_price
        price = max(current_price, lowest_ask_price) * ((100 + agent.bid_ask_spread) / 100)
        volume = int( int(div0(agent.money, price)) * agent.volume_risk_aversion)
    elif buy_or_sell == 'sell':
        # ask price is below the min(highest bid or current price)
        highest_bid_price = orderbook.highest_bid_price
        price = min(current_price, highest_bid_price) * ((100 - agent.bid_ask_spread) / 100)
        volume = int(agent.stocks[stock] * agent.volume_risk_aversion)

    return buy_or_sell, price, volume


def transaction(buyer, seller, stock, amount_of_product, amount_of_money):
    """Perform transaction between buyer and seller.

    Parameters
    ----------
    buyer : :obj:`agent`
        Trader that buys the stock.
    seller : :obj:`agent`
        Trader that sells the stock.
    stock : :obj:`stock`
        The stock to be sold.
    amount_of_product : int
        Number of stocks sold.
    amount_of_money : scalar
        Total price for all stocks.
    quarter :
        The quarter the transaction occurs

    """
    seller.sell(stock, amount_of_product, amount_of_money)
    buyer.buy(stock, amount_of_product, amount_of_money)
