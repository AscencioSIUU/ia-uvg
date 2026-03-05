class Node:
    def __init__(self, state, parent=None, path_cost=0, heuristic=0, mode="astar"):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.heuristic = heuristic
        self.mode = mode

    def __lt__(self, other):
        if self.mode == "ucs":
            return self.path_cost < other.path_cost
        elif self.mode == "greedy":
            return self.heuristic < other.heuristic
        else:  # astar
            return (self.path_cost + self.heuristic) < (other.path_cost + other.heuristic)