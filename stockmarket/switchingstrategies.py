"""In this file, we define the switching functions for switching strategy"""

import numpy as np
from stockmarket.valuationfunctions import *


def adaptive_switching(agent, propensity_to_switch, realised_returns, possibly_realised_returns):
    """The agent switches strategy if its returns where below what it could have earned"""
    fundamentalist = extrapolate_average_profit
    chartist = predict_by_moving_avg_growth
    agent_type = str(agent.function)

    if (str(fundamentalist) not in agent_type) and (str(chartist) not in agent_type):
        raise ValueError("agent is neither a chartist nor a fundamentalist")

    missed_returns = max((possibly_realised_returns - realised_returns), 0)
    prob_status_quo_choice = max(1 - missed_returns * propensity_to_switch, 0)

    if str(fundamentalist) in agent_type:
        prob_fundamentalist = prob_status_quo_choice
        prob_chartist = 1 - prob_status_quo_choice
    else:
        prob_fundamentalist = 1 - prob_status_quo_choice
        prob_chartist = prob_status_quo_choice

    strategy = np.random.choice([chartist, fundamentalist], p=[prob_chartist, prob_fundamentalist])

    return strategy

