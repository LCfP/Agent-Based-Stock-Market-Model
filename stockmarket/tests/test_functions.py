"""This file runs tests for all functions in functions"""

import pytest
from numpy.testing import assert_equal
from numpy.testing import assert_raises
from stockmarket.firms import *
from stockmarket.setup import *
from stockmarket.valuationfunctions import *
from stockmarket.functions import *


@pytest.fixture()
def set_up_agents():
    demander = Trader(name='demander', money=10, bid_ask_spread=0, memory=2, ma_short=3, ma_long=5,
                      function=lambda x: extrapolate_average_profit(x, 2))
    supplier = Trader(name='supplier', money=10, bid_ask_spread=0, memory=2, ma_short=3, ma_long=5,
                      function=lambda x: extrapolate_average_profit(x, 1))
    agents = [demander, supplier]
    firm = Firm(name='firm', book_value=200, profits=[0, 5, 0, 0], seed=1, dividend_rate=1)
    stocks = setup_stocks([firm], amount=4)
    distribute_initial_stocks(stocks, agents)
    return {'demander': demander, 'supplier': supplier, 'agents': agents, 'firm': firm, 'stocks': stocks}


def test_growing_perpetuity():
    # positive values
    assert_equal(npv_growing_perpetuity(2, 0.05), 40)
    assert_equal(npv_growing_perpetuity(2, 0.1, 0.05), 40)
    # negative values
    assert_equal(npv_growing_perpetuity(-2, 0.05), -40)
    # growth >= discount
    assert_raises(ValueError, npv_growing_perpetuity, 2, -0.05)
    assert_raises(ValueError, npv_growing_perpetuity, 2, 0.5, 0.7)
    assert_raises(ValueError, npv_growing_perpetuity, 1, 0.5, 0.5)


def test_moving_averages():
    # TODO: write tests
    pass


def test_div0():
    assert_equal(div0(23, 0), 0)
    assert_equal(div0(10, 5), 2)
    assert_equal(div0(10, 4), 2.5)
