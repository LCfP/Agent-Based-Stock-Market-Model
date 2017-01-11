ODD format (Overview, Design concepts, Details)

#1 Purpose
What is the purpose of the study? For who is it designed.
To make a working stock market model which contains the minimal amount of moving parts. We design the model as a starting point for the programming learning communities ABM working group. 

#2 Entities, state-variables and scales
What kinds of entities are in the model? By what attributes (i.e. state variables and parameters) are these entities characterized? What are the exogenous factors / drivers of the model? If applicable, how is space included in the model? What are the temporal and spatial resolutions and extents of the model?
Entities and state variables:
Firm:
Amount of stocks
Dividends 
Agents: Traders.
Money
Portfolio of stocks
Bid- ask spread  → FIXED
Memory size
Risk aversion
Extrapolation parameter
Objects: 1 Stock of 1 firm 
Firm
Exogeneous factors - drivers of the model
Dividends process 
Time: 
Quarterly

#3 Process overview and scheduling
What entity does what, and in what order? pseudo-code of the schedule
Update dividends
Update expected price and spread
Market mechanism
Store market prices t-1 

#4 Theoretical and Empirical Background
Which general concepts, theories or hypotheses are underlying the model’s design? On what assumptions is/are the agents’ decision model(s) based? If the model / a submodel (e.g. the decision model) is based on empirical data, where does the data come from?
Asset pricing theory, based on dividends (Net present value calculation). Buyer - seller agents with bid-ask spread. Agents form adaptive / extrapolative expectations.  

#5 Individual decision making
What are the subjects and objects of decision-making? On which level of aggregation is decision-making modeled? Are multiple levels of decision making included? What is the basic rationality behind agents’ decision-making in the model? Do agents pursue an explicit objective or have other success criteria? How do agents make their decisions?  Do the agents adapt their behavior to changing endogenous and exogenous state variables? And if yes, how? Do temporal aspects play a role in the decision process? To which extent and how is uncertainty included in the agents’ decision rules? 
Traders make the following decisions based on rational adaptive expectations: 
Expected-price(previous dividends)
Bid ask spread 
Quantity to buy or sell 

Agents implicitly (through their decision rules) try to maximize profits taking into account their risk aversion. Agents adapt their expectations based on the changing exogeneous dividends. Agents are backward looking in forming their expectations and thus implicitly deal with uncertainty. 

#6 Learning
Is individual learning included in the decision process? How do individuals change their decision rules over time as consequence of their experience? Is collective learning implemented in the model?
There adaptive expectations but there is no real learning. 

#7 Individual sensing
What endogenous and exogenous state variables are individuals assumed to sense and consider in their decisions? What state variables of which other individuals can an individual perceive? What is the spatial scale of sensing?  Are the mechanisms by which agents obtain information modeled explicitly, or are individuals simply assumed to know these variables? Are costs for cognition and costs for gathering information inclu­ded in the model?
Local: They can observe all their own state variables. 
Global: Agents can see the dividends and some of its previous values. 
Other local : They can observe bid- ask prices of other agents. 

#8 Individual prediction
Which data uses the agent to predict future conditions? What internal models are agents assumed to use to estimate future conditions or consequences of their decisions? Might agents be erroneous in the prediction process, and how is it  implemented?
Agents predict dividends based on previous dividend values. They might be erroneous in their prediction.

#9 Interaction
Are interactions among agents and entities assumed as direct or indirect? On what do the interactions depend? If the interactions involve communication, how are such communications represented? If a coordination network exists, how does it affect the agent behaviour? Is the structure of the network imposed or emergent?
Interactions take place on the stock market. The structure of the market is imposed. 

#10 Heterogeneity
Are the agents heterogeneous? If yes, which state variables and/or processes differ between the agents? Are the agents heterogeneous in their decision-making? If yes, which decision models or decision objects differ between the agents?
Agents are heterogeneous in the values of their state variables except for the BID-ASK spread. Their memory size can be different. In their decision rules on which they base their expectation the parameters are heterogeneous.   

#11 Stochasticity
What processes (including initialization) are modeled by assuming they are random or partly random?
In the initialization there is some randomization

There will be some stochasticity in the market mechanism. 

There is a stochastic term in the dividend process. 

#12 Observation
What data are collected from the ABM for testing, understanding, and analyzing it, and how and when are they collected? What key results, outputs or characteristics of the model are emerging from the individuals? (Emergence)
Data: We collect data at the end of every tick. We collect of all state variables. Furthermore, we keep track of all the variables of the market process at the end of the market process loop.
Emergence: Stock prices, trading volume and frequency. Profits. 

#13 Implementation details
How has the model been implemented? Is the model accessible and if so where?
The model will be implemented in Python. It will be publically available via GitHub. 

#14 Initialization
What is the initial state of the model world, i.e. at time t=0 of a simulation run? Is initialization always the same, or is it allowed to vary among simulations? Are the initial values chosen arbitrarily or based on data?
The initial values are chosen arbitrarily and randomly distributed with a fixed seed. 

We begin with 
Agents:
1 firm 
25 traders
Globals 
€ 10.000 money
Firm variables:
Initial dividends
Amount of stocks = 1000
Dividend stochastic process = ARMA process? 
Stock variables:
Owner = firm 1
Trader variables: 
Money = randPar * total Money
Portfolio of stocks = randPar * all stocks
Bid- ask spread  = 10% around expected price
Risk aversion = distribution between 0 and 1 
Memory size = distribution between 2 and 5
Extrapolation parameter = distribution


#15 Input data
Does the model use input from external sources such as data files or other models to represent processes that change over time?
No!!!

#16 Submodels
Markets matching process
What, in detail, are the submodels that represent the processes listed in ‘Process overview and scheduling’? What are the model parameters, their dimensions and reference values?  How were submodels designed or chosen, and how were they parameterized and then tested?

Mix set of Traders
For actingTrader in Traders:
Observe random subset of traders
Calculate best deal and trade with that trader (buy or sell) 
Write data on counterparty + quantity + price to dataset


