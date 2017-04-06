"""This file runs tests for all functions in functions"""
from numpy.testing import assert_equal
import pytest
from numpy.testing import assert_equal
from stockmarket.agents import *
from stockmarket.firms import *
from stockmarket.setup import *
from stockmarket.functions import *

@pytest.fixture()
def set_up_agents():
    demander = Trader(name='demander', money=10, bid_ask_spread=0, memory_size=2)
    supplier = Trader(name='supplier', money=10, bid_ask_spread=0, memory_size=1)
    agents = [demander, supplier]
    firm = Firm(name='firm', book_value=200, profit=0, profit_history=[0, 5, 0], seed=1, dividend_rate=1)
    stocks = setup_stocks([firm], face_value=50)
    # distribute stocks
    stocks, agents = distribute_initial_stocks(stocks, agents)
    return {'demander': demander, 'supplier': supplier, 'agents': agents, 'firm': firm, 'stocks': stocks}

def test_calculate_npv():
    assert_equal(calculate_npv(1, 0.05), 20)
    assert_equal(calculate_npv(2, 0.05), 40)

def test_distribute_initial_stocks(set_up_agents):
    pass
