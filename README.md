[![Build Status](https://travis-ci.org/LCfP/abm.svg?branch=dev)](https://travis-ci.org/LCfP/abm)
[![Coverage Status](https://coveralls.io/repos/github/LCfP/abm/badge.svg?branch=dev)](https://coveralls.io/github/LCfP/abm?branch=dev)

# Basic stock market model
This repository contains a simple agent-based stock market model. While this is a work in progress, 
the model works. Feel free to copy or use the code under the terms of the licence under LICENCE.txt. 
 
# How to use the model
1. Download the repository to your system.
2. Run the Fundamentals-unknown-replication-notebook, (or recalibrate the model using the calibration notebook). 
3. The results will be added to an sql lite database on your system.
4. In the second part of Fundamentals-unknown-replication-notebook you can analyse the output data.

# Repository structure

* The main folder contains supporting files
* The **stockmarket** folder contains supporting scripts, classes and functions.

For clarity reasons, we tried to stick to a functional programming style as much as possible. Therefore, most of the action takes 
place in the baseline.py file.


