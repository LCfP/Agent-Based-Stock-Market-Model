"""This file runs tests for all functions in functions"""
from numpy.testing import assert_equal
from numpy.testing import assert_raises
from stockmarket.functions import *

class TestFunctions:

    @classmethod
    def setup_class(cls):
        pass

    def test_calculate_npv(self):
        # default values
        assert_equal(calculate_npv(3), 60)
        # positive values
        # negative values
        # floats
        # discount rate smaller than growth rate
        assert_raises(ValueError, calculate_npv, 1, 0.05, 0.1)
