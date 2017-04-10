"""This file runs tests for all functions in agents"""

from stockmarket.agents import *
from stockmarket.valuationfunctions import *
from stockmarket.firms import Firm
from stockmarket.stocks import Stock
from numpy.testing import assert_equal

def test_valuate_stocks():
    traderEA = Trader("Agent1", 10, 0, 2, valuation_extrapolate_average)
    traderEG = Trader("Agent2", 10, 0, 2, valuation_extrapolate_growth_average)
    traderPT = Trader("Agent3", 10, 0, 2, price_trend)
    firm = Firm("Firm1", 10000, 300, [200, 300, 400], 1)
    stock = Stock("Stock1", firm, 100, 1000)
    # test if different kind of functions work
    assert_equal(traderEA.valuate_stocks(stock), valuation_extrapolate_average(stock, 2))
    assert_equal(traderEG.valuate_stocks(stock), valuation_extrapolate_growth_average(stock, 2))
    assert_equal(traderPT.valuate_stocks(stock), price_trend(stock, 2))
    # test change of parameters
    traderEA.memory_size = 3
    assert_equal(traderEA.valuate_stocks(stock), valuation_extrapolate_average(stock, 3))
    # test change function
    traderEA.function = valuation_extrapolate_growth_average
    assert_equal(traderEA.valuate_stocks(stock), valuation_extrapolate_growth_average(stock, 3))



