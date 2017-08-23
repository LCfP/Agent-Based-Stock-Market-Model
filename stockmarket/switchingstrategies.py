"""In this file, we define the switching functions for switching strategy"""

from stockmarket.buysellfunctions import *


def adaptive_switching(agent, propensity_to_switch, realised_returns, possibly_realised_returns):
    """The agent switches strategy if its returns where below what it could have earned"""
    mean_reverter = mean_reversion
    momentum_trader = momentum
    agent_type = str(agent.function)

    if (str(mean_reverter) not in agent_type) and (str(momentum_trader) not in agent_type):
        raise ValueError("agent type is unknown")

    missed_returns = max((possibly_realised_returns - realised_returns), 0)
    prob_status_quo_choice = max(1 - missed_returns * propensity_to_switch, 0)

    if str(mean_reverter) in agent_type:
        prob_fundamentalist = prob_status_quo_choice
        prob_chartist = 1 - prob_status_quo_choice
    else:
        prob_fundamentalist = 1 - prob_status_quo_choice
        prob_chartist = prob_status_quo_choice

    strategy = np.random.choice([momentum_trader, mean_reverter], p=[prob_chartist, prob_fundamentalist])

    return strategy

