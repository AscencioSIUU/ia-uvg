import time
from core.node import Node

def dfs(maze, start_pos, end_pos):
    """
    Depth First Search algorithm.
    Yields the current node for visualization.
    Returns metrics upon completion.
    """
    start_time = time.time()
    start_node = Node(start_pos)
    stack = [start_node]
    visited = {start_pos}
    nodes_explored = 0
    
    path_found = None
    
    while stack:
        current_node = stack.pop()
        nodes_explored += 1
        
        yield current_node, False
        
        if current_node.position == end_pos:
            path_found = current_node
            break
            
        # Hierarchical order for DFS popping: Up -> Right -> Down -> Left
        # Since stack is LIFO, push neighbors in Reverse Order: Left -> Down -> Right -> Up
        neighbors = maze.get_neighbors(*current_node.position)
        # Neighbors are already returned in U-R-D-L order. Reverse them to push L-D-R-U.
        for neighbor_pos in reversed(neighbors):
            if neighbor_pos not in visited:
                visited.add(neighbor_pos)
                new_node = Node(neighbor_pos, current_node)
                stack.append(new_node)
                
    end_time = time.time()
    execution_time = end_time - start_time
    
    path = []
    if path_found:
        curr = path_found
        while curr:
            path.append(curr.position)
            curr = curr.parent
            if curr:
                yield curr, True
    
    path_length = len(path)
    branching_factor = nodes_explored / path_length if path_length > 0 else 0
    
    metrics = {
        "path_length": path_length,
        "nodes_explored": nodes_explored,
        "execution_time": execution_time,
        "branching_factor": branching_factor,
        "path": path[::-1]
    }
    
    yield metrics, None
