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


def overTheCounterMarket(agentset, stock, observablesetsize, set_of_traders_function, period, seed, Transactions, Transactors, Objects):
    # copy the agentset and shuffle the set to get different order of traders every time
    randomized_agent_set = list(agentset)
    random.shuffle(randomized_agent_set)

    # store total price and trade volume for the stock in the given period.
    total_volumn = 0
    total_money = 0

    for demander in randomized_agent_set:
        # create a random set of suppliers the demander can observe
        observable_set = set_of_traders_function(demander, randomized_agent_set, observablesetsize)
        # pick the cheapest supplier
        trade = find_best_trade(demander, observable_set, stock)
        # if there is a trade and the volume of that trade is bigger than zero: trade!
        if (trade is not None) and (trade[1] > 0):
            transaction(demander, trade[0], stock, trade[1], trade[1] * trade[2])
            total_volumn += trade[1]
            total_money += trade[1] * trade[2]
            Transactions, Transactors, Objects = df_update_transactions(seed, period, demander, trade[0], stock, trade[1], trade[1] * trade[2], Transactions, Transactors, Objects)

    # add average price to the stock's memory
    stock.add_price(total_volumn, total_money)

    return agentset, stock, Transactions, Transactors, Objects


def trade_stock(agentset, observablesetsize, stock, set_of_traders_function, quarter):
    # TODO
    """ ???

    Parameters
    ----------
    agentset
    observablesetsize
    stock
    set_of_traders_function
    quarter
    """
    # copy the agent set and shuffle the set to get different order of traders every time
    randomized_agent_set = list(agentset)
    random.shuffle(randomized_agent_set)

    # store total price and trade volume for the stock in the given period.
    total_volumn = 0
    total_money = 0

    for demander in randomized_agent_set:
        # create a random set of suppliers the demander can observe
        observable_set = set_of_traders_function(demander, randomized_agent_set, observablesetsize)
        # pick the cheapest supplier
        trade = find_best_trade(demander, observable_set, stock)
        # if there is a trade and the volume of that trade is bigger than zero: trade!
        if (trade is not None) and (trade[1] > 0):
            transaction(demander, trade[0], stock, trade[1], trade[1] * trade[2])
            total_volumn += trade[1]
            total_money += trade[1] * trade[2]

    stock.add_price(total_volumn, total_money)


def find_best_trade(demander, sellers, stock):
    """

    Parameters
    ----------
    demander
    sellers
    stock

    Returns
    -------
    seller : :obj:`seller`
    volume : int
    price : int

    """
    sup = best_supplier(sellers, stock)
    if sup is not None:
        vol_price = find_volume_price(demander, sup, stock)
        if vol_price is not None:
            return sup, vol_price[0], vol_price[1]
    return None


def find_volume_price(demander, supplier, stock):
    """Determines volume and price of the trade

    Parameters
    ----------
    demander : :obj:`agent`
        Buyer of the stock.
    supplier : :obj:`agent`
        Seller of the stock.
    stock : :obj:`stock`
        Stock to be traded.

    Returns
    -------
    volume : int
        Trade volume.
    price : int
        Price of trade

    """
    sp = selling_price(stock, supplier)
    bp = buying_price(stock, demander)
    if bp is not None and sp is not None and (sp <= bp and sp > 0):
        return min(supplier.stocks[stock], math.floor(np.divide(demander.money, sp))), sp
    else:
        return None


def best_supplier(suppliers, stock):
    """Returns trader with the lowest price.

    Determines the trader that sells the `stock` for the lowest price and returns it.

    Parameters
    ----------
    suppliers : :obj:`list` of :obj:`agent`
        List of potential sellers.
    stock : :obj:`stock`
        Stock to be traded.

    Returns
    -------
    :obj:`agent`
        Trader with the lowest price.
    None
        If there is no trader able to sell in the list of `suppliers`.

    """
    current_supplier = None
    current_price = None
    for supplier in suppliers:
        price = selling_price(stock, supplier)
        if price is not None and supplier.stocks[stock] > 0:
            if current_price is None or current_price > price:
                current_supplier = supplier
                current_price = price
    return current_supplier


def buying_price(stock, demander):
    """Determines maximum price an agent is willing to pay for a stock.

    Parameters
    ----------
    stock : :obj:`stock`
        Stock to be traded.
    demander : :obj:`agent`
        The buyer of the stock.

    Returns
    -------
    scalar :
        Price the `demander` is willing to buy for.
    None :
        If the `demander` doesn't have a price.

    """
    price = demander.valuate_stocks(stock)
    if price is not None:
        return demander.valuate_stocks(stock) * (1 - (demander.bid_ask_spread / 200))
    else:
        return None


def selling_price(stock, supplier):
    """Determines minimum price an agent is willing to sell a stock for.

    Parameters
    ----------
    stock : :obj:`stock`
        Stock to be traded.
    supplier : :obj:`agent`
        The seller of the stock.

    Returns
    -------
    scalar :
        Price the `supplier` is willing to sell for.
    None :
        If the `supplier` doesn't have a price.

    """
    price = supplier.valuate_stocks(stock)
    if price is not None:
        # TODO: Edge case: valuated at zero
        return supplier.valuate_stocks(stock) * (1 + (supplier.bid_ask_spread / 200))
    else:
        return None


def orders_based_on_stock_valuation(agent, orderbook, stock, agents_hold_thresholds):
    """Add orders to the orderbook based on stock valuation"""
    orderbook = copy.deepcopy(orderbook)
    price_forecast = agent.valuate_stocks(stock)
    # simultaneously submit a bid and ask based on the bid-ask spread
    bid_price = price_forecast * ((100 - agent.bid_ask_spread) / 100)
    bid_volume = int(div0(agent.money, bid_price))
    if bid_volume > 0:
        orderbook.add_bid(bid_price, bid_volume, agent)
    ask_price = price_forecast * ((100 + agent.bid_ask_spread) / 100)
    ask_volume = agent.stocks[stock]
    if ask_volume > 0:
        orderbook.add_ask(ask_price, ask_volume, agent)

    return orderbook


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
