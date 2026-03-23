import time
import heapq
from core.node import Node

def astar(maze, start_pos, end_pos, heuristic_func):
    """
    A* Search algorithm.
    """
    start_time = time.time()
    start_node = Node(start_pos, None, 0, heuristic_func(start_pos, end_pos))
    # Priority queue stores (f, node)
    pq = [(start_node.f, start_node)]
    
    # Track g_scores for each position
    g_score = {start_pos: 0}
    nodes_explored = 0
    
    path_found = None
    
    while pq:
        _, current_node = heapq.heappop(pq)

        # Skip stale entries: a better path to this position was already processed
        if current_node.g > g_score.get(current_node.position, float('inf')):
            continue

        nodes_explored += 1

        yield current_node, False
        
        if current_node.position == end_pos:
            path_found = current_node
            break
            
        for neighbor_pos in maze.get_neighbors(*current_node.position):
            tentative_g = g_score[current_node.position] + 1
            
            if neighbor_pos not in g_score or tentative_g < g_score[neighbor_pos]:
                g_score[neighbor_pos] = tentative_g
                h = heuristic_func(neighbor_pos, end_pos)
                new_node = Node(neighbor_pos, current_node, tentative_g, h)
                heapq.heappush(pq, (new_node.f, new_node))
                
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
