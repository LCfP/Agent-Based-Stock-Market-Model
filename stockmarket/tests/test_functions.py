"""This file runs tests for all functions in functions"""
from numpy.testing import assert_equal
from stockmarket.functions import *

class TestFunctions:

    @classmethod
    def setup_class(cls):
        pass

    def test_calculate_npv(self):
        assert_equal(calculate_npv(1, 0.05), 20)
        assert_equal(calculate_npv(2, 0.05), 40)


