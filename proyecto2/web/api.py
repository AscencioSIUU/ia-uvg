import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from core.maze import Maze
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.greedy import greedy
from algorithms.astar import astar
from heuristics.manhattan import manhattan_distance
from heuristics.euclidean import euclidean_distance

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def run_algo_generator(algo_name, generator, websocket):
    """
    Wraps an algorithm generator and sends steps via WebSocket.
    """
    try:
        for step, is_final in generator:
            if isinstance(step, dict): # Metrics
                await websocket.send_json({
                    "type": "metrics",
                    "algo": algo_name,
                    "data": step
                })
            else: # Node
                await websocket.send_json({
                    "type": "step",
                    "algo": algo_name,
                    "pos": step.position,
                    "is_final": is_final
                })
            # Delay para animación observable (10ms por paso)
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Error in {algo_name}: {e}")

@app.websocket("/solve")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            grid = data.get("maze")
            heuristic_name = data.get("heuristic", "Manhattan")
            
            maze = Maze(grid)
            start_pos = maze.starts[0] if maze.starts else (0, 0)
            end_pos = maze.ends[0] if maze.ends else (len(grid)-1, len(grid[0])-1)
            
            h_func = manhattan_distance if heuristic_name == "Manhattan" else euclidean_distance
            
            # Create generators for all 4 algorithms
            generators = {
                "BFS": bfs(maze, start_pos, end_pos),
                "DFS": dfs(maze, start_pos, end_pos),
                "Greedy": greedy(maze, start_pos, end_pos, h_func),
                "A*": astar(maze, start_pos, end_pos, h_func)
            }
            
            # Run all algorithms in parallel (as much as asyncio allows)
            tasks = [run_algo_generator(name, gen, websocket) for name, gen in generators.items()]
            await asyncio.gather(*tasks)
            
            await websocket.send_json({"type": "complete"})
            
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
