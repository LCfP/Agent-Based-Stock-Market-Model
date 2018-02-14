# -*- coding: utf-8 -*-
"""
Forecast object
Author: Blake LeBaron
Date: June 2016
All forecasts are build from one instance of this

"""

import numpy as np

class forecasts:
    # initialize forecast components
    def __init__(self,Lmax,pf,sigmae):
        self.fundamental = 0.
        # chartist is vector for different lengths
        self.chartist    = np.zeros(Lmax)
        self.noise       = 0.
        self.v = 0.
        self.pf = pf
        self.sigmae = sigmae
        self.Lmax = Lmax
    # update forecasts
    def updateForecasts(self,t,price,ret):
        self.fundamental = np.log(self.pf/price)
        self.noise = self.sigmae*np.random.randn()
        self.v = np.var(ret[0:t])
        revrets = ret[t:(t-self.Lmax):-1]
        self.chartist = np.cumsum(revrets)/np.arange(1.,float(self.Lmax+1))