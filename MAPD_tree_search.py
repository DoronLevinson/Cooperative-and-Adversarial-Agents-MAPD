import os


'''
PART 1: BASE FUNCTIONS
A. read_input
B. build_grid
'''

# A. read_input function:
# This function reads the input file to extract the following information:
# - Grid dimensions (x, y)
# - List of packages (Package objects) with their respective details
# - Two agents (Agent objects) and their initial positions
# - List of blocked edges where the agents are restricted from moving
# Returns:
# - x, y: integers, grid dimensions
# - packages: list of Package objects
# - agent1, agent2: two Agent objects representing the initial state of two agents
# - blocked_edges: list of blocked edges as tuples

def read_input(input_path):
    with open(input_path, 'r') as file:
        lines = file.readlines()

    # Initialize lists for packages and blocked edges
    packages = []
    blocked_edges = []

    # Parse the input file line by line
    for line in lines:
        # Parse grid dimension X
        if line.startswith('#X'):
            x = int(line.split()[1])
        # Parse grid dimension Y
        elif line.startswith('#Y'):
            y = int(line.split()[1])

        # Parse package details and create Package objects
        elif line.startswith('#P'):
            package_details = []
            elements = line.split()
            for element in elements:
                try:
                    package_details.append(int(element))
                except ValueError:
                    pass
            package = Package(package_details)
            packages.append(package)

        # Parse blocked edges (both directions are blocked)
        elif line.startswith('#B'):
            edge_coords = []
            elements = line.split()
            edge_coords.extend(map(int, elements[1:]))
            blocked_edge = ((edge_coords[0], edge_coords[1]), (edge_coords[2], edge_coords[3]))
            blocked_edge_reversed = ((edge_coords[2], edge_coords[3]), (edge_coords[0], edge_coords[1]))
            blocked_edges.extend([blocked_edge, blocked_edge_reversed])

        # Parse agent initial positions and assign them to agent1 or agent2
        elif line.startswith('#A'):
            elements = line.split()
            agent_x = int(elements[1])
            agent_y = int(elements[2])
            agent_num = int(elements[3])
            if agent_num == 1: 
                agent1 = Agent(agent_x,agent_y)
            else:
                agent2 = Agent(agent_x, agent_y)
        
    return (x, y, packages, agent1, agent2, blocked_edges)


# B. build_grid function:
# This function creates a grid (graph) representing the connectivity of vertices.
# Vertices are connected by edges unless blocked by the blocked_edges parameter.
# The grid is represented as a dictionary where each vertex has a list of its available neighbors.
# Returns:
# - graph: dictionary where keys are vertices and values are lists of adjacent vertices
def build_grid(x_limit, y_limit, blocked_edges):
    graph = {}

    # Initialize all vertices with empty neighbor lists
    for x in range(x_limit + 1):
        for y in range(y_limit + 1):
            graph[(x,y)] = []

    # Add neighboring vertices for each vertex (up, down, left, right)
    for x in range(x_limit + 1):
        for y in range(y_limit + 1):
            if x+1 <= x_limit:  graph[(x,y)].append((x+1,y))
            if x-1 >= 0:        graph[(x,y)].append((x-1,y))
            if y+1 <= y_limit:  graph[(x,y)].append((x,y+1))
            if y-1 >= 0:        graph[(x,y)].append((x,y-1))
        
    # Remove neighbors if they are blocked
    for edge in blocked_edges:
        vertex_1 = edge[0]
        vertex_2 = edge[1]
        if vertex_2 in graph[vertex_1]: graph[vertex_1].remove(vertex_2)
        if vertex_1 in graph[vertex_2]: graph[vertex_2].remove(vertex_1)
    
    return graph


'''
PART 2: CLASSES
A. Agent
B. Package
C. State
'''

# A. Agent class:
# This class represents an agent in the grid. 
# Each agent has a location and a score representing the number of delivered packages.
class Agent:
    def __init__(self, x, y):
        self.location = (x, y)  # Agent's current location on the grid
        self.score = 0          # Agent's score based on successfully delivered packages
    
    # Creates a copy of the agent (used for state expansion)
    def copy(self):
        agent_copy = Agent(0, 0)
        agent_copy.location = self.location
        agent_copy.score = self.score
        return agent_copy


