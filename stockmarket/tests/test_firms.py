"""This file runs tests for all functions in firms"""

from stockmarket.firms import Firm
from numpy.testing import assert_equal


def test_update_profit():
    firm = Firm("test", 10000, [100], 1)
    firm.update_profits(1.05)
    assert_equal([firm.profit, firm.profit_history], [105, [100, 105]])
