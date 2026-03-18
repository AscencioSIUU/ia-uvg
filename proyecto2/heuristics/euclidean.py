import math

def euclidean_distance(pos1, pos2):
    """
    Calculates the Euclidean distance between two positions.
    """
    (r1, c1) = pos1
    (r2, c2) = pos2
    return math.sqrt((r1 - r2)**2 + (c1 - c2)**2)
