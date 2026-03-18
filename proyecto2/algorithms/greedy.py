import time
import heapq
from core.node import Node

def greedy(maze, start_pos, end_pos, heuristic_func):
    """
    Greedy Best-First Search algorithm.
    """
    start_time = time.time()
    # For Greedy, g=0, h=heuristic
    start_node = Node(start_pos, None, 0, heuristic_func(start_pos, end_pos))
    # Priority queue stores (h, node)
    pq = [(start_node.h, start_node)]
    visited = {start_pos}
    nodes_explored = 0
    
    path_found = None
    
    while pq:
        _, current_node = heapq.heappop(pq)
        nodes_explored += 1
        
        yield current_node, False
        
        if current_node.position == end_pos:
            path_found = current_node
            break
            
        for neighbor_pos in maze.get_neighbors(*current_node.position):
            if neighbor_pos not in visited:
                visited.add(neighbor_pos)
                h = heuristic_func(neighbor_pos, end_pos)
                new_node = Node(neighbor_pos, current_node, 0, h)
                heapq.heappush(pq, (new_node.h, new_node))
                
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
