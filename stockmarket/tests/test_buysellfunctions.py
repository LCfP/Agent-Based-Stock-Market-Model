import pytest
from stockmarket.stock import Stock
from stockmarket.firms import Firm
from stockmarket.buysellfunctions import *
from numpy.testing import assert_equal
from numpy.testing import assert_almost_equal


@pytest.fixture()
def stock():
    convex = [1]
    for t in range(100):
        previous = convex[-1]
        convex.append(previous * 2)

    concave = [1]
    for t in range(100):
        previous = concave[-1]
        concave.append(concave[0] + previous * 0.75)

    return (Stock(Firm("ConvexFirm", 10000, convex, 1), 100),
            Stock(Firm("ConcaveFirm", 8774, concave, 1), 100))


def test_mean_reversion(stock):
    assert_equal(mean_reversion(stock[0].price_history, shortMA=20, upper_threshold=1.05, lower_threshold=0.95), 'sell')
    assert_equal(mean_reversion(stock[1].price_history, shortMA=20, upper_threshold=1.0, lower_threshold=1.0))
