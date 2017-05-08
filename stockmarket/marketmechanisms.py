"""In this file, we define market matching mechanism functions.
These functions take in agent sets and output matched pairs of agents"""

import math
import random
import stockmarket.parameters as par
from stockmarket.database import record_transaction

__author__ = 'Schasfoort, Abeshzadeh, Broek & Peters'


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
    # copy the agentset and shuffle the set to get different order of traders every time
    randomized_agent_set = list(agentset)
    random.shuffle(randomized_agent_set)

    # store total price and trade volume for the stock in the given period.
    total_volumn = 0
    total_money = 0

    for demander in randomized_agent_set:

        observable_set = set_of_traders_function(demander, randomized_agent_set, observablesetsize)

        trade = find_best_trade(demander, observable_set, stock)
        if trade is not None:
            transaction(demander, trade[0], stock, trade[1], trade[1] * trade[2])
            total_volumn += trade[1]
            total_money += trade[1] * trade[2]
            if par.record_data:
                record_transaction(demander, trade[0], stock, trade[1], trade[1] * trade[2], quarter)

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
    if bp is not None and sp is not None and sp <= bp:
        return min(supplier.stocks[stock], math.floor(demander.money / sp)), sp
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
