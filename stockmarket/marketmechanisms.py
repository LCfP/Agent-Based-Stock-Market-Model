"""In this file, we define market matching mechanism functions.
These functions take in agent sets and output matched pairs of agents"""

import math
import random
from stockmarket.database import df_update_transactions
from stockmarket.functions import div0
import numpy as np
import copy


def continuous_double_auction(agentset, stock, orderbook, valuation_type_function, agents_hold_thresholds, order_variability):
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

    # 3 Continuous double auction trading
    for agent in randomized_agent_set:
        # add orders to the orderbook according to the type of valuation function
        if not agent.order_in_market:
            buy_or_sell, price, volume = valuation_type_function(agent, orderbook, stock, agents_hold_thresholds, order_variability)

            if volume > 0 and price > 0:
                if buy_or_sell == 'buy':
                    agent.order_in_market = True
                    orderbook.add_bid(price, volume, agent)
                    orderbook.buy_orders_today += 1
                elif buy_or_sell == 'sell':
                    orderbook.add_ask(price, volume, agent)
                    orderbook.sell_orders_today += 1
                    agent.order_in_market = True

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

        # clean limit order book and check whether there are still market maker orders
        orderbook.clean_book()

    # add average price to the stock's memory
    stock.add_price(total_volume, total_money)
    if total_volume <= 0:
        print('no volume')
    # at the end of the day, cleanse the order-book
    orderbook.cleanse_book()

    return agentset, stock, orderbook


def orders_based_on_sentiment_and_fundamentals(agent, orderbook, stock, agents_hold_thresholds, order_variability):
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
    #
    lowest_ask_price = orderbook.lowest_ask_price
    highest_bid_price = orderbook.highest_bid_price
    bid_ask_spread = lowest_ask_price - highest_bid_price
    # TODO replace point5 with a parameter
    sigma = order_variability * bid_ask_spread if bid_ask_spread > 0 else order_variability * agent.bid_ask_spread

    # 3 Determine price and volume of the order
    if buy_or_sell == 'buy':
        # bid price is around the max(lowest ask, last_price)
        #reference_price = max(current_price, lowest_ask_price)
        price = np.random.normal(lowest_ask_price, sigma)
        volume = int( int(div0(agent.money, price)) * agent.volume_risk_aversion)
    elif buy_or_sell == 'sell':
        # ask price is around the min(highest bid or current price)
        #reference_price = min(current_price, highest_bid_price)
        price = np.random.normal(highest_bid_price, sigma)
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
