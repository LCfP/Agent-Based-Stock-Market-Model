from stockmarket.evolutionaryalgo import *
import pytest
from numpy.testing import assert_equal


@pytest.fixture()
def population():
    return [Individual([0.96,0.79,3603,3,4,44,262,0.007,0.31,1.36,46,19,1.3,16,1.5,1.45,2],
                       [-0.008, 3.6, -0.004, 0.4, 0.2], 20)
        ,Individual([0.5,0.23,1603,2,1,64,282,0.004,0.52,1.12,55,21,1.6,18,1.1,1.12,3],
                    [-0.008, 3.8, -0.004, 0.4, 0.2], 30)]

@pytest.fixture()
def problem():
    return({'num_vars': 17,
            'names': ['share_chartists', 'share_mean_reversion', 'order_expiration_time', 'agent_order_price_variability',
            'agent_order_variability', 'agent_ma_short', 'agent_ma_long', 'agents_hold_thresholds',
           'agent_volume_risk_aversion', 'agent_propensity_to_switch', 'profit_announcement_working_days',
           'price_to_earnings_base', 'price_to_earnings_heterogeneity', 'price_to_earnings_gap',
           'longMA_heterogeneity', 'shortMA_heterogeneity', 'shortMA_memory_divider'],
            'bounds': [[0.0, 1.0], [0.0, 1.0], [1000, 10000], [1, 10],
             [0.1, 5.0], [5, 100], [50, 400], [0.00005,0.01],
             [0.1, 1], [0.1, 2.2], [5, 50],
             [10,20], [1.1,2.5], [4,20],
             [1.1,1.8], [1.1,1.8], [1, 10]]})


def test_average_fitness(population):
    assert_equal(average_fitness(population), 25.0)


def test_cost_function(population):
    # the cost of two exactly similar values should be 0
    assert_equal(cost_function(population[0].stylized_facts, population[0].stylized_facts), 0.0)
    assert_equal((cost_function(population[0].stylized_facts, population[0].stylized_facts) < cost_function(population[1].stylized_facts, population[0].stylized_facts)) , True)


def test_evolve_population():
    pass


def debug_ev_pop(population, problem):
    evolve_population(population=population, fittest_to_retain=0.5, random_to_retain=0.5, parents_to_mutate=1, parameters_to_mutate=0.5, problem=problem)

debug_ev_pop(population=population(), problem=problem())