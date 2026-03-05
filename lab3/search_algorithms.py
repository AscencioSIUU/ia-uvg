from node import Node

def reconstruct_path(node):
    path = []
    current = node
    while current is not None:
        path.append(current.state)
        current = current.parent
    return path[::-1] # Invertimos la lista para que empiece desde el inicio

def graph_search(start_state, goal_state, graph, heuristics, queue, use_heuristic=False):
    # Creamos el nodo inicial
    start_node = Node(state=start_state, path_cost=0, heuristic=heuristics[start_state])
    queue.ADD(start_node)
    
    explored = set()
    
    while not queue.EMPTY():
        current_node = queue.POP()
        
        # Revisamos si es la meta
        if current_node.state == goal_state:
            return reconstruct_path(current_node), current_node.path_cost
            
        explored.add(current_node.state)
        
        # Revisamos si el nodo tiene conexiones en el grafo
        if current_node.state in graph:
            for neighbor, cost in graph[current_node.state].items():
                if neighbor not in explored:
                    # Costo acumulado
                    new_path_cost = current_node.path_cost + cost
                    
                    # h(n): Si no usamos heurística (como en UCS o BFS), será 0.
                    h_val = heuristics.get(neighbor, 0) if use_heuristic else 0
                    
                    child_node = Node(state=neighbor, 
                                      parent=current_node, 
                                      path_cost=new_path_cost, 
                                      heuristic=h_val)
                    queue.ADD(child_node)
                    
    return None, 0 # No se encontró camino