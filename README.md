# Cooperative-and-Adversarial-Agents-in-MAPD-Problem
A Multi-Agent Pickup and Delivery (MAPD) problem simulation solved using search tree algorithm and three game modes: Adversarial, Semi-Cooperative, and Fully Cooperative.


Cooperative and Adversarial Agents in MAPD Problem
This project implements a simulator for the Multi-Agent Pickup and Delivery (MAPD) problem, where two agents interact in a shared environment to deliver packages. These agents, either cooperating or competing, must navigate a grid-shaped environment while seeking to optimize their performance under different game settings. The simulation implements three types of games: Adversarial, Semi-Cooperative, and Fully Cooperative, each requiring different strategies and objectives.

Overview
In the MAPD problem, two agents operate on a shared undirected graph (grid) where they pick up and deliver packages. Agents can move to adjacent vertices or remain in place (no-op). Each agent aims to maximize its score by delivering packages on time, while avoiding obstacles and respecting the movement rules (e.g., agents cannot traverse blocked edges or move to a vertex occupied by the other agent).

This project focuses on three different types of agent behavior:

Adversarial Game (Zero-Sum Game): Each agent tries to maximize its own score while minimizing the score of the opposing agent. The objective is to achieve the highest difference between their own score and the opponent's score. This is implemented using a minimax search algorithm with alpha-beta pruning to optimize decision-making.

Semi-Cooperative Game: Each agent seeks to maximize its individual score. However, in case of a tie, the agents cooperate to break the tie in favor of the agent that helps the other achieve a higher score.

Fully Cooperative Game: Both agents work together to maximize the sum of their scores, optimizing the total number of packages delivered on time.

The agents are controlled using a search tree algorithm that evaluates possible future states and chooses optimal actions based on the game type. A heuristic function is used to guide the search when the game tree is too large to explore fully.

Game Environment
The environment consists of a grid-shaped graph where each vertex represents a location, and edges represent paths between these locations. Each agent can perform the following actions:

Traverse: Move to an adjacent vertex, provided the edge is not blocked and the destination vertex is not occupied by the other agent.
No-op: Remain at the current location without moving.
Game Mechanics:
The game runs in turn-based pseudo-parallelism, where the agents take turns applying actions.
The game ends when no more packages can be delivered on time, or when the time limit is reached.
The agents can observe the entire state of the world and base their decisions on it.
Input File Format
The input file specifies the grid dimensions, agent starting positions, package details, and blocked edges. The format is as follows:

#X <value>: Specifies the grid width.
#Y <value>: Specifies the grid height.
#P <x_pickup> <y_pickup> <pickup_time> <x_delivery> <y_delivery> <delivery_time>: Defines a package.
#B <x1> <y1> <x2> <y2>: Specifies a blocked edge between two vertices.
#A <x> <y> <agent_number>: Specifies an agent's initial position and number (either 1 or 2).
Example Input File:
txt
Copy code
#X 5
#Y 5
#P 1 1 0 4 4 10
#P 3 3 2 5 5 12
#B 0 0 0 1
#A 0 0 1
#A 5 5 2
Usage
Running the Simulation
To run the simulation, execute the following command:

bash
Copy code
python3 main.py --input <path_to_input_file> --max_depth <max_depth> --time_limit <time_limit>
Arguments:
--input: The path to the input file (required).
--max_depth: Maximum depth for the search tree (optional, default is 7).
--time_limit: Maximum time limit for the simulation (optional, default is 4).
Example Command:
bash
Copy code
python3 main.py --input input.txt --max_depth 7 --time_limit 4
Output:
For each game mode (adversarial, semi-cooperative, fully cooperative), the simulation outputs:

Agent 1's score and path.
Agent 2's score and path.
The game mode used.
Example Output:
bash
Copy code
**** Game 1 Results ****
Mode: adversarial
Agent 1: Score: 2, Path: [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1)]
Agent 2: Score: 1, Path: [(5, 5), (4, 5), (3, 5), (3, 4), (3, 3)]

**** Game 2 Results ****
Mode: semi-cooperative
...

**** Game 3 Results ****
Mode: fully cooperative
...
Game Modes
1. Adversarial Mode:
This is a zero-sum game where each agent aims to maximize its own individual score (number of packages delivered on time) while minimizing the opponent’s score. The total score for each agent is calculated as:

makefile
Copy code
TS1 = IS1 - IS2
TS2 = IS2 - IS1
Here, TS1 and TS2 are the total scores of agents 1 and 2, and IS1 and IS2 represent their individual scores.

This mode uses a minimax algorithm with alpha-beta pruning to optimize the agents’ decisions by evaluating possible future states and choosing the best action to maximize the score difference.

2. Semi-Cooperative Mode:
In this mode, each agent tries to maximize its individual score (TS1 = IS1 and TS2 = IS2). Agents disregard the opponent's score unless there is a tie, in which case the tie is broken cooperatively by favoring the agent that helps the other achieve a higher score.
3. Fully Cooperative Mode:
In this mode, both agents work together to maximize the total number of packages delivered. The total score is the sum of both agents' individual scores:

makefile
Copy code
TS1 = TS2 = IS1 + IS2
Both agents aim to maximize the joint score by selecting actions that benefit the team as a whole.

Search Algorithm and Heuristic
Since the game tree can be too large to explore fully, a cutoff depth is applied to the search, and a heuristic static evaluation function is used to approximate the value of non-terminal states. The same heuristic is used across all game modes, though the agents' behavior differs depending on the type of game being played.

Heuristic Function:
The heuristic evaluates the proximity of agents to packages, whether packages have been picked up, and the likelihood of delivering packages on time.

Requirements
This project requires Python 3.x. No external libraries are needed beyond Python’s standard library.

Example
Here’s an example of running the script with an input file:

Input File (input.txt):
txt
Copy code
#X 4
#Y 4
#P 1 1 0 3 3 10
#B 2 2 2 3
#A 0 0 1
#A 4 4 2
Command:
bash
Copy code
python3 main.py --input input.txt --max_depth 7 --time_limit 4
Output:
bash
Copy code
**** Game 1 Results ****
Mode: adversarial
Agent 1: Score: 1, Path: [(0, 0), (1, 0), (1, 1), ...]
Agent 2: Score: 0, Path: [(4, 4), ...]

**** Game 2 Results ****
Mode: semi-cooperative
...

**** Game 3 Results ****
Mode: fully cooperative
...
Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

How to Contribute:
Fork the repository.
Create a new branch (git checkout -b feature/your-feature-name).
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature/your-feature-name).
Open a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.
