import time
from collections import deque
from core.node import Node

def bfs(maze, start_pos, end_pos):
    """
    Breadth First Search algorithm.
    Yields the current node for visualization.
    Returns metrics upon completion.
    """
    start_time = time.time()
    start_node = Node(start_pos)
    queue = deque([start_node])
    visited = {start_pos}
    nodes_explored = 0
    
    # Track exploration for visualization
    path_found = None
    
    while queue:
        current_node = queue.popleft()
        nodes_explored += 1
        
        yield current_node, False # False means not final path
        
        if current_node.position == end_pos:
            path_found = current_node
            break
            
        # Hierarchical order: Up -> Right -> Down -> Left (handled by get_neighbors)
        for neighbor_pos in maze.get_neighbors(*current_node.position):
            if neighbor_pos not in visited:
                visited.add(neighbor_pos)
                new_node = Node(neighbor_pos, current_node)
                queue.append(new_node)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    path = []
    if path_found:
        curr = path_found
        while curr:
            path.append(curr.position)
            curr = curr.parent
            if curr:
                yield curr, True # True means it's part of the final path
    
    path_length = len(path)
    # Branching factor: average number of successors explored per node
    # Approximate b* = (nodes_explored - 1) / (nodes_explored - leaf_nodes) ? 
    # Usually it's (nodes_explored / depth) or similar.
    # Instruction says: "branching_factor: float"
    # A common way to calculate effective branching factor is nodes_explored / path_length
    branching_factor = nodes_explored / path_length if path_length > 0 else 0
    
    metrics = {
        "path_length": path_length,
        "nodes_explored": nodes_explored,
        "execution_time": execution_time,
        "branching_factor": branching_factor,
        "path": path[::-1]
    }
    
    yield metrics, None
