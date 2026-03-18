import pygame
import sys
import time
from core.maze import Maze
from utils.loader import load_maze
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.greedy import greedy
from algorithms.astar import astar
from heuristics.manhattan import manhattan_distance
from heuristics.euclidean import euclidean_distance

# Constants
CELL_SIZE = 5
MAZE_SIZE = 128
WIDTH = MAZE_SIZE * CELL_SIZE
HEIGHT = MAZE_SIZE * CELL_SIZE
SIDEBAR_WIDTH = 250
WINDOW_WIDTH = WIDTH + SIDEBAR_WIDTH
WINDOW_HEIGHT = HEIGHT

# Colors
COLOR_WALL = (0, 0, 0)         # 1: Black
COLOR_PATH = (255, 255, 255)   # 0: White
COLOR_START = (0, 255, 0)      # 2: Green
COLOR_END = (255, 0, 0)        # 3: Red
COLOR_EXPLORE = (0, 191, 255)  # Blue
COLOR_FINAL_PATH = (255, 255, 0) # Yellow
COLOR_BG = (230, 230, 230)
COLOR_TEXT = (0, 0, 0)
COLOR_BTN = (100, 100, 100)
COLOR_BTN_HOVER = (150, 150, 150)

class MazeApp:
    def __init__(self, maze_file):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Maze Solver Engineer")
        self.font = pygame.font.SysFont("Arial", 18)
        self.small_font = pygame.font.SysFont("Arial", 14)
        
        self.grid_data = load_maze(maze_file)
        self.maze = Maze(self.grid_data)
        
        self.algorithm = "BFS"
        self.heuristic = "Manhattan"
        self.speed = 0.001
        
        self.reset_state()
        
    def reset_state(self):
        self.exploring_cells = set()
        self.final_path_cells = set()
        self.current_generator = None
        self.solving = False
        self.metrics = None
        self.start_pos = self.maze.starts[0] if self.maze.starts else (0,0)
        self.end_pos = self.maze.ends[0] if self.maze.ends else (MAZE_SIZE-1, MAZE_SIZE-1)

    def draw_maze(self):
        for r in range(self.maze.rows):
            for c in range(self.maze.cols):
                val = self.maze.get_value(r, c)
                color = COLOR_PATH
                if val == 1: color = COLOR_WALL
                elif val == 2: color = COLOR_START
                elif val == 3: color = COLOR_END
                
                # Overlays
                if (r, c) in self.final_path_cells:
                    color = COLOR_FINAL_PATH
                elif (r, c) in self.exploring_cells:
                    color = COLOR_EXPLORE
                    
                pygame.draw.rect(self.screen, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw_sidebar(self):
        pygame.draw.rect(self.screen, COLOR_BG, (WIDTH, 0, SIDEBAR_WIDTH, HEIGHT))
        
        y = 20
        self.draw_text("MAZE SOLVER", WIDTH + 50, y, bold=True)
        y += 40
        
        self.draw_text(f"Algorithm: {self.algorithm}", WIDTH + 20, y)
        y += 30
        self.draw_text(f"Heuristic: {self.heuristic}", WIDTH + 20, y)
        y += 50
        
        # Buttons logic would go here, simplified for now
        self.draw_text("[1-4] Select Algo", WIDTH + 20, y, size=14)
        y += 20
        self.draw_text("[M/E] Select Heuristic", WIDTH + 20, y, size=14)
        y += 20
        self.draw_text("[SPACE] Solve", WIDTH + 20, y, size=14)
        y += 20
        self.draw_text("[R] Reset", WIDTH + 20, y, size=14)
        
        y += 60
        if self.metrics:
            self.draw_text("METRICS:", WIDTH + 20, y, bold=True)
            y += 30
            self.draw_text(f"Nodes: {self.metrics['nodes_explored']}", WIDTH + 20, y)
            y += 25
            self.draw_text(f"Path Len: {self.metrics['path_length']}", WIDTH + 20, y)
            y += 25
            self.draw_text(f"Time: {self.metrics['execution_time']:.4f}s", WIDTH + 20, y)
            y += 25
            self.draw_text(f"Branching: {self.metrics['branching_factor']:.2f}", WIDTH + 20, y)

    def draw_text(self, text, x, y, color=COLOR_TEXT, bold=False, size=18):
        txt_surface = self.font.render(text, True, color)
        if size == 14:
            txt_surface = self.small_font.render(text, True, color)
        self.screen.blit(txt_surface, (x, y))

    def start_solving(self):
        self.exploring_cells = set()
        self.final_path_cells = set()
        self.metrics = None
        
        h_func = manhattan_distance if self.heuristic == "Manhattan" else euclidean_distance
        
        if self.algorithm == "BFS":
            self.current_generator = bfs(self.maze, self.start_pos, self.end_pos)
        elif self.algorithm == "DFS":
            self.current_generator = dfs(self.maze, self.start_pos, self.end_pos)
        elif self.algorithm == "Greedy":
            self.current_generator = greedy(self.maze, self.start_pos, self.end_pos, h_func)
        elif self.algorithm == "A*":
            self.current_generator = astar(self.maze, self.start_pos, self.end_pos, h_func)
            
        self.solving = True

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: self.algorithm = "BFS"
                    if event.key == pygame.K_2: self.algorithm = "DFS"
                    if event.key == pygame.K_3: self.algorithm = "Greedy"
                    if event.key == pygame.K_4: self.algorithm = "A*"
                    if event.key == pygame.K_m: self.heuristic = "Manhattan"
                    if event.key == pygame.K_e: self.heuristic = "Euclidean"
                    if event.key == pygame.K_SPACE and not self.solving:
                        self.start_solving()
                    if event.key == pygame.K_r:
                        self.reset_state()

            if self.solving and self.current_generator:
                try:
                    res, is_final = next(self.current_generator)
                    if isinstance(res, dict): # Metrics
                        self.metrics = res
                        self.solving = False
                    else:
                        node = res
                        if is_final:
                            self.final_path_cells.add(node.position)
                        else:
                            self.exploring_cells.add(node.position)
                except StopIteration:
                    self.solving = False

            self.screen.fill((0,0,0))
            self.draw_maze()
            self.draw_sidebar()
            pygame.display.flip()
            # clock.tick(1000) # Control speed if needed

if __name__ == "__main__":
    app = MazeApp("maze_sample.txt")
    app.run()
