"""This file runs tests for all functions in firms"""

from stockmarket.firms import Firm
from numpy.testing import assert_equal


def test_update_profit():
    firm = Firm(name="test", book_value=10000, profits=[100], drift_alpha=0.02, drift_mu=0.03, brownian_delta=0.25,
                brownian_sigma=0.1, dividend_rate=1)
    firm.update_profits(0.0105)
    assert_equal([firm.profit, firm.profit_history], [105, [100, 105]])
