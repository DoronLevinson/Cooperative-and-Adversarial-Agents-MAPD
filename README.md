# Cooperative-and-Adversarial-Agents-in-MAPD-Problem
A Multi-Agent Pickup and Delivery (MAPD) problem simulation solved using search tree algorithm and three game modes: Adversarial, Semi-Cooperative, and Fully Cooperative.


![image](https://github.com/user-attachments/assets/7f825568-bb6a-4b6e-bfe7-faeaa5a0155a)



## Overview

This project simulates a grid-based environment where two agents aim to deliver packages. The agents interact under different game settings:

1.   **Adversarial Mode**: Agents compete to maximize their own score and minimize the opponent's score using a minimax search algorithm with alpha-beta pruning.
2.   **Semi-Cooperative Mode**: Agents maximize their own score but break ties cooperatively.
3.   **Fully Cooperative Mode**: Agents work together to maximize the total number of packages delivered.

The environment is a grid-shaped graph where agents can move between vertices or remain in place. The simulation explores possible future states using a search tree algorithm and a heuristic function to evaluate non-terminal game states.

## The Search Tree Algorithm

The simulator uses a depth-limited search tree algorithm with alpha-beta pruning to explore and evaluate future states in the Multi-Agent Pickup and Delivery (MAPD) problem. The agents navigate a grid environment, where they must decide how to move in order to maximize their performance according to different game modes: Adversarial, Semi-Cooperative, and Fully Cooperative.

### Algorithm Overview
The search tree algorithm models the game as a sequence of alternating agent moves. At each step, the algorithm generates possible future states by simulating each agent’s actions, including movement (traverse) or remaining in place (no-op). These actions form the nodes of the search tree.

For each possible state, the algorithm calculates a score that estimates the desirability of that state. Since exploring the entire game tree would be computationally expensive, a **depth limit** is set to restrict how deep the algorithm explores.

To optimize the search, the algorithm uses **alpha-beta pruning** to skip branches of the search tree that cannot improve the outcome, effectively reducing the number of nodes evaluated. This makes the search more efficient while still finding an optimal move for the agents.

### Heuristic Evaluation
Because the game tree is too large to reach terminal states in most cases, the algorithm relies on a **heuristic function** to estimate the value of non-terminal states. This function evaluates the proximity of agents to package locations, whether packages have been picked up, and the likelihood of on-time delivery.

* Agents receive 1 point for each delivered package.
* 0.5 points for a package picked up but not yet delivered.
* 0.25 points for packages that have not been picked up.

### Game Mode Variations
* **Adversarial Mode (Zero-Sum Game)**: Each agent tries to maximize its own score while minimizing the opponent's score. It is done by using a min-max scoring system for the search tree, with the following calculation: TS1=IS1-IS2 and TS2=IS2-IS1.
TS = total score, IS = individual score.
* **Semi-Cooperative Mode**: Each agent focuses on maximizing its own individual score, but ties are broken in favor of maximazing the total score (cooperation). For agent 1 the following score will be calculated: TS1=IS1, breaking ties in favor of greater IS2
* **Fully Cooperative Mode**: Both agents work together as a team to maximize the combined score. TS1=TS2=IS1+IS2.
## Input File Format

The input is a text file specifies the grid dimensions, agent starting positions, package details, and blocked edges.

* #X <value>: Grid width.
* #Y <value>: Grid height.
* #P <x_pickup> <y_pickup> <pickup_time> <x_delivery> <y_delivery> <delivery_time>: Package.
* #B <x1> <y1> <x2> <y2>: Blocked edge.
* #A <x> <y> <agent_number>: Agent starting position.

Change the input parameters to affect the simulation.

### Example Input
#X 3 <br />
#Y 3 <br />
#P 1 0 0  D 2 0 4 <br />
#P 1 0 0  D 2 0 4 <br />
#P 0 2 0  D 0 3 4 <br />
#B 1 2 0 2 <br />
#B 1 1 1 2 <br />
#A 0 0 1 <br />
#A 3 0 2 <br />


## Usage

To run the simulation, execute:
```ruby
python3 main.py --input <path_to_input_file> --max_depth <max_depth> --time_limit <time_limit>
```
Example command:
```ruby
python3 main.py --input input.txt --max_depth 7 --time_limit 4
```

## Requirements

This project uses Python 3.x and requires no external libraries beyond Python’s standard library.
