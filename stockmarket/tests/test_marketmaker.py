import pytest
from stockmarket.marketmaker import *
#from stockmarket.valuationfunctions import *
from stockmarket.firms import Firm
from stockmarket.stock import Stock
from numpy.testing import assert_equal
from numpy.testing import assert_raises


@pytest.fixture()
def marketmakers():
    return [Marketmaker("market_maker1", 1000, 3, (2,15), 0.5, 50, 2),
            Marketmaker("market_maker2", 1000, 3, (2,15), 0.5, 50, 2)]

@pytest.fixture()
def stock():
    firm = Firm("Firm1", 10000, [200, 300, 400, 300])
    return Stock(firm, 1000)

def determine_spread(marketmakers, stock):
    # test if different kind of functions work
    # if the market makers buys exactly its target inventory
    marketmakers[0].buy(stock, 50, 500)
    bid, ask = marketmakers[0].determine_spread(22, stock)
    assert_equal(bid, 22 + marketmakers[0].bid_ask_spread)
    assert_equal(ask, 22 - marketmakers[0].bid_ask_spread)
