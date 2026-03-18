import random
import time
from core.maze import Maze
from utils.loader import load_maze
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.greedy import greedy
from algorithms.astar import astar
from heuristics.manhattan import manhattan_distance
from heuristics.euclidean import euclidean_distance

def run_simulation(maze_file, num_runs=5):
    grid_data = load_maze(maze_file)
    maze = Maze(grid_data)
    
    # Find all possible starting positions (0 or 2)
    possible_starts = []
    for r in range(maze.rows):
        for c in range(maze.cols):
            if maze.grid[r][c] in [0, 2]:
                possible_starts.append((r, c))
    
    end_pos = maze.ends[0] if maze.ends else (maze.rows-1, maze.cols-1)
    
    algorithms = ["BFS", "DFS", "Greedy (Manhattan)", "A* (Manhattan)"]
    results = {algo: [] for algo in algorithms}
    
    for i in range(num_runs):
        start_pos = random.choice(possible_starts)
        print(f"Run {i+1}/{num_runs} - Start: {start_pos}")
        
        # BFS
        for res, _ in bfs(maze, start_pos, end_pos):
            if isinstance(res, dict): results["BFS"].append(res)
            
        # DFS
        for res, _ in dfs(maze, start_pos, end_pos):
            if isinstance(res, dict): results["DFS"].append(res)
            
        # Greedy
        for res, _ in greedy(maze, start_pos, end_pos, manhattan_distance):
            if isinstance(res, dict): results["Greedy (Manhattan)"].append(res)
            
        # A*
        for res, _ in astar(maze, start_pos, end_pos, manhattan_distance):
            if isinstance(res, dict): results["A* (Manhattan)"].append(res)
            
    # Calculate averages
    print("\n" + "="*50)
    print(f"{'Algorithm':<20} | {'Nodes':<8} | {'Path':<8} | {'Time':<8}")
    print("-" * 50)
    
    for algo, metrics_list in results.items():
        if not metrics_list: continue
        avg_nodes = sum(m['nodes_explored'] for m in metrics_list) / len(metrics_list)
        avg_path = sum(m['path_length'] for m in metrics_list) / len(metrics_list)
        avg_time = sum(m['execution_time'] for m in metrics_list) / len(metrics_list)
        
        print(f"{algo:<20} | {avg_nodes:<8.1f} | {avg_path:<8.1f} | {avg_time:<8.4f}s")
    print("="*50)

if __name__ == "__main__":
    run_simulation("maze_sample.txt", num_runs=10)
