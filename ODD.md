#ODD format (Overview, Design concepts, Details)

##1 Purpose
*What is the purpose of the study? For who is it designed.* 

To make a working stock market model which contains the minimal amount of moving parts. We design the model as a starting point for the programming learning communities ABM working group. 

##2 Entities, state-variables and scales
*What kinds of entities are in the model? By what attributes (i.e. state variables and parameters) are these entities characterized? What are the exogenous factors / drivers of the model? If applicable, how is space included in the model? What are the temporal and spatial resolutions and extents of the model?*

**Firm:**
- Book value: *assets - liabilities.*
- Profit: *exogenous process.*
- Profit history: *stores all previous profits*
- Dividend rate: *the rate at which profit is turned into dividends.*

**Traders:**
- Money
- Portfolio of stocks: *The type and amount of that stock agent holds*
- Bid-ask spread: *the percentage difference between the amount at which an agent is willing to buy and sell a stock.*
- Memory size: *the amount of periods an agent remembers stock prices*

**Firm stocks:**
- Firm: *the firm this stock refers to.*
- Face value: *the value printed on the stock.*
- Amount: *The amount of this type of stock in circulation.*

**Time scale:** Quarterly

##3 Process overview and scheduling
*What entity does what, and in what order? pseudo-code of the schedule*

1. Update firm profits and dividends
2. Update expected price and spread
3. Market mechanism
4. Store market prices t-1 

##4 Theoretical and Empirical Background
*Which general concepts, theories or hypotheses are underlying the model’s design? On what assumptions is/are the agents’ 
decision model(s) based? If the model / a submodel (e.g. the decision model) is based on empirical data, where does the 
data come from?*

The way that agents value stocks is based on asset pricing theory. Agents make a net-present value calculation of stocks 
based on dividends. Agents make this calculation based on adaptive / extrapolative expectations. This means that they  
Furthermore, agents can be both buyer and seller as long as their price demands are met. Therefore, agents work with 
a spread which between their ask (at which they are willing to sell) and their bid price (at which they are wiling to 
buy).  

##5 Individual decision making
*What are the subjects and objects of decision-making? On which level of aggregation is decision-making modeled? 
Are multiple levels of decision making included? What is the basic rationality behind agents’ decision-making in 
the model? Do agents pursue an explicit objective or have other success criteria? How do agents make their decisions?  
Do the agents adapt their behavior to changing endogenous and exogenous state variables? And if yes, how? 
Do temporal aspects play a role in the decision process? To which extent and how is uncertainty included in the agents’ 
decision rules?*

In the model traders are the decision makers. Traders make the following decisions:
- Determine stock value,
- Determine stock quantity to buy or sell.

By buying at a price below their expected stock value and selling at a price above that agents try to maximize profits. 
Agents deal with uncertainty by using an adaptive heuristic which looks at the past. They adapt their expectations 
based on their memory of previous dividends. 

##6 Learning
*Is individual learning included in the decision process? How do individuals change their decision rules 
over time as consequence of their experience? Is collective learning implemented in the model?*

By updating their memoery of previous dividends, traders update their expectated stock value.
Since their valuation strategy does not change, there is no real learning. 

##7 Individual sensing
*What endogenous and exogenous state variables are individuals assumed to sense and consider in their decisions? 
What state variables of which other individuals can an individual perceive? What is the spatial scale of sensing?  
Are the mechanisms by which agents obtain information modeled explicitly, or are individuals simply assumed to 
know these variables? Are costs for cognition and costs for gathering information inclu­ded in the model?*

Traders can observe:
- their own state variables,
- bid-ask prices of other traders,
- stock state variables,
- firm profits and dividend rate.

##8 Individual prediction
*Which data uses the agent to predict future conditions? What internal models are agents assumed to use to 
estimate future conditions or consequences of their decisions? 
Might agents be erroneous in the prediction process, and how is it  implemented?*

Agents predict dividends based on extrapolating a set of previous dividend values. 
Since the actual dividend process it stochastic, they might be erroneous in their prediction.

##9 Interaction
*Are interactions among agents and entities assumed as direct or indirect? 
On what do the interactions depend? If the interactions involve communication, how are such communications represented? 
If a coordination network exists, how does it affect the agent behaviour? 
Is the structure of the network imposed or emergent?*

Interactions take place on the stock market. The structure of the market is imposed. 

##10 Heterogeneity
*Are the agents heterogeneous? If yes, which state variables and/or processes differ between the agents? 
Are the agents heterogeneous in their decision-making? If yes, which decision models or decision objects 
differ between the agents?*

Agents are heterogeneous in the values of their state variables. 

##11 Stochasticity
*What processes (including initialization) are modeled by assuming they are random or partly random?*

We use the Mersienne twister pseudo number generator from the Python random package. Random numbers are drawn in:
* the initialization: agent state variables are randomly distributed in a range;
* the dividend process: the dividend process is an AR process;
* the market mechanism: the order of agents entering and being drawn from the market is random. 

##12 Observation
*What data are collected from the ABM for testing, understanding, and analyzing it, and how and when are they collected? 
What key results, outputs or characteristics of the model are emerging from the individuals? (Emergence)*

**Data:** We collect all object state variables at the end of every period. 
Furthermore, we keep track of transactions that take place during the market mechanism. 

**Emergence:** The transaction prices, quantities, and frequency emerge from the market interactions. 

##13 Implementation details
*How has the model been implemented? Is the model accessible and if so where?*

The model will be implemented in Python. It will be publicly available via GitHub. 

##14 Initialization
*What is the initial state of the model world, i.e. at time t=0 of a simulation run? 
Is initialization always the same, or is it allowed to vary among simulations? 
Are the initial values chosen arbitrarily or based on data?*

The initial values are randomly within a fixed range. This range is not based on data.
Stocks are initally distributed at random.
As we use a pseudo random number generator, We can replicate the model exactly if we use a fixed seed. 

### 14.1 Initial objects
* Firms: 1
* Stocks: 
* Traders: 25

### 14.2 Initial trader variables
* Money : (100, 200)
* Bid ask spread : (5, 5)
* Memory size: (2, 3)

###14.3 Initial firm variables:
* Profit : (200, 200)
* Book value : (10000, 10000)
* Profit history : [150, 170, 190]
* Dividend payout ratio : 1

###14.4 Initial stock variables:
* Face value: 50
* Firm: Firm 1 

##15 Input data
*Does the model use input from external sources such as data files or other models to represent processes 
that change over time?*

No.

##16 Submodels
*What, in detail, are the submodels that represent the processes listed in ‘Process overview and scheduling’? 
What are the model parameters, their dimensions and reference values?  How were submodels designed or chosen, 
and how were they parameterized and then tested?*

Markets matching process

* Mix set of Traders
* For trader in Traders:
    1. Observe random subset of traders and their ask price
    2. Pick the cheapest trader from that set
    3. Buy maximung amount of stocks possible (given money) from that trader


