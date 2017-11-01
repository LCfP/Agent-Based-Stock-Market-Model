""""This file contains functions which can be used for an evolutionary algorithm"""
import random
import bisect
import numpy as np
from stockmarket import baselinemodel
from stockmarket.stylizedfacts import *
from statistics import mean


def average_fitness(population):
    total_cost = 0
    for individual in population:
        total_cost += individual.cost
    return total_cost / (float(len(population)))


def cost_function(observed_values, average_simulated_values):
    """cost function"""
    score = 0
    for obs, sim in zip(observed_values, average_simulated_values):
        score += ((obs - sim) / obs)**2
    return score


def evolve_population(population, fittest_to_retain, random_to_retain, parents_to_mutate, parameters_to_mutate, problem):
    """
    Evolves a population. First, the fittest members of the population plus some random individuals become parents.
    Then, some random mutations take place in the parents. Finally, the parents breed to create children.
    :param population: population individuals sorted by cost (cheapest left) which contain parameter values
    :param fittest_to_retain: percentage of fittest individuals which should be maintained as parents
    :param random_to_retain: percentage of other random individuals which should be maintained as parents
    :param individuals_to_mutate: percentage of parents in which mutations will take place
    :param parameters_to_mutate: percentage of parameters in chosen individuals which will mutate
    :return:
    """
    # 1 retain parents
    retain_lenght = int(len(population) * fittest_to_retain)
    parents = population[:retain_lenght]

    # 2 retain random individuals
    amount_random_indiv = int(len(population) * random_to_retain)
    parents.extend(random.sample(population[retain_lenght:], amount_random_indiv))

    # 3 mutate random parameters of random individuals
    amount_of_individuals_to_mutate = int(parents_to_mutate * len(parents))
    amount_of_params_to_mutate = int(parameters_to_mutate * len(parents[0].parameters))
    for parent in random.sample(parents, amount_of_individuals_to_mutate):
        indexes_of_mutable_params = random.sample(range(len(parent.parameters)), amount_of_params_to_mutate)
        for idx in indexes_of_mutable_params:
            min_value, max_value = problem['bounds'][idx][0], problem['bounds'][idx][1]
            if type(min_value) == float:
                parent.parameters[idx] = random.uniform(min_value, max_value)
            else:
                parent.parameters[idx] = random.randint(min_value, max_value)

    # 4 parents breed to create a new population
    parents_lenght = len(parents)
    desired_lenght = len(population) - parents_lenght
    children = []
    while len(children) < desired_lenght:
        male = random.randint(0, parents_lenght - 1)
        female = random.randint(0, parents_lenght - 1)
        if male != female:
            male = parents[male]
            female = parents[female]
            half = int(len(male.parameters) / 2)
            child_parameters = male.parameters[:half] + female.parameters[half:]
            child = Individual(child_parameters, [], np.inf)
            children.append(child)
    parents.extend(children)
    # the parents list now contains a full new population with the parents and their offspring
    return parents


