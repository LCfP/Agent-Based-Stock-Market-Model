"""In this file, we define general functions for the benchmark stock market model"""

import numpy as np


def npv_growing_perpetuity(dividend, discount_rate=0.11, growth_rate=0):
    """Returns the present value of a growing perpetuity.

    Parameters
    ----------
    dividend : scalar
        Value of the first dividend.
    discount_rate : scalar
        Rate of interest as decimal per period.
    growth_rate : scalar
        Rate of growth of the dividend as decimal per period.

    Returns
    -------
    scalar
        Present value
    """
    if discount_rate <= growth_rate:
        raise ValueError('discount rate <= growth rate', 'dc = ' + str(discount_rate), 'gr = ' + str(growth_rate))
    return np.divide(dividend, (discount_rate - growth_rate))


def div0(a, b):
    """
    ignore / 0, and return 0 div0( [-1, 0, 1], 0 ) -> [0, 0, 0]
    credits to Dennis @ https://stackoverflow.com/questions/26248654/numpy-return-0-with-divide-by-zero
    """
    answer = np.true_divide(a, b)
    if not np.isfinite(answer):
        answer = 0
    return answer