# B. Package class:
# This class represents a package with its pickup and delivery details.
# It tracks the package's status, such as whether it's been picked up or delivered, 
# and which agent is responsible for it.
class Package:
    def __init__(self, details):
        self.pickup_location = (details[0], details[1])  # Location to pick up the package
        self.pickup_time = details[2]                   # Earliest time the package can be picked up
        self.delivery_location = (details[3], details[4])  # Location to deliver the package
        self.delivery_time = details[5]                   # Latest time for delivery
        self.picked_up = False                           # Flag for whether the package is picked up
        self.delivered = False                           # Flag for whether the package is delivered
        self.agent = 0                                   # Agent responsible for the package
    
    # Creates a copy of the package (used for state expansion)
    def copy(self):
        package_copy = Package([0, 0, 0, 0, 0, 0])
        package_copy.pickup_location = self.pickup_location
        package_copy.pickup_time = self.pickup_time
        package_copy.delivery_location = self.delivery_location
        package_copy.delivery_time = self.delivery_time
        package_copy.picked_up = self.picked_up
        package_copy.delivered = self.delivered
        package_copy.agent = self.agent
        return package_copy


# C. State class:
# This class encapsulates the complete state of the system, including:
# - The current time, agent positions, and the grid.
# - The list of packages and their status.
# It is used to track the progression of the system over time.
class State:
    def __init__(self, grid, _agent1, _agent2, _packages, time, ply):
        self.time = time             # Current time in the simulation
        self.ply = ply               # Turn number (used to alternate agents' turns)
        self.agent1 = _agent1.copy() # Copy of agent1 (to ensure no side effects)
        self.agent2 = _agent2.copy() # Copy of agent2
        self.grid = grid             # The grid representing the environment
        self.packages = [package.copy() for package in _packages]  # List of packages
        self.update()                # Update package statuses and scores based on the initial state

    # Creates a copy of the current state (used for state expansion)
    def copy(self):
        return State(self.grid, self.agent1.copy(), self.agent2.copy(), self.packages, self.time, self.ply)

    # Update agent1's location and increment the time and ply (turn number)
    def update_1(self, new_location):
        self.time += 1
        if new_location in self.grid[self.agent1.location] and new_location != self.agent2.location:
            self.agent1.location = new_location
        self.update()
        self.ply += 1

    # Update agent2's location and increment the ply (turn number)
    def update_2(self, new_location):
        if new_location in self.grid[self.agent2.location] and new_location != self.agent1.location:
            self.agent2.location = new_location
        self.update()
        self.ply += 1

    # Update the status of packages (picked up, delivered) and agents' scores
    def update(self):
        for package in self.packages:
            # Check if packages can be picked up
            if not package.picked_up and package.pickup_time <= self.time:
                # Agent 1 picks up the package
                if self.agent1.location == package.pickup_location:
                    package.picked_up = True
                    package.agent = 1
                # Agent 2 picks up the package
                if self.agent2.location == package.pickup_location:
                    package.picked_up = True
                    package.agent = 2           
            
            # Check if picked-up packages can be delivered
            if package.picked_up and not package.delivered and package.delivery_time >= self.time:
                # Agent 1 delivers the package
                if package.agent == 1 and self.agent1.location == package.delivery_location:
                    package.delivered = True
                    self.agent1.score += 1
                # Agent 2 delivers the package
                if package.agent == 2 and self.agent2.location == package.delivery_location:
                    package.delivered = True
                    self.agent2.score += 1


'''
PART 3: IMPORTANT FUNCTIONS
A. expand
B. heuristic_score
'''

