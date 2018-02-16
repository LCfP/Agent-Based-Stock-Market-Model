"""This file runs tests for all functions in firms"""

from stockmarket.firms import Firm
from numpy.testing import assert_equal, assert_almost_equal
import pandas as pd
import pytest

@pytest.fixture
def firm():
    return Firm(name="test", book_value=10000, profits=[100], mu=0.03, brownian_delta=0.25,
                brownian_sigma=0.1, dividend_rate=1)


def test_update_profit(firm):
    firm.update_profits(105)
    assert_equal([firm.profit, firm.profit_history], [105, [100, 105]])


def test_determine_profit(firm):
    # ask the firm to generate a series of profits using the function
    for t in range(150):
        next_profit = firm.determine_profit()
        firm.update_profits(next_profit)
    # second order autocorrelation of returns should be close to zero
    assert_almost_equal(pd.Series(firm.profit_history[-150:]).pct_change().autocorr(lag=2),0, decimal=0)
    # the lenght of profits should be 151
    assert_equal(len(firm.profit_history), 151)