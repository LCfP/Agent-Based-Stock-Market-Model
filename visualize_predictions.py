import numpy as np
import csv
import math
import matplotlib.pyplot as plt
import random

STOCK_DATA = 'YHOO.csv' 

"""
Methods to load and list the data
"""
# loads the stock data and returns a list
def load_stock_data(csv_file): # works with data from YAHOO Finance
    x = []
    with open(csv_file, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            row = row[0].split(',')
            try:
                y = float(row[-2])
            except ValueError:
                pass
            else:
                x.append(y)
    return x 

# takes prediction function and returns list of all predictions
def make_prediction(stock, prediction):
    pred = [None]
    for i,val in enumerate(stock):
        at_i = stock[:i+1]
        pred.append(prediction(at_i))
    return pred

# calculates moving averages from stock data with n periods
def moving_average(x, n):
    i = 0
    while x[i] is None:
        i = i+1
    x = x[i:]
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[n:] - cumsum[:-n]) / n

"""
Prediction functions here
"""

# predicts next price by using ma and growth avg of last periods
def predict_avg_growth(x, n):
    ma = moving_average(x, n)
    try:
        growth = ma[-1] - ma[-2]
        gr_prev = ma[-2] - ma[-3]
    except IndexError:
        return None
    else:
        gr_pre = (growth + gr_prev) / 2
        return ma[-1] + 2 * gr_pre # growth times 2 because MA is delayed by 1 period, so we want to predict the price two periods after the last MA

def chris_method(x, s, l):
    try:
        short_ma = moving_average(x, s)[-1]
        long_ma = moving_average(x, s)[-1]
    except IndexError:
        return None
    return short_ma+((short_ma-long_ma)/(l-s))
        
"""
Execute 
"""
stock = load_stock_data(STOCK_DATA) 
ma = [None] # adding 1 None because when calculating MA, it is delayed by 1 period 
ma.extend(moving_average(stock, 3))

prediction_name = 'Chris/Joeri Method'
prediction = lambda x: chris_method(x, 3, 5)
pred = make_prediction(stock, prediction)

prediction_name2 = 'MA growth'
prediction2 = lambda x: predict_avg_growth(x, 3)
pred2 = make_prediction(stock, prediction2)

"""
Graph
"""
plt.plot(stock, 'r', label=STOCK_DATA)
plt.plot(ma, 'y', label="Moving Average")
plt.plot(pred, 'b', label=prediction_name)
plt.legend()
plt.show()
