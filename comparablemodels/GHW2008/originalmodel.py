import numpy as np

# David Ritzwoller
# July 2016

# A Nonlinear Structural Model for Volatility Clustering
# This program is designed to duplicate the results found by
# Andrea Gaunersdorfer & Cars Hommes
# It also builds off the earlier results from
# Gaunersdorfer, Hommes, Wagener, Journal of Economic Behavior and
# Organization, Vol 67, 27-47: 2008

# Type 1 agents hold fundamentalist beliefs
# Type 2 agents are trend followers
# E1t[pt+1] = p* + v(pt-1 - p*)
# E2t[pt+1] = pt-1 + g(pt-1 - pt-2)

T = 10000  # Time Horizon
# For GHW model with low D chaos set chaos = 1
# For GH  model with limit cycle and realistic price dynamics set chaos = 0

# The model is written with the dynamics in terms of deviations
# from the constant fundamental given by pbar
# as x(t) = p(t)-pbar
# this is both a little simpler, and turns out to be a better
# thing to do numerically.  See notes for some details

chaos = 0

# a*sigma(risk aversion * variance)
asig = 1
ybar = 1

if chaos == 1:
    T = 500
    r = 0.01
    pstar = ybar / r
    beta = 4
    v = 0.3
    # g == 2.00 # fixed point
    # g = 2.09 # limit cycle
    g = 2.4  # chaos
    eta = 0
    # std for price noise
    epssig = 0
    alpha = 10
    # set to one for risk adjustment trading profits(done differnently in the
    # two papers)
    riskAdjust = 1
    # starting price level
    startx = 0.01
else:
    r = 0.001
    pstar = ybar / r
    beta = 2
    v = 1
    g = 1.9
    alpha = 1800
    eta = 0.99
    riskAdjust = 0
    epssig = 10
    startx = -400

n2 = np.zeros([T, 1])  # Fraction of type 2
p = np.zeros([T, 1])  # Price
R = np.zeros([T, 1])  # Per share Return
# x = deviation from fundamental (pstar)
x = np.zeros([T, 1])  # p - pstar (used in most dynamics)
u1 = np.zeros([T, 1])  # type 1 accumulated realized profits
u2 = np.zeros([T, 1])  # type 2 accumulated realized profits
z1 = 0.5 * np.ones([T, 1])  # share holdings type 1
z2 = 0.5 * np.ones([T, 1])  # share holdings type 2
eps = epssig * np.random.randn(T)  # additive pricing noise
nn = np.zeros([T, 1])

# initial value

# fraction of agents
n2[0] = 0.5
n2[1] = n2[0]
n2[2] = n2[1]
n2[3] = n2[2]

# x = price - pstar
x[0] = startx
x[1] = x[0]
x[2] = x[1]
x[3] = x[2]

p = pstar + x

# start at t = 5 to allow for lags
for t in range(4, T):
    # update utility
    # simplified equation from paper(see GHW equation(12))
    # u1(t) = -0.5*(x(t-1)-v*x(t-3))^2;
    # u2(t) = -0.5*(x(t-1) - x(t-3) - g*(x(t-3)-x(t-4)))^2;
    # detaled one period profits using last period holdings
    pi1 = R[t - 1] * z1[t - 2] - riskAdjust * 0.5 * asig * z1[t - 2] ** 2
    pi2 = R[t - 1] * z2[t - 2] - riskAdjust * 0.5 * asig * z2[t - 2] ** 2
    # accumulated fitness
    u1[t - 1] = pi1 + eta * u1[t - 2]
    u2[t - 1] = pi2 + eta * u2[t - 2]
    # normalization for logistice
    norm = np.exp(beta * u1[t - 1]) + np.exp(beta * u2[t - 1])
    nn[t] = norm
    # basic n2tilde (before adjustment)
    n2tilde = np.exp(beta * u2[t - 1]) / norm
    # emergency check to make sure still in range, if not set to 0.5
    if np.isnan(n2tilde):
        n2tilde = 0.5
    # adjustment to n, see paper
    n2[t] = n2tilde * np.exp(-(x[t - 1]) ** 2 / alpha)
    # x(t+1) ( p(t+1)) forecasts
    exp1 = v * (x[t - 1])  # type 1 price forecast for t+1
    exp2 = x[t - 1] + g * (x[t - 1] - x[t - 2])  # type 2 price forecast for t+1
    # new price for today from t+1 forecasts (note timing)
    x[t] = 1 / (1 + r) * (((1 - n2[t]) * exp1 + n2[t] * exp2) + eps[t])
    p[t] = x[t] + pstar
    # returns time path
    # R[t-1] = p[t+1] - pstar - (1+r)*(p[t]-pstar) + dstd*np.randn(1)
    R[t] = x[t] - x[t - 1]
    # portfolio decisions
    z1[t] = (exp1 - x[t]) / asig
    z2[t] = (exp2 - x[t]) / asig