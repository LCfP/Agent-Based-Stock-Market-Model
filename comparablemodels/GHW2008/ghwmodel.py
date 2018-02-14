import numpy as np
import random

def ghw_model(seed, simulation_time, init_backward_simulated_time, chaos, risk_av_variance, dividends,
              discount_rate, intensity_of_choice, fundamentalist_adaptive_parameter, chartist_adaptive_parameter,
              bubble_sensitivity, fitness_memory_strenght, risk_adjustment, noise_std, init_price_dev_fundament,
              init_type2_agents, init_type2_holdings):
    """

    :param seed: integer
        used to set the pseudo number generator for experiment reproduction
    :param simulation_time: integer
        Amount of periods over which the simulation takes place
    :param init_backward_simulated_time: integer
        Amount of pre-simulated periods
    :param chaos:
    :param risk_av_variance:
    :param dividends:
    :param discount_rate:
    :param intensity_of_choice:
    :param fundamentalist_adaptive_parameter:
    :param chartist_adaptive_parameter:
    :param bubble_sensitivity:
    :param fitness_memory_strenght:
    :param risk_adjustment:
    :param noise_std:
    :param init_price_dev_fundament:
    :param init_type2_agents:
    :param init_type2_holdings:
    :return:
    """
    random.seed(seed)
    np.random.seed(seed)

    """
    Set-up
    """
    fundamental_price = dividends / discount_rate
    fraction_type2 = [init_type2_agents for x in range(init_backward_simulated_time)]
    returns = [0 for x in range(init_backward_simulated_time)]
    price_deviation_from_fundamental = [init_price_dev_fundament for x in range(init_backward_simulated_time)]
    accumulated_fitness1 = [0 for x in range(init_backward_simulated_time - 1)]
    accumulated_fitness2 = [0 for x in range(init_backward_simulated_time - 1)]
    share_holdings_type1 = [(1 - init_type2_holdings) for x in range(init_backward_simulated_time)]
    share_holdings_type2 = [init_type2_holdings for x in range(init_backward_simulated_time)]
    normalized_acc_fitness = [0 for x in range(init_backward_simulated_time)]
    # TODO make this a function?
    pricing_noise = noise_std * np.random.randn(simulation_time)
    price = [fundamental_price + x for x in price_deviation_from_fundamental]

    """
    Simulation

    Process overview and scheduling
    1. Update profits
    2. Caclulate fitness
    3. Switch strategies
    4. Price forecasting
    5. Price formation
    6. Portfolio decisions
    """
    for day in range(simulation_time):
        # 1 update profits
        profits_type1 = returns[-1] * share_holdings_type1[-1] - \
                        risk_adjustment * 0.5 * risk_av_variance * share_holdings_type1[-1]**2
        profits_type2 = returns[-1] * share_holdings_type2[-1] - \
                        risk_adjustment * 0.5 * risk_av_variance * share_holdings_type2[-1]**2
        # 2 Calculate fitness
        accumulated_fitness1.append(profits_type1 + fitness_memory_strenght * accumulated_fitness1[-1])
        accumulated_fitness2.append(profits_type2 + fitness_memory_strenght * accumulated_fitness2[-1])
        normalized_fitness = np.exp(intensity_of_choice * accumulated_fitness1[-1]) + np.exp(intensity_of_choice * accumulated_fitness2[-1])
        normalized_acc_fitness.append(normalized_fitness)
        performance_measure = np.exp(intensity_of_choice * accumulated_fitness2[-1]) / normalized_fitness
        if np.isnan(performance_measure):
            performance_measure = 0.5
        # 3 Switch strategies
        fraction_type2.append(performance_measure * np.exp(-(price_deviation_from_fundamental[-1])** 2 / bubble_sensitivity))
        # 4 Price forecasting
        type1_forecast_price = fundamentalist_adaptive_parameter * (price_deviation_from_fundamental[-1])
        type2_forecast_price = price_deviation_from_fundamental[-1] + \
                               chartist_adaptive_parameter * \
                               (price_deviation_from_fundamental[-1] - price_deviation_from_fundamental[-2])
        # 5 Price formation
        price_deviation_from_fundamental.append(1/(1+discount_rate) * (((1-fraction_type2[-1]) * type1_forecast_price +
                                                                     fraction_type2[-1] * type2_forecast_price)
                                                + pricing_noise[day]))
        price.append(price_deviation_from_fundamental[-1] + fundamental_price)
        returns.append(price_deviation_from_fundamental[-1] - price_deviation_from_fundamental[-2])
        # 6 Portfolio decision
        share_holdings_type1.append((type1_forecast_price - price_deviation_from_fundamental[-1]) / risk_av_variance)
        share_holdings_type2.append((type2_forecast_price - price_deviation_from_fundamental[-1]) / risk_av_variance)

    return price_deviation_from_fundamental, price, returns, fraction_type2

