"""This file runs tests for all functions in agents"""
import pytest
from stockmarket.agents import *
from stockmarket.valuationfunctions import *
from stockmarket.firms import Firm
from stockmarket.stocks import Stock
from numpy.testing import assert_equal
from numpy.testing import assert_raises


@pytest.fixture()
def agents():
    return [Trader("Agent1", 1000, 0, 2, valuation_extrapolate_average),
                Trader("Agent2", 1000, 0, 2, valuation_extrapolate_growth_average),
                Trader("Agent3", 1000, 0, 2, price_trend)]


@pytest.fixture()
def stock():
    firm = Firm("Firm1", 10000, 300, [200, 300, 400], 1)
    return Stock(firm, 100)


def test_valuate_stocks(agents, stock):
    # test if different kind of functions work
    assert_equal(agents[0].valuate_stocks(stock), valuation_extrapolate_average(stock, 2))
    assert_equal(agents[1].valuate_stocks(stock), valuation_extrapolate_growth_average(stock, 2))
    assert_equal(agents[2].valuate_stocks(stock), price_trend(stock, 2))
    # test change of parameters
    agents[0].memory_size = 3
    assert_equal(agents[0].valuate_stocks(stock), valuation_extrapolate_average(stock, 3))
    # test change function
    agents[0].function = valuation_extrapolate_growth_average
    assert_equal(agents[0].valuate_stocks(stock), valuation_extrapolate_growth_average(stock, 3))


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
    assert_raises(KeyError, agents[1].sell, stock, 10, 1000)
    # not enough stock for transaction
    assert_raises(ValueError, agents[0].sell, stock, 50, 1500)