# A. expand function:
# Recursive function that explores possible future states of the system by simulating agent movements.
# It performs depth-limited search using alpha-beta pruning to explore the best actions.
# Returns:
# - The best move for the current agent and the heuristic scores of both agents
def expand(state, depth=0, alpha=float('-inf'), beta=float('inf')):
    turn = 1 if state.ply % 2 == 0 else 2  # Determine the agent's turn (agent1 or agent2)

    # Base case: check if the search should terminate (due to time limit, depth, or package delivery)
    if state.time >= time_limit or depth >= max_depth or all(package.delivered or package.delivery_time < state.time for package in packages):
        p1, p2 = heuristic_score(state)  # Calculate heuristic scores for both agents
        return None, p1, p2
    
    location = state.agent1.location if turn == 1 else state.agent2.location  # Current agent's location
    # Define possible moves: no operation (stay), up, down, left, right
    up = (location[0], location[1]+1)
    down = (location[0], location[1]-1)
    right = (location[0] + 1, location[1])
    left = (location[0] - 1, location[1])
    no_op = (location[0], location[1])

    moves = [no_op, up, down, left, right]  # List of all possible moves
    max_score = float('-inf')
    max_move = None
    max_p2 = None
    max_p1 = None

    # Explore each move recursively
    for move in moves:
        new_state = state.copy()
        if turn == 1:
            new_state.update_1(move)  # Update state for agent1's move
        else:
            new_state.update_2(move)  # Update state for agent2's move
        new_move, p1, p2 = expand(new_state, depth + 1, alpha, beta)  # Recursively expand the next state

        # Calculate score based on the game mode
        if mode == 1:
            score = p1 - p2 if turn == 1 else p2 - p1  # Adversarial mode (maximize difference)
        if mode == 2:
            score = p1 if turn == 1 else p2  # Semi-cooperative mode (maximize individual score)
        if mode == 3:
            score = p1 + p2  # Fully cooperative mode (maximize joint score)

        # Update the best move based on the calculated score
        if score > max_score or (mode == 2 and score == max_score and (p2 > max_p2 or p1 > max_p1)):
            max_score = score
            max_p1 = p1
            max_p2 = p2
            max_move = move
        
        # Alpha-beta pruning: terminate branches that can't improve the result
        if mode == 1:
            if turn == 1:
                if beta < score:
                    break
                if alpha < score: alpha = score
            if turn == 2:
                if alpha > score * -1:
                    break
                if beta > score * -1: beta = score * -1
    
    return max_move, max_p1, max_p2


# B. heuristic_score function:
# Computes a heuristic score for both agents based on the current state.
# Heuristics include:
# - Package pickup status
# - Package delivery status
# - Score increments for delivering packages
# Returns:
# - agent1_heuristic: score estimate for agent1
# - agent2_heuristic: score estimate for agent2
def heuristic_score(state):
    agent1_heuristic = 0
    agent2_heuristic = 0

    for package in state.packages:
        # If the package is not picked up
        if not package.picked_up:
            agent1_heuristic += 0.25
            agent2_heuristic += 0.25
        # If the package is picked up but not delivered
        if package.picked_up and not package.delivered:
            if package.agent == 1:
                agent1_heuristic += 0.5
            if package.agent == 2:
                agent2_heuristic += 0.5
        # If the package is delivered
        if package.delivered:
            if package.agent == 1:
                agent1_heuristic += 1
            if package.agent == 2:
                agent2_heuristic += 1

    return agent1_heuristic, agent2_heuristic


'''
PART 4: MAIN
'''

##### Main ####
# Global variables defining simulation constraints
max_depth = 7
time_limit = 4

# Reading input from the input file
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')  # Change file path here if needed!
x, y, packages, agent1, agent2, blocked_edges = read_input(file_path)

# Build the grid and initialize the first state
grid = build_grid(x, y, blocked_edges)
time = 0
ply = 0
state_0 = State(grid, agent1, agent2, packages, time, ply)

# Simulate the game for each mode (adversarial, semi-cooperative, fully cooperative)
modes = {1: "adversarial", 2: "semi-cooperative", 3: "fully cooperative"}
for mode, mode_str in modes.items():
    time = 0
    game_over = False
    agent1_path = [agent1.location]
    agent2_path = [agent2.location]
    state = state_0.copy()
    state.update()

    # Continue the simulation until the time limit or game over condition
    while time < time_limit and not game_over:
        # Agent 1 makes a move
        move1, p1, p2 = expand(state)
        state.update_1(move1)

        # Agent 2 makes a move
        move2, p1, p2 = expand(state)
        state.update_2(move2)

        # Track the paths of both agents
        agent1_path.append(state.agent1.location)
        agent2_path.append(state.agent2.location)

        # Increment time
        time += 1

        # End the game if all packages are delivered or can't be delivered
        game_over = all(package.delivered or package.delivery_time <= state.time for package in state.packages)

    # Print the results for each mode
    print("")
    print(f"**** Game {mode} Results ****")
    print(f"Mode: {mode_str}")
    print(f"Agent 1: Score: {state.agent1.score}, Path: {agent1_path}")
    print(f"Agent 2: Score: {state.agent2.score}, Path: {agent2_path}")
    print("")

