class Maze:
    """
    Manages the maze grid and states.
    0: Free path (White)
    1: Wall (Black)
    2: Start (Green)
    3: End (Red)
    """
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.starts = self._find_positions(2)
        self.ends = self._find_positions(3)

    def _find_positions(self, value):
        positions = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == value:
                    positions.append((r, c))
        return positions

    def is_valid_move(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c] != 1
        return False

    def get_neighbors(self, r, c):
        # Hierarchical order: Up -> Right -> Down -> Left
        moves = [
            (-1, 0), # Up
            (0, 1),  # Right
            (1, 0),  # Down
            (0, -1)  # Left
        ]
        neighbors = []
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if self.is_valid_move(nr, nc):
                neighbors.append((nr, nc))
        return neighbors

    def get_value(self, r, c):
        return self.grid[r][c]
