# GeneticAlgorithmForTSP
Genetic algortihm implementation for travelling sales problem

Details of Genetic Algorithm


# Initialization

To initialize the population, cities are shuffled and added to the population list.


# Cross Over

For cross over “Order One” cross over method is used. 

Order One Cross Over

1.	Choose random index to start swath.

2.	Choose random swath width. Make sure the width does not exceed the length of the city list.

3.	Create swath from parent 1 by taking the city list then copying from random index until random swath width.

4.	Create a new child with empty city list.

5.	Start copying from parent 2. If the city is in swath list then do not copy that city. Only copy the cities which are not present in swath.

6.	Add swath to the child’s city list at random index chosen from step 1. 


# Mutation

For mutation, “Inversion” mutation is used.

Inversion Mutation

1.	Choose a random index to start from.

2.	Choose another random index to stop.

3.	Inverse the list from the starting index to stopping index.


# Parent Selection
For parent selection, “K-Way Tournament” selection method is used.

K-Way Tournament Selection

1.	Choose random k individuals from population.

2.	Compare the fitness’ of the chosen individuals.

3.	Choose and return the individual with best fitness.
