"""This file runs tests for all functions in agents"""
import pytest

from stockmarket.limitorderbook import *
from stockmarket.agent import Trader
from stockmarket.firms import Firm
from stockmarket.stock import Stock
from stockmarket.valuationfunctions import *
from numpy.testing import assert_equal
from numpy.testing import assert_raises

@pytest.fixture()
def agents():
    return [Trader("Agent1", 1000, 0, 2, 3, 5, lambda **x: extrapolate_average_profit(**x)),
            Trader("Agent2", 1000, 0, 2, 3, 5, lambda **x: extrapolate_ma_price(**x))]

@pytest.fixture()
def limitorderbook():
    # create a firm
    firm = Firm("Firm1", 10000, [200, 300, 400, 300], 1)
    # create a stock of that firm
    stocks = Stock(firm, 1000)
    return LimitOrderBook(stocks, 100, 120)

def test_add_bid():
    order_book = limitorderbook
    order_book.add_bid(10, 20, 'trader-1')
    order_book.add_bid(5, 20, 'trader-2')
    order_book.add_bid(7, 20, 'trader-3')
    order_book.add_bid(7, 20, 'trader-4')
    order_book.add_bid(7, 20, 'trader-5')
    # highest bid is 10
    assert_equal(order_book.bids[-1].price, 10)
    # lowest bid is 5
    assert_equal(order_book.bids[0].price, 5)
    # second highest bid trader = trader-2
    assert_equal(order_book.bids[-2].owner, 'trader-3')

def test_add_ask():
    order_book = limitorderbook
    order_book.add_ask(11, 20, 'trader-1')
    order_book.add_ask(5, 20, 'trader-2')
    order_book.add_ask(7, 20, 'trader-3')
    order_book.add_ask(7, 20, 'trader-4')
    order_book.add_ask(7, 20, 'trader-5')
    # highest ask is 11
    assert_equal(order_book.asks[-1].price, 11)
    # lowest ask is 5
    assert_equal(order_book.asks[0].price, 5)
    # second highest ask trader = trader-5
    assert_equal(order_book.asks[-2].owner, 'trader-5')

def test_clean_book():
    order_book = limitorderbook
    order_book.add_bid(10, 20, 'trader-1')
    order_book.add_bid(5, 20, 'trader-2')
    order_book.add_ask(11, 20, 'trader-1')
    order_book.add_ask(5, 20, 'trader-2')
    for n in range(119):
        order_book.clean_book()
    assert_equal(len(order_book.bids), 2)
    assert_equal(len(order_book.asks), 2)
    order_book.clean_book()
    assert_equal(len(order_book.bids), 0)
    assert_equal(len(order_book.asks), 0)