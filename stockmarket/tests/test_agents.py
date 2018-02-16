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
    return [Trader(name="Agent1", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3, valuation_function=lambda **x: extrapolate_average_profit(**x), propensity_to_switch=1.1, price_to_earnings_window=(6,12), trader_volume_risk_aversion= 0.1),
            Trader(name="Agent2", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3, valuation_function=lambda **x: extrapolate_ma_price(**x), propensity_to_switch=1.1, price_to_earnings_window=(6,12), trader_volume_risk_aversion= 0.1)]


@pytest.fixture()
def stock():
    firm = Firm("Firm1", 10000, [200, 300, 400, 300])
    return Stock(firm, 1000)

def test_buy(agents, stock):
    """Test if the buy function"""
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
    """Test if the sell function throws the correct errors if selling cannot be done"""
    # normal working transaction
    agents[0].stocks[stock] = 50
    agents[0].sell(stock, 10, 500)
    assert_equal(agents[0].stocks[stock], 40)
    assert_equal(agents[0].money, 1500)
    # does not have stock
    assert_raises(ValueError, agents[1].sell, stock, 10, 1000)
    # not enough stock for transaction
    assert_raises(ValueError, agents[0].sell, stock, 50, 1500)


def test_buy_sell_or_hold(agents, stock):
    """Test if a deviation from fundamentals overwrites the technical strategy"""
    # the first agent should sell as the P/E ratio is too high
    buy_or_sell = agents[0].buy_sell_or_hold(price_series=[2 for x in range(300)], current_price_to_earnings_ratio=14)
    assert_equal(buy_or_sell, 'sell')
    # the second agent should buy as the P/E ratio is too low
    buy_or_sell = agents[1].buy_sell_or_hold(price_series=[2 for x in range(300)], current_price_to_earnings_ratio=3)
    assert_equal(buy_or_sell, 'buy')

#test_buy_sell_or_hold(agents(), stock())