"""This file runs tests for functions in stylized facts"""

from numpy.testing import assert_equal
import numpy as np
from numpy.testing import assert_almost_equal
from stockmarket.stylizedfacts import *

def test_autocorrelation_returns():
    """test the calculation of autocorrelation for extreme cases"""
    assert_equal(autocorrelation_returns([1,1,1,1], 2), np.nan)
    assert_equal(autocorrelation_returns([8, 10, 8, 10, 8], 2), -1.0)

def test_kurtosis():
    """The excess kurtosis of a normal distribution should be close to zero"""
    randomdistr = np.random.normal(0, 0.1, 10000)
    assert_almost_equal(kurtosis(randomdistr), 0, decimal=0)

def test_autocorrelation_abs_returns():
    # autocorrelation of absolute returns should be equal to 1 where the autocor was not 1
    assert_equal(autocorrelation_abs_returns([-8, 6, -4, 2], 2), 1.0)
    # but should work similar to normal autocorrelation when the signs do not switch
    assert_equal(autocorrelation_abs_returns([8, 10, 8, 10, 8], 2), autocorrelation_returns([8, 10, 8, 10, 8], 2))