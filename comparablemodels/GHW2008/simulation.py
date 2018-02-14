"""
Andrea Gaunersdorfer and Cars Hommes. A nonlinear structural model for volatility clustering. In A. Kirman and G. Teyssiere, editors, Micro Economic Models for Long Memory in Economics, pages 265–288. Springer-Verlag, 2007.

Andrea Gaunersdorfer, Cars H. Hommes, and Florian O. O. Wagener. Bifurcation routes to volatility clustering under evolutionary learning. Journal of Economic Behavior and Organization, 67:27–47, 2008.

Adapted from David Ritzwoller
http://people.brandeis.edu/~blebaron/classes/agentfin/GaunersdorferHommes.html
"""

from comparablemodels.GHW2008 import ghwmodel
import matplotlib.pyplot as plt
import numpy as np

price_deviation_from_fundamental, price, returns, fraction_type2 = \
    ghwmodel.ghw_model(seed=1, simulation_time=10000, init_backward_simulated_time=4, chaos=0, risk_av_variance=1,
                       dividends=1, discount_rate=0.001, intensity_of_choice=2, fundamentalist_adaptive_parameter=1,
                       chartist_adaptive_parameter=1, bubble_sensitivity=1800, fitness_memory_strenght=0.99,
                       risk_adjustment=0, noise_std=10, init_price_dev_fundament=-400, init_type2_agents=0.5,
                       init_type2_holdings=0.5)

fig_p, ax_p = plt.subplots()
ax_p.plot(range(len(price)), price[0:])
plt.xlabel('Time')
plt.ylabel('Price')
plt.show()

# log return
lret = np.log(price[1:]) - np.log(price[0:-1])
# arithmetic return
ret = np.array(price[1:]) / np.array(price[0:-1])-1
ghret = np.array(price[1:]) - 1 - (1+0.001) * np.array(price[0:-1])

fig_r, ax_r = plt.subplots()
ax_r.plot(range(len(lret)), lret[0:] )
plt.xlabel('Time')
plt.ylabel('Returns')
plt.show()