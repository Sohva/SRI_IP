
                 First Stab at CP for SR (stable roommates)
                 ------------------------------------------

The model is based on the binary constraint proposed in SARA 2005 and IJCAI2005 and CPAIOR-2014
The cost is O(n^3) for the binary constraint  models. The binary constraint is posted between all pairs of 
agents that find each other acceptable in a stable roommates instance where preference lists may be 
incomplete (i.e. SRI). The n-ary constraint is a single object posted over the array of agents and is 
O(n^2) complexity (optimal)

Directories
-----------
codeyyyymmdd is where the java source files reside
data contains stable roommates problem instance
choco is where choco jar file has been placed

choco
-----
The choco constraint programming toolkit is used, consequently choco-solver-2.1.5.jar must be in the classpath.
This has been placed into the choco directory

The Models
----------
We have 2 models: 

    (a) SR: using toolkit constraints and enumerated domained variables. 
    (b) SRNary: using the specialized n-ary constraint.

All the models have a constrained integer variable for each agent, with a domain of ranks
0 to L_i, where L_i is the length of agent_i preference list. If the agent is assigned the value n 
this means the agent_i is matched to agent_i. Internally, ranks run from 0 to n, as do agent indices, 
therefore everything is shifted down one to zero.

To Run
------
To get a first solution

  >> java SR* fname option

where SR* is SR or SRNary, fname is the filename of an problem instance and option is
one of first, all, count or propagation. NOTE: if the option is omitted then it defaults to first.

The Output
----------
For the following options we get the following output

 first:     a solution is delivered as a list of pairs followed by run time statistics
 all:       all solutions are output plus run time statistics
 count:     the number of solutions are output and runtime statistics
 propagate: the phase1 table is output with restricted runtime statistics

Run Time Statistics
-------------------
For options all, first and count 

   nodes:     number of "decisions" made by choco
   modelTime: time to create the model
   solveTime: time spent searching for solutions
   totalTime: time to read, model and solve
   modelSize: the size of the model in kilobytes

When option is propagate nodes and solveTime are omitted

To Generate Random Problem Instances
-----------------------------------
Use the program RandomRoommate

 >> java RandomRoommate 20

will output a random instance with n=20

 >> java RandomRoomate 20 0.5

will output a random instances of a stable roommates problem with incomplete preference
lists, where the probability of an agent occurring in a preference list is 0.5 

Examples
--------
From within the code directory

 >> java SRNary ../data/sr10.txt all
(1,7) (2,3) (4,9) (5,10) (6,8) 
(1,7) (2,8) (3,5) (4,9) (6,10) 
(1,7) (2,8) (3,6) (4,9) (5,10) 
(1,4) (2,8) (3,6) (5,7) (9,10) 
(1,4) (2,9) (3,6) (5,7) (8,10) 
(1,4) (2,3) (5,7) (6,8) (9,10) 
(1,3) (2,4) (5,7) (6,8) (9,10) 
nodes: 12  modelTime: 161  solveTime: 16  totalTime: 212  modelSize: 7735 

 >> java SRNary ../data/sr10.txt propagate
1: 8 2 3 6 4 7 
2: 4 3 8 9 5 1 10 6 
3: 5 6 2 1 7 10 
4: 9 1 6 2 
5: 7 10 8 2 6 3 
6: 2 8 3 4 10 1 5 9 
7: 1 8 3 5 
8: 10 2 5 6 7 1 
9: 6 2 10 4 
10: 3 6 5 2 9 8 
modelTime: 163  totalTime: 201  modelSize: 7735  


NOTE
----
The code also works for stable roommates ... just make an SRI instance that is bipartite


Mac?
---
See Martin Van der Linden's blog

https://martinvdlinden.wordpress.com/2016/04/01/finding-all-stable-matchings-in-roommate-and-marriage-problems/



Patrick Prosser
04/04/2016