def simulate_population(population, number_of_runs, simulation_time, number_of_agents, init_tot_money, init_profit, init_discount_rate, stylized_facts_real_life):
    """
    Simulate a population of parameter spaces for the stock market model
    :param population: population of parameter spaces used to simulate model
    :param number_of_runs: number of times the simulation should be run
    :param simulation_time: amount of days which will be simulated for each run
    :return: simulated population, average population fitness
    """
    simulated_population = []
    for idx, individual in enumerate(population):
        parameters = individual.parameters
        stylized_facts = [[], [], [], [], []]

        # identify parameters
        share_chartists = parameters[0]
        share_mean_reversion = parameters[1]
        order_expiration_time = parameters[2]
        agent_order_price_variability = parameters[3]
        agent_order_variability = parameters[4]
        agent_ma_short = parameters[5]
        agent_ma_long = parameters[6]
        agents_hold_thresholds = parameters[7]
        agent_volume_risk_aversion = parameters[8]
        agent_propensity_to_switch = parameters[9]
        profit_announcement_working_days = parameters[10]
        price_to_earnings_base = parameters[11]
        price_to_earnings_heterogeneity = parameters[12]
        price_to_earnings_gap = parameters[13]
        longMA_heterogeneity = parameters[14]
        shortMA_heterogeneity = parameters[15]
        shortMA_memory_divider = parameters[16]
        PE_low_low = price_to_earnings_base
        PE_low_high = int(price_to_earnings_heterogeneity * price_to_earnings_base)
        PE_high_low = PE_low_high + price_to_earnings_gap
        PE_high_high = int(price_to_earnings_heterogeneity * PE_high_low)

        # simulate the model
        for seed in range(number_of_runs):
            agents, firms, stocks, order_books = baselinemodel.stockMarketSimulation(seed=seed,
                                                                                     simulation_time=simulation_time,
                                                                                     init_backward_simulated_time=int(
                                                                                         agent_ma_long * longMA_heterogeneity),
                                                                                     number_of_agents=number_of_agents,
                                                                                     share_chartists=share_chartists,
                                                                                     share_mean_reversion=share_mean_reversion,
                                                                                     amount_of_firms=1,
                                                                                     initial_total_money=(
                                                                                         init_tot_money,
                                                                                     int(init_tot_money * 1.1)),
                                                                                     initial_profit=(
                                                                                     init_profit, init_profit),
                                                                                     discount_rate=init_discount_rate,
                                                                                     init_price_to_earnings_window=(
                                                                                     (PE_low_low,
                                                                                      PE_low_high),
                                                                                     (PE_high_low,
                                                                                      PE_high_high)),
                                                                                     order_expiration_time=order_expiration_time,
                                                                                     agent_order_price_variability=(
                                                                                     agent_order_price_variability,
                                                                                     agent_order_price_variability),
                                                                                     agent_order_variability=agent_order_variability,
                                                                                     agent_ma_short=(agent_ma_short,
                                                                                                     int(
                                                                                                         agent_ma_short * shortMA_heterogeneity)),
                                                                                     agent_ma_long=(agent_ma_long, int(
                                                                                         agent_ma_long * longMA_heterogeneity)),
                                                                                     agents_hold_thresholds=(
                                                                                     1 - agents_hold_thresholds,
                                                                                     1 + agents_hold_thresholds),
                                                                                     agent_volume_risk_aversion=agent_volume_risk_aversion,
                                                                                     agent_propensity_to_switch=agent_propensity_to_switch,
                                                                                     firm_profit_mu=0.058,
                                                                                     firm_profit_delta=0.00396825396,
                                                                                     firm_profit_sigma=0.125,
                                                                                     profit_announcement_working_days=profit_announcement_working_days,
                                                                                     mean_reversion_memory_divider=4,
                                                                                     printProgress=False,
                                                                                     )
            # store simulated stylized facts
            sim_returns = calculate_returns(order_books[0].transaction_prices_history)
            sim_volume = []
            for day in order_books[0].transaction_volumes_history[1:]:
                sim_volume.append(sum(day))
            stylized_facts[0].append(autocorrelation_returns(sim_returns, 25))
            stylized_facts[1].append(kurtosis(sim_returns))
            stylized_facts[2].append(autocorrelation_abs_returns(sim_returns, 25))
            stylized_facts[3].append(hurst(sim_returns, lag1=2, lag2=20))
            stylized_facts[4].append(correlation_volume_volatility(sim_volume, sim_returns, window=10))

            # create next generation individual
        next_gen_individual = Individual(parameters, [], np.inf)
        # add average stylized facts to individual
        for s_fact in stylized_facts:
            next_gen_individual.stylized_facts.append(mean(s_fact))
        # add average fitness to individual
        next_gen_individual.cost = cost_function(stylized_facts_real_life, next_gen_individual.stylized_facts)
        # set any non_volume simulation cost to infinity
        if np.isnan(next_gen_individual.cost):
            next_gen_individual.cost = np.inf
        # insert into next generation population, lowest score to the left
        bisect.insort_left(simulated_population, next_gen_individual)

    average_population_fitness = average_fitness(simulated_population)

    return simulated_population, average_population_fitness

class Individual:
    """The order class can represent both bid or ask type orders"""
    def __init__(self, parameters, stylized_facts, cost):
        self.parameters = parameters
        self.stylized_facts = stylized_facts
        self.cost = cost

    def __lt__(self, other):
        """Allows comparison to other individuals based on its cost (negative fitness)"""
        return self.cost < other.cost