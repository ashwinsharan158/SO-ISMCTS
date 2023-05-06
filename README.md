# Cribbage AI agent
## Abstract
This experment discusses the challenges of designing Artificial Intelligence (AI) for non-deterministic imperfect information games as compared to perfect information games. To address these challenges, the Monte Carlo Tree Search (MCTS) technique has been used, which involves random sampling of game playouts to build a search tree instead of relying on domain-specific knowledge about how to play a given game. This study presents the implementation of MCTS in non-deterministic imperfect information games, using techniques such as sampling over many determinizations of a starting game state and considering the player's information set. The results demonstrate the potential of MCTS in addressing the challenges of designing AI for non-deterministic imperfect information games.

[//]: # (Image References)

[image1]: ./output_images/img1.PNG "Car Samples"
[image2]: ./output_images/img2.PNG "Non-car Samples"
[image3]: ./output_images/img3.PNG "HOG Comparison"


## Background

### Cribbage
The card game, Cribbage, involves 2-4 players using a standard deck of 52 cards. For the purposes of this study, only the 2-player version was examined. The objective of the game is for a player to reach 121 points at any point during the game by playing repeated hands. This paper focuses solely on the gameplay aspect of Cribbage.

During each hand, players are dealt six cards and must each discard two cards face down to form a third hand (the crib), which is later scored by the dealer. In the playing stage of the hand, players take turns playing cards face up while keeping a running sum of the ranks of cards played. Once a player cannot play without exceeding 31, the play restarts from zero with the remaining cards. When all cards have been played, players count the points earned by their hands, and the dealer also counts the crib as their second hand. Points can be scored in both the play and counting stages by getting sums of 15 and 31, pairs, flushes, straights (runs), and other combinations.

Cribbage has a relatively small game tree, as only 13 cards are in play per hand for a given deal of the cards. If played with all cards face-up, as a perfect information game, each hand would have at most 129,600 possible combinations..

### MCTS
The concept of MCTS was initially introduced in the field of game AI. MCTS involves constructing a search tree through a process of repeatedly simulating the game with random moves, and recording the average success rate of different moves. This process builds the game tree in an asymmetric manner by placing emphasis on more promising branches. Each node of the search tree accumulates information about its previous performance, which is then used to guide the selection of child nodes during subsequent search iterations. MCTS is an online search technique that does not require precomputed data, and it is an anytime search algorithm, which allows it to be halted once a computational or time limit is reached. At the point of termination, the best move found thus far from the root of the tree is selected. The procedure for building the tree involves several steps, which include the simulation of the game with random moves and the accumulation of information at each node. In more detail, the procedure for building the tree is as follows:
* <b>Nodes</b>: The tree consists of nodes representing states in the game. Each node keeps track of its visit count and total score or value (win or loss in most games) from visiting that node, as well as a reference to its parent node and child nodes.
* <b>Selection</b>: Descend the tree from the root node by following a selection policy until either a terminal node or a node with unexpanded children is reached.
* <b>Expansion</b>: If the selected node is not a terminal node, expand it by creating a new node representing an action taken from the parent node and the state arrived at by taking that action.
* <b>Simulation</b>:Play from the expanded node by following a default policy until reaching a terminal game state, which has a value (score for Cribbage) for each player associated with it. The default policy is usually random play but can be otherwise.
* <b>Backpropagation</b>:Backup the simulation values to all the nodes visited in the selection and expansion steps.

This a typical structure of MCTS but for this paper we make use of a modified approach to deal with a partially observable environment.

### Single observer Information set MCTS
Terminologies used in the section related to the concempts:
* <b>Derterminization</b>: It is a process of making a partially observable environment fully observable by creating a Information set of all possible state including the opponents moves and creating a tree for each state depicting a play out. It is an expensive process with both time and memory. For a environment like card game it would look like all player can see all cards at all states of the game.
* <b>Information set</b>: It is a set of all possible states for a partially observable environment it is used by determinization for creating trees. 

To overcome the problems associated with the determinization approach, we propose searching a single tree whose nodes correspond to information sets rather than states. In single-observer information set MCTS (SO-ISMCTS), nodes in the tree correspond to information sets from the root player’s point of view, and edges correspond to actions (i.e., moves from the point of view of the player who plays them). The correspondence between nodes and information sets is not one–one: partially observable opponent moves that are indistinguishable to the root player have separate edges in the tree, and thus the resulting information set has several nodes in the tree.

![alt_text][image1]

## Experiments
For the first part of this experiment we test how it performs against the random agent and greedy agent for creating a tree with 1000 node possible moves for each game state, where we play a total of 400 games to assess its performance. It makes sense for the scope of this experiment because 
This experiment is cogent as it should show signs of learning and should give a fair win-percentage.

![alt_text][image2]

The above experiment was completed 2hrs 13 mins due the the large number of games and and each step of the game required a tree to be created with a 1000 nodes. According to the table we have good cribbage agent as it at least or around 50% of the time, as some of the best players in history will have win percentages over 55% because of the random nature of the game. 
Now two avenues were explored:

* To change with the UCB selection or node selection to see if a higher win percentage can be obtained.
* To see if we can get a better win rate by increasing the number of nodes possible.

For this part of the experiment we only make use of the random agent to create a baseline.
<b>Changing the UCB</b> For purpose of the experiment we remove the exploration portion of the UCB where we had 

![alt_text][image3]

instead, in an effort to maximize rewarding branch non-zero visited branch. We ran this for 400 games and with a tree node size of 1000. In the results it was found due to the loss of exploration of non-zero visited node there was decline in win percentage against the random player to 45.33%.
<b>Increasing the number of nodes</b> For this part of the experiment we try increase the number of node to see if better performance can be yielded. Hence we increase the number of node to 10000 for 300 games to see if the win percentage increases. Result, caused a win rate of 62% with a run time of 14hrs.

## Conclusion
We have learned from the run that for SO-ISMCTS to perform optimally to give a high percentage of wins needs to a significantly large sum of node to effectively play a partially observable game like cribbage. The game itself has high amounts of random noise causing it not to have a high win rate. In the implementation we observed in the beginning the number possible games states to explore is too high as we have the entire enemy hand of any 4 possible cards out of 37 cards to explore which has 101,270 possible combinations but as soon as the number of enemy cards to explore went down due to the progression of the game easier it became for the algorithm to explore