"""This file runs tests for all functions in functions"""
import pytest
from numpy.testing import assert_equal
from numpy.testing import assert_raises
from stockmarket.agents import *
from stockmarket.firms import *
from stockmarket.setup import *
from stockmarket.stocks import *
from stockmarket.functions import *
from stockmarket.valuationfunctions import *


@pytest.fixture()
def set_up_agents():
    demander = Trader(name='demander', money=10, bid_ask_spread=0, memory_size=2, function=valuation_extrapolate_average)
    supplier = Trader(name='supplier', money=10, bid_ask_spread=0, memory_size=1, function=valuation_extrapolate_average)
    agents = [demander, supplier]
    firm = Firm(name='firm', book_value=200, profit=0, profit_history=[0, 5, 0], seed=1, dividend_rate=1)
    stocks = setup_stocks([firm], face_value=50)
    # distribute stocks
    agents = distribute_initial_stocks(stocks, agents)
    return {'demander': demander, 'supplier': supplier, 'agents': agents, 'firm': firm, 'stocks': stocks}


def test_calculate_npv():
    # positive values
    assert_equal(npv_growing_perpetuity(2, 0.05), 40)
    assert_equal(npv_growing_perpetuity(2, 0.1, 0.05), 40)
    # negative values
    assert_equal(npv_growing_perpetuity(-2, 0.05), -40)
    # growth >= discount
    assert_raises(ValueError, npv_growing_perpetuity, 2, -0.05)
    assert_raises(ValueError, npv_growing_perpetuity, 2, 0.5, 0.7)
    assert_raises(ValueError, npv_growing_perpetuity, 1, 0.5, 0.5)


def test_distribute_initial_stocks(set_up_agents):
    # even distribution
    assert_equal(set_up_agents['demander'].stocks[set_up_agents['stocks'][0]], 2)
    assert_equal(set_up_agents['supplier'].stocks[set_up_agents['stocks'][0]], 2)
    # uneven distribution
    other_firm = Firm("other", 200, 0, [0, 5, 0], 1, 1)
    stock = Stock(other_firm, 40)
    agents = distribute_initial_stocks([stock], set_up_agents['agents'])
    assert_equal(agents[0].stocks[stock], 3)
    assert_equal(agents[1].stocks[stock], 2)


def test_transaction():
    pass

