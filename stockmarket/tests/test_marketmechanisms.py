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
                  valuation_function=extrapolate_average_profit, price_to_earnings_window=(6,12), trader_volume_risk_aversion= 0.1, propensity_to_switch=1.1)


@pytest.fixture()
def chartist():
    return Trader(name='demander', money=10, bid_ask_spread=10, memory=2, ma_short=3, ma_long=5,
                  valuation_function=extrapolate_ma_price, price_to_earnings_window=(6,12), trader_volume_risk_aversion= 0.1, propensity_to_switch=1.1)

@pytest.fixture()
def chartist_two():
    return Trader(name='demander', money=10, bid_ask_spread=10, memory=2, ma_short=3, ma_long=4,
                  valuation_function=extrapolate_ma_price, price_to_earnings_window=(6,12), trader_volume_risk_aversion= 0.1, propensity_to_switch=1.1)


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



