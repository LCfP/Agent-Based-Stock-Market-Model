import pytest
from stockmarket.agent import Trader
from stockmarket.switchingstrategies import *
from stockmarket.valuationfunctions import *
from numpy.testing import assert_equal
from numpy.testing import assert_raises


@pytest.fixture()
def agents():
    return [Trader("Agent1", 1000, 0, 2, 3, 5, extrapolate_average_profit, price_to_earnings_window=(6,12), propensity_to_switch=1.1),
            Trader("Agent2", 1000, 0, 2, 3, 5, predict_by_moving_avg_growth, price_to_earnings_window=(6,12), propensity_to_switch=1.1),
            Trader("WeirdAgent", 1000, 0, 2, 3, 5, None, price_to_earnings_window=(6,12), propensity_to_switch=1.1)]


def test_adaptive_switching(agents):
    # a none chartist and non fundamentalist agent should raise a value error
    assert_raises(ValueError, adaptive_switching, agents[-1], 0.3, 0.04, 0.03)
    # the fundamentalist agent does not switch strategy if it did not mis any returns
    # assert_equal(adaptive_switching(agent=agents[0], propensity_to_switch=0.3, realised_returns=0.04,
    #                                 possibly_realised_returns=0.03), agents[0].function)
    # the chartist agent does not switch strategy if it did not miss any returns
    # assert_equal(adaptive_switching(agent=agents[1], propensity_to_switch=0.3, realised_returns=0.04,
    #                                 possibly_realised_returns=0.03), agents[1].function)

    # the fund agent switches strategies for sure as possibly realised returns are 100% bigger than realised returns
    # assert_equal(adaptive_switching(agent=agents[0], propensity_to_switch=2, realised_returns=0,
    #                                 possibly_realised_returns=1), agents[1].function)
    # the chartist agent switches strategies for sure as possibly realised returns are 100% bigger than realised returns
    # assert_equal(adaptive_switching(agent=agents[1], propensity_to_switch=2, realised_returns=0,
    #                                 possibly_realised_returns=1), agents[0].function)