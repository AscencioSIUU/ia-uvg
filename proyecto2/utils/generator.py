import random

def generate_maze(rows, cols, wall_prob=0.3):
    maze = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if random.random() < wall_prob:
                row.append(1)
            else:
                row.append(0)
        maze.append(row)
    
    # Set start and end
    maze[1][1] = 2
    maze[rows-2][cols-2] = 3
    
    return maze

def save_maze(maze, file_path):
    with open(file_path, 'w') as f:
        for row in maze:
            f.write("".join(map(str, row)) + "\n")

if __name__ == "__main__":
    m = generate_maze(128, 128)
    save_maze(m, "maze_sample.txt")
