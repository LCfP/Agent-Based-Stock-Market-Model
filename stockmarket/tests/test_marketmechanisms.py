"""This file runs tests for all functions in marketmechanisms"""

import pytest
from numpy.testing import assert_equal
from numpy.testing import assert_almost_equal
from stockmarket.marketmechanisms import *
from stockmarket.agent import *
from stockmarket.firms import *
from stockmarket.stock import Stock
from stockmarket.setup import distribute_initial_stocks
from stockmarket.valuationfunctions import extrapolate_average_profit
from stockmarket.valuationfunctions import extrapolate_ma_price
from stockmarket.limitorderbook import LimitOrderBook

@pytest.fixture()
def fundamentalist():
    return Trader(name='supplier', money=10, bid_ask_spread=10, memory=2, ma_short=3, ma_long=5,
                  valuation_function=extrapolate_average_profit, propensity_to_switch=1.1)


@pytest.fixture()
def chartist():
    return Trader(name='demander', money=10, bid_ask_spread=10, memory=2, ma_short=3, ma_long=5,
                  valuation_function=extrapolate_ma_price, propensity_to_switch=1.1)

@pytest.fixture()
def chartist_two():
    return Trader(name='demander', money=10, bid_ask_spread=10, memory=2, ma_short=3, ma_long=4,
                  valuation_function=extrapolate_ma_price, propensity_to_switch=1.1)


@pytest.fixture()
def firm():
    return Firm(name='firm', book_value=200, profits=[3, 5, 5, 3])


@pytest.fixture()
def stock(firm):
    return Stock(firm, 200)

@pytest.fixture()
def limitorderbooks(stock):
    # create a firm
    firmpje = Firm("Firm1", 10000, [200, 300, 400, 300])
    # create a stock of that firm
    stocks = Stock(firmpje, 1000)
    return [LimitOrderBook(stocks, 100, 120), LimitOrderBook(stock, 100, 120)]


def test_orders_based_on_stock_valuation(fundamentalist, chartist_two, stock, limitorderbooks):
    new_orderbook = orders_based_on_stock_valuation(fundamentalist, limitorderbooks[1], stock)
    assert_equal(len(new_orderbook.bids), 1)
    assert_equal(len(new_orderbook.asks), 0)
    chart_orderbook = orders_based_on_stock_valuation(chartist_two, limitorderbooks[1], stock)
    assert_equal(len(chart_orderbook.bids), 1)
    assert_equal(len(chart_orderbook.asks), 0)


def test_best_trade():
    seller1 = Trader("1", 100, 10, 2, 3, 5, extrapolate_average_profit, propensity_to_switch=1.1)
    seller2 = Trader("2", 100, 5, 2, 3, 5, extrapolate_average_profit, propensity_to_switch=1.1)
    demander = Trader("d", 100, 10, 1, 3, 5, extrapolate_average_profit, propensity_to_switch=1.1)
    firm = Firm("1", 200, [10, 20])
    stock = Stock(firm, 10)
    seller1.stocks[stock] = 3
    seller2.stocks[stock] = 3
    demander.stocks[stock] = 4
    trade = find_best_trade(demander, [seller1, seller2], stock)
    assert_equal(trade[:-1], [seller2, 3])
    assert_almost_equal(trade[-1], 30.0075)


def test_selling_price(stock, fundamentalist, chartist):
    assert_almost_equal(selling_price(stock, fundamentalist), extrapolate_average_profit(stock, 2) * 1.0005)
    assert_equal(selling_price(stock, chartist), None)


def test_buying_price(stock, fundamentalist, chartist):
    assert_almost_equal(buying_price(stock, fundamentalist), extrapolate_average_profit(stock, 2) * 0.9995)
    assert_equal(buying_price(stock, chartist), None)


def test_best_supplier(fundamentalist, chartist, stock):
    low_price = Trader('low', 10, 5, 1, 3, 5, extrapolate_average_profit, propensity_to_switch=1.1)
    distribute_initial_stocks([stock], [low_price, chartist])
    assert_equal(best_supplier([fundamentalist, chartist, low_price], stock), low_price)
    assert_equal(best_supplier([chartist, low_price, fundamentalist], stock), low_price)


def test_volume_price():
    seller = Trader("1", 100, 10, 2, 3, 5, extrapolate_average_profit, propensity_to_switch=1.1)
    demander = Trader("2", 100, 10, 1, 3, 5, extrapolate_average_profit, propensity_to_switch=1.1)
    firm = Firm("1", 200, [10, 20])
    stock = Stock(firm, 10)
    seller.stocks[stock] = 5
    demander.stocks[stock] = 5
    assert_almost_equal(find_volume_price(demander, seller, stock), [3, 30.015])
    assert_equal(find_volume_price(seller, demander, stock), None)


def test_transaction(chartist, fundamentalist, stock):
    buyer = chartist
    seller = fundamentalist
    buyer.stocks[stock] = 2
    seller.stocks[stock] = 2
    transaction(buyer, seller, stock, 1, 7)
    assert_equal([buyer.stocks[stock], buyer.money, seller.stocks[stock], seller.money], [3, 3, 1, 17])

