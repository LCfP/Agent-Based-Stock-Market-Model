# -*- coding: utf-8 -*-
"""
Agent object
Author: Blake LeBaron
Date: June 14, 2016

All agents are a single instance of this
This is usually put into a single list (as in main program)

"""

import numpy as np


class agent:
    def __init__(self, sigmaF, sigmaM, sigmaN, kmax, Lmin, Lmax):
        # set strategy weights
        # set all positive :  this diverges from the paper a little
        self.fundWeight = np.abs(sigmaF * np.random.randn())
        self.chartWeight = (sigmaM * np.random.randn())
        self.noiseWeight = (sigmaN * np.random.randn())
        # horizons for momentum rules
        self.l = np.random.randint(Lmin, Lmax)
        # random component of spread
        self.k = kmax * np.random.rand()
        self.fcast = 0.
        self.pfcast = 0.
        self.wealth = 0.
        self.bid = 0.
        self.ask = 0.
        # forecast adjustment weight
        self.fcastAdjust = 1. / (self.fundWeight + self.chartWeight + self.noiseWeight)

    def updateFcast(self, forecast, price, tau):
        # weighted forecast value
        self.fcast = self.fcastAdjust * (
        self.fundWeight * forecast.fundamental + self.chartWeight * forecast.chartist[self.l] + \
        self.noiseWeight * forecast.noise)
        # bound the forecast
        self.fcast = min(self.fcast, 0.5)
        self.fcast = max(self.fcast, -0.5)
        # exponentiate the forecast to get future price forecast
        # note:  this could have a variance adjustment, but it doesn't at the moment
        self.pfcast = price * np.exp(self.fcast + 0.0 * forecast.v)

    def getAgentOrder(self, price):
        # generate bid or ask with k and forecast price
        if self.pfcast > price:
            self.bid = (1. - self.k) * self.pfcast
        else:
            self.ask = (1. + self.k) * self.pfcast
