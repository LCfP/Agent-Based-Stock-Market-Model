"""In this file, we define the switching functions for switching strategy"""

from stockmarket.buysellfunctions import *


def adaptive_switching(agent, propensity_to_switch, realised_returns, possibly_realised_returns):
    """The agent switches strategy if its returns where below what it could have earned"""
    mean_reverter = mean_reversion
    momentum_trader = momentum
    noise_trader = noise_trading
    agent_type = str(agent.function)

    if (str(noise_trader) in agent_type):
        return noise_trader

    if (str(mean_reverter) not in agent_type) and (str(momentum_trader) not in agent_type):
        raise ValueError("agent type is unknown")

    # TODO remove this code Check if the P/E ratio is too high or too low always switch to mean reversion strategy
    # if (price_to_earnings > agent.price_to_earnings_window[1]) or (
    #     price_to_earnings < agent.price_to_earnings_window[0]):
    #     return mean_reverter

    missed_returns = max((possibly_realised_returns - realised_returns), 0)
    prob_status_quo_choice = max(1 - missed_returns * propensity_to_switch, 0)

    if str(momentum_trader) in agent_type:
        prob_momentum = prob_status_quo_choice
        prob_mean_reversion = 1 - prob_status_quo_choice

    else:
        prob_mean_reversion = prob_status_quo_choice
        prob_momentum = 1 - prob_status_quo_choice


    strategy = np.random.choice([momentum_trader, mean_reverter], p=[prob_momentum, prob_mean_reversion])

    return strategy

