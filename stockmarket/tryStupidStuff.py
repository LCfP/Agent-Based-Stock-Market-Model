from stockmarket import firms, stock, valuationfunctions, switchingstrategies
from stockmarket.agent import Trader


agents = [Trader("Agent1", 1000, 0, 2, 3, 5, valuationfunctions.extrapolate_average_profit),
            Trader("Agent2", 1000, 0, 2, 3, 5, valuationfunctions.predict_by_moving_avg_growth),
            Trader("WeirdAgent", 1000, 0, 2, 3, 5, None)]

