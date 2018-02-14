from comparablemodels.chiarellaIori import chilori_model
import matplotlib.pyplot as plt
import numpy as np

day_price, day_volume, day_return, price, returns, total_volume = chilori_model.ciarellilori2002(seed=1, max_time=500, init_time=100, number_of_agents=1000, av_return_interval_min=5,
                     av_return_interval_max=50, fundamental_value=1000., allowed_price_steps=0.1, variance_noise_forecast=0.1,
                     order_noise_max=0.5, order_expiration_time=50, fundamental_weight=1., momentum_weight=10., noise_weight=1.,
                     ticks_per_day=100)