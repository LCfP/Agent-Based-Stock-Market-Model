[![Build Status](https://travis-ci.org/LCfP/abm.svg?branch=dev)](https://travis-ci.org/LCfP/abm)
[![Coverage Status](https://coveralls.io/repos/github/LCfP/abm/badge.svg?branch=dev)](https://coveralls.io/github/LCfP/abm?branch=dev)

# Basic stock market model
This repository contains a simple agent-based stock market model. While this is a work in progress, 
the model works. Feel free to copy or use the code under the terms of the licence under LICENCE.txt. 
 
# How to use the model
1. Download the repository to your system.
2. Run the simulate_cdoubleauction notebook or simulation.py script and fill in the model parameters to your tase. 
3. The results will be added to an sql lite database on your system.
4. Use the data_notebook.ipynb (Jupyter Notebook) to analyse this data. 

# Repository structure

* The **ODD.md** file contains (an early version of) the model description
* The **stockmarket** folder contains supporting scripts, classes and functions.

For clarity reasons, we tried to stick to a functional programming style as much as possible. Therefore, most of the action takes 
place in the simulation.py file. Exceptions are the functions.transaction, and datawriting functions in database.py.

## To do
- [ ] Reach 100% testing coverage
- [ ] Calibrate the model to match stylized facts of real markets

