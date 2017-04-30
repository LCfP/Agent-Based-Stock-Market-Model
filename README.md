[![Build Status](https://travis-ci.org/LCfP/abm.svg?branch=dev)](https://travis-ci.org/LCfP/abm)
[![Coverage Status](https://coveralls.io/repos/github/LCfP/abm/badge.svg?branch=dev)](https://coveralls.io/github/LCfP/abm?branch=dev)

# Basic stock market model
This repository contains a simple agent-based stock market model. While this is a work in progress, 
the model works. Feel free to copy or use the code under the terms of the licence under LICENCE.txt. 
 
# How to use the model
1. Download the repository to your system.
2. Run the simulation.py file --> this generates a SQLlite database on your system.
3. Use the data_notebook.ipynb (Jupyter Notebook) to analyse the data. 

# Repository structure

* The **ODD.md** file contains the model description
* The **simulation.py** file can be used to run the model and corresponds to the Process overview and scheduling in the ODD. 
* The **stockmarket** folder contains supporting scripts, classes and functions.

For clarity reasons, we tried to stick to a functional programming style as much as possible. Therefore, most of the action takes 
place in the simulation.py file. Exceptions are the functions.transaction, and datawriting functions in database.py.

## To do
- [x] Build minimal model
- [x] Build SQL database
- [ ] Test the existing code
- [ ] Add different traders to the model (fundamentalist and chartists) 
- [ ] New trading mechanism

