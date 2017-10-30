"""This file contains functions and tests to calculate the stylized facts"""
import pandas as pd
import numpy as np
from math import isclose
import powerlaw
from stockmarket.functions import div0

# return autocorrelation close to zero after lag 1
# calculate returns
def calculate_close(orderbook_transaction_price_history):
    closing_prices = []
    for day in orderbook_transaction_price_history:
        closing_prices.append(day[-1])
    close = pd.Series(closing_prices).pct_change()
    return close


def calculate_returns(orderbook_transaction_price_history):
    """Return the returns"""
    closing_prices = []
    for day in orderbook_transaction_price_history:
        closing_prices.append(day[-1])
    returns = pd.Series(closing_prices).pct_change()
    return returns[1:]


# Test 1
def zero_autocorrelation(returns, lags):
    """returns wether average autocorrelation is much different from zero"""
    autocorr_returns = [returns.autocorr(lag=lag) for lag in range(lags)]
    # if mean autocorrelation are between -0.1 and 0.1
    average_autocorrelation = np.mean(autocorr_returns[1:])
    if (average_autocorrelation < 0.1) and (average_autocorrelation > -0.1):
        return True, average_autocorrelation
    else:
        return False, np.inf

# Test 2
def fat_tails(returns):
    results = powerlaw.Fit(returns)
    alpha = results.power_law.alpha
    #print(alpha)
    if (alpha < 5) and (alpha > 3):
        return True, alpha
    else:
        return False, np.inf

def fat_tails_kurtosis(returns):
    series_returns = pd.Series(returns)
    kurt = series_returns.kurtosis()
    if kurt > 4:
        return True, kurt
    else:
        return False, np.inf


# Test 3
def clustered_volatility(returns, lags):
    absolute_returns = returns.abs()
    autocorr_abs_returns = [absolute_returns.autocorr(lag=lag) for lag in range(lags)]
    average_autocorrelation = np.mean(autocorr_abs_returns[1:])
    #print(average_autocorrelation)
    if (average_autocorrelation < 0.1) and (average_autocorrelation > -0.1):
        return False, np.inf
    else:
        return True, average_autocorrelation


# Test 4
def long_memory(returns, hurst_function, lag1, lag2):
    h = hurst_function(returns, lag1, lag2)
    #print('h = ', h)
    return not isclose(0.5, h, abs_tol=(10 ** -1 / 2)), h

def hurst(price_series, lag1, lag2):
    """
    This is an adaption from:
    https://robotwealth.com/demystifying-the-hurst-exponent-part-1/
    """
    lags = range(lag1, lag2)
    std_differences = [np.sqrt(np.std(np.subtract(price_series[lag:], price_series[:-lag]))) for lag in lags]
    m = np.polyfit(np.log(lags), np.log(std_differences), 1)
    hurst = m[0]*2.0
    return hurst

# Test 5
def correlation_volume_volatility():
    