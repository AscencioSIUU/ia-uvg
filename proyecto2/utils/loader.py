def load_maze(file_path):
    """
    Loads a maze from a .txt file.
    """
    grid = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                # Remove whitespace and filter out empty lines
                row_str = line.strip()
                if row_str:
                    row = [int(char) for char in row_str]
                    grid.append(row)
        return grid
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except Exception as e:
        print(f"Error loading maze: {e}")
        return None
