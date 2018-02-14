"""
@author
: Joeri Schasfoort
: rewritten code from Blake LeBaron (http://people.brandeis.edu/~blebaron/classes/agentfin/Chiarellaetal.html)
: based on Chiarella/Iori, Quant Finance, 2002, vol 2, 346-353
"""

import numpy as np
import numpy.random as rnd
from comparablemodels.chiarellaIori.agent import agent
from comparablemodels.chiarellaIori.forecasts import forecasts
from comparablemodels.chiarellaIori.order_book import orderBook

def ciarellilori2002(seed, max_time, init_time, number_of_agents, av_return_interval_min,
                     av_return_interval_max, fundamental_value, allowed_price_steps, variance_noise_forecast,
                     order_noise_max, order_expiration_time, fundamental_weight, momentum_weight, noise_weight,
                     ticks_per_day):
    """
    :param seed: integer
        used to set the pseudo number generator for experiment reproduction
    :param max_time: integer
    :param init_time: integer
    :param number_of_agents: integer
    :param av_return_interval_min: integer
    :param av_return_interval_max: integer
    :param fundamental_value: float
    :param allowed_price_steps:
    :param variance_noise_forecast:
    :param order_noise_max:
    :param order_expiration_time:
    :param fundamental_weight:
    :param momentum_weight:
    :param noise_weight:
    :param ticks_per_day:
    :return:
    """
    np.random.seed(seed)
    """
    Set-up
    """
    #price = fundamental_value * np.ones(max_time + 1)
    price = [fundamental_value * (1. + 0.001 * np.random.randn()) for x in range(init_time)]
    #returns = np.zeros(max_time + 1)
    returns = [0.001 * np.random.randn() for x in range(init_time)]
    total_volume = [0 for x in range(init_time)]
    #total_volume = np.zeros(max_time + 1)
    #day_price = np.zeros(int((max_time + 1) / ticks_per_day))
    agent_list = [agent(fundamental_weight, momentum_weight, noise_weight, order_noise_max, av_return_interval_min,
                        av_return_interval_max) for i in range(number_of_agents)]
    forecastSet = forecasts(av_return_interval_max, fundamental_value, variance_noise_forecast)
    marketBook = orderBook(600., 1400., allowed_price_steps)  # set up initial prices

    #price[0:init_time] = fundamental_value * (1. + 0.001 * np.random.randn(init_time))
    #returns[0:init_time] = 0.001 * np.random.randn(init_time)

    """
    Simulation
    
    Process overview and scheduling
    1. Update all forecasts
    2. Draw random agent
    3. Get its demand /supply 
    4. Submit bid or ask order
    5. Price formation
    6. Portfolio decisions
    """
    for t in range(init_time-1, max_time):
        # update all forecasts
        forecastSet.updateForecasts(t, price[t], returns)
        trade_price = -1
        # draw random agent
        randomAgent = agent_list[np.random.randint(1, number_of_agents)]
        # set update current forecasts for random agent
        randomAgent.updateFcast(forecastSet, price[t], order_expiration_time)
        # get demands for random agent
        randomAgent.getAgentOrder(price[t])
        # potential buyer
        if randomAgent.pfcast > price[t]:
            # add bid or market order
            trade_price = marketBook.addBid(randomAgent.bid, 1., t)
        else:
            # seller: add ask, or market order
            trade_price = marketBook.addAsk(randomAgent.ask, 1., t)
        # update price and volume
        # no trade
        if trade_price == -1:
            price.append((marketBook.bestBid + marketBook.bestAsk) / 2.)
            total_volume.append(total_volume[t])
        else:
            # trade
            price.append(trade_price)
            total_volume.append(total_volume[t] + 1.)
        # returns
        returns.append(np.log(price[t + 1] / price[t]))
        # clear book
        if (rnd.rand() < 0.2):
            marketBook.cleanBook(t, order_expiration_time)

    # generate long run values for time series
    day_volume = np.diff(np.array(total_volume)[range(init_time + ticks_per_day, max_time, ticks_per_day)])
    day_price = np.array(price)[range(init_time + ticks_per_day, max_time, ticks_per_day)]
    day_return = np.diff(np.log(day_price))

    return day_price, day_volume, day_return, price, returns, total_volume