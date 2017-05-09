"""This file runs tests for all functions in agents"""
import pytest
from stockmarket.agent import *
from stockmarket.valuationfunctions import *
from stockmarket.firms import Firm
from stockmarket.stock import Stock
from numpy.testing import assert_equal
from numpy.testing import assert_raises


@pytest.fixture()
def agents():
    return [Trader("Agent1", 1000, 0, 2, 3, 5, lambda **x: extrapolate_average_profit(**x)),
            Trader("Agent2", 1000, 0, 2, 3, 5, lambda **x: extrapolate_ma_price(**x))]


@pytest.fixture()
def stock():
    firm = Firm("Firm1", 10000, [200, 300, 400, 300], 1)
    return Stock(firm, 1000)


def test_valuate_stocks(agents, stock):
    # test if different kind of functions work
    assert_equal(agents[0].valuate_stocks(stock), extrapolate_average_profit(stock, 2))
    assert_equal(agents[1].valuate_stocks(stock), extrapolate_ma_price(stock, 3, 5))
    # test change of parameters
    agents[0].memory_size = 3
    assert_equal(agents[0].valuate_stocks(stock), extrapolate_average_profit(stock, 3))
    # test change function
    agents[0].function = extrapolate_growth_average_profit
    assert_equal(agents[0].valuate_stocks(stock), extrapolate_growth_average_profit(stock, 3))


def test_buy(agents, stock):
    # does not have stock in portfolio
    agents[0].buy(stock, 10, 500)
    assert_equal(agents[0].stocks[stock], 10)
    assert_equal(agents[0].money, 500)
    # already has this stock in portfolio
    agents[1].stocks[stock] = 50
    agents[1].buy(stock, 10, 500)
    assert_equal(agents[1].stocks[stock], 60)
    assert_equal(agents[1].money, 500)
    # not enough money for transaction
    assert_raises(ValueError, agents[0].buy, stock, 30, 1500)


def test_sell(agents, stock):
    # normal working transaction
    agents[0].stocks[stock] = 50
    agents[0].sell(stock, 10, 500)
    assert_equal(agents[0].stocks[stock], 40)
    assert_equal(agents[0].money, 1500)
    # does not have stock
    assert_raises(ValueError, agents[1].sell, stock, 10, 1000)
    # not enough stock for transaction
    assert_raises(ValueError, agents[0].sell, stock, 50, 1500)
