class Node:
    """
    Represents a state in the search space.
    """
    def __init__(self, position, parent=None, g=0, h=0):
        self.position = position  # (x, y)
        self.parent = parent      # Reference to parent Node
        self.g = g                # Cost from start to current node
        self.h = h                # Heuristic cost from current node to end
        self.f = g + h            # Total cost

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash(self.position)

    def __repr__(self):
        return f"Node({self.position}, f={self.f})"
