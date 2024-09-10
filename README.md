# Cooperative-and-Adversarial-Agents-in-MAPD-Problem
A Multi-Agent Pickup and Delivery (MAPD) problem simulation solved using search tree algorithm and three game modes: Adversarial, Semi-Cooperative, and Fully Cooperative.


![image](https://github.com/user-attachments/assets/7f825568-bb6a-4b6e-bfe7-faeaa5a0155a)



## Overview

This project simulates a grid-based environment where two agents aim to deliver packages. The agents interact under different game settings:

1.   **Adversarial Mode**: Agents compete to maximize their own score and minimize the opponent's score using a minimax search algorithm with alpha-beta pruning.
2.   **Semi-Cooperative Mode**: Agents maximize their own score but break ties cooperatively.
3.   **Fully Cooperative Mode**: Agents work together to maximize the total number of packages delivered.

The environment is a grid-shaped graph where agents can move between vertices or remain in place. The simulation explores possible future states using a search tree algorithm and a heuristic function to evaluate non-terminal game states.

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
