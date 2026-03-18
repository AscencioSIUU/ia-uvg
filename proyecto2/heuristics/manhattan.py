import math

def manhattan_distance(pos1, pos2):
    """
    Calculates the Manhattan distance between two positions.
    """
    (r1, c1) = pos1
    (r2, c2) = pos2
    return abs(r1 - r2) + abs(c1 - c2)
