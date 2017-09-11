import pytest
from stockmarket.agent import Trader
from stockmarket.switchingstrategies import *
from stockmarket.valuationfunctions import *
from numpy.testing import assert_equal
from numpy.testing import assert_raises


@pytest.fixture()
def agents():
    return [Trader(name="Agent1", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3,
                   valuation_function=lambda **x: extrapolate_average_profit(**x), propensity_to_switch=1.1,
                   price_to_earnings_window=(6, 12), trader_volume_risk_aversion=0.1),
            Trader(name="Agent2", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3,
                   valuation_function=lambda **x: extrapolate_ma_price(**x), propensity_to_switch=1.1,
                   price_to_earnings_window=(6, 12), trader_volume_risk_aversion=0.1),
            Trader(name="WeirdAgent", money=1000, bid_ask_spread=0, ma_short=2, ma_long=3,
                   valuation_function=None, propensity_to_switch=1.1,
                   price_to_earnings_window=(6, 12), trader_volume_risk_aversion=0.1)]



def test_adaptive_switching(agents):
    # a none chartist and non fundamentalist agent should raise a value error
    assert_raises(ValueError, adaptive_switching, agents[-1], 1.1, 0.04, 0.03)
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