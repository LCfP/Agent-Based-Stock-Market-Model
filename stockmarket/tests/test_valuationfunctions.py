"""This file runs tests for all functions in valuation functions"""

import pytest
from stockmarket.stocks import Stock
from stockmarket.firms import Firm
from stockmarket.valuationfunctions import *
from numpy.testing import assert_equal
from numpy.testing import assert_almost_equal


@pytest.fixture()
def stock():
    return (Stock(Firm("Firm1", 10000, 300, [200, 300, 400], 1), 100),
            Stock(Firm("Firm1", 8774, 246, [215, 359, 233], 1), 100))


def test_extrapolate(stock):
    # natural number
    assert_equal(valuation_extrapolate_average(stock[0], 4), 60)
    # faction
    assert_almost_equal(valuation_extrapolate_average(stock[1], 3), 55.8666666)
    # memory > history
    assert_equal(valuation_extrapolate_average(stock[0], 6), 60)
    



