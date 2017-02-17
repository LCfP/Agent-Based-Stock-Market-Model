# DataBase design for stock market ABM:

Create multiple dataTables and connect them. 

Building a data model:
* Drawing a picture of the different tables and their relationships 
* Don't put the same string data in twice
* Copy in the real world means there should be a copy in the database

Look at the tables and ask if it is a thing... or just an attribute of a thing. 

because we simulate agent interactions and interactions take the form of transactions. that is the first
table. 

### Table 1 Transactions
* primary key = id
* foreign_key = experiment_id
* seed
* period
* amount_of_product
* amount_of_money
* foreign_key = buyer_id
* foreign_key = seller_id 
* foreign_key = stock_id

### Table 2 State Variables
* primary_key = id
* foreign_key = experiment_id
* seed
* period
* foreign_key = Variable_type 
* foreign_key = owner_id (object)
* value

### Table 3 Variable types
* primary_key = id
* logical_key = variable_name

### Table 4 Objects
* primary_key = id
* logical_key = object_name
* STRING object_type 


|


### Possibly later: Experiments
* primary_key = id
* logical_key = experiment
* parameter_space

