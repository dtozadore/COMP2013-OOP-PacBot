from enum import Enum
import numpy as np

# Define static map states using an enumeration for clarity
class StaticMapState(Enum):
    BLANK = 0
    SURVIVOR = 1
    WALL_VERTICAL = 2
    WALL_HORIZONTAL = 3
    WALL_T_UP = 4           # ⊥ Shape
    WALL_T_DOWN = 5         # T Shape
    WALL_T_TOP_RIGHT = 6    # ├ Shape (reads as wall on top, bottom, right)
    WALL_T_TOP_LEFT = 7     # ┤ Shape
    WALL_CORNER_NE = 8      # ┐
    WALL_CORNER_NW = 9      # ┌
    WALL_CORNER_SE = 10     # ┘
    WALL_CORNER_SW = 11     # └
    WALL_CROSS = 12         # +

class DynamicMapState(Enum):
    PACBOT = 0
    ALIEN = 1

pacbot_map = [
    # Row 0: Top Boundary
    [9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8],
    # Row 1: Top Lane (High Speed)
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 9, 3, 3, 3, 3, 3, 3, 3, 3, 8, 0, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 0, 9, 3, 3, 8, 0, 9, 3, 3, 3, 8, 0, 2, 2, 0, 9, 3, 3, 3, 8, 0, 9, 3, 3, 8, 0, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 0, 9, 3, 3, 3, 3, 3, 3, 3, 3, 8, 0, 2],
    [2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 2, 2, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 2, 0, 9, 3, 3, 3, 8, 0, 0, 2, 0, 2, 0, 9, 3, 3, 3, 3, 3, 3, 8, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 2, 2, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 9, 3, 3, 3, 3, 3, 3, 8, 0, 2, 0, 2, 0, 0, 9, 3, 3, 3, 8, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 11, 10, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 2],
    # Row 6: Survivors Cluster A (Left) and B (Right) in the loops
    [2, 0, 2, 0, 2, 1, 1, 1, 2, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 11, 3, 3, 10, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 11, 3, 3, 10, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 1, 1, 1, 0, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 11, 3, 3, 3, 10, 0, 0, 2, 0, 2, 0, 11, 3, 3, 3, 3, 3, 3, 10, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 9, 3, 8, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 11, 3, 3, 3, 3, 3, 3, 10, 0, 2, 0, 11, 3, 3, 3, 3, 3, 10, 0, 2, 0, 2],
    [2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 11, 3, 3, 3, 3, 3, 3, 3, 3, 10, 0, 11, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 10, 0, 9, 3, 3, 3, 3, 10, 0, 0, 0, 11, 3, 10, 0, 11, 3, 3, 3, 10, 0, 0, 0, 9, 3, 3, 3, 3, 8, 0, 11, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 10, 0, 9, 3, 3, 3, 3, 3, 3, 3, 3, 10, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 9, 3, 3, 3, 3, 3, 8, 0, 0, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 0, 0, 9, 4, 10, 0, 0, 9, 3, 3, 3, 3, 8, 0, 0, 0, 0, 0, 0, 0, 9, 3, 3, 3, 3, 8, 0, 0, 11, 4, 8, 0, 0, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 0, 0, 9, 3, 3, 3, 3, 3, 8, 0, 2],
    [2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 9, 3, 3, 3, 3, 8, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 2, 1, 1, 1, 1, 2, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 12, 0, 2, 1, 1, 1, 1, 2, 0, 12, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0],
    [2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 11, 3, 3, 3, 3, 10, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 11, 3, 3, 3, 3, 3, 10, 0, 0, 11, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 10, 0, 0, 11, 3, 3, 3, 3, 10, 0, 0, 0, 0, 2, 0, 9, 3, 3, 3, 3, 8, 0, 2, 0, 0, 0, 0, 11, 3, 3, 3, 3, 10, 0, 0, 11, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 10, 0, 0, 11, 3, 3, 3, 3, 3, 10, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 9, 3, 3, 3, 3, 3, 8, 0, 0, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 0, 0, 9, 3, 3, 3, 3, 8, 0, 0, 0, 0, 11, 3, 10, 0, 0, 0, 0, 11, 3, 10, 0, 0, 0, 0, 9, 3, 3, 3, 3, 8, 0, 0, 9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 0, 0, 9, 3, 3, 3, 3, 3, 8, 0, 2],
    [2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 2, 0, 9, 3, 3, 3, 10, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 11, 3, 3, 3, 8, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 11, 3, 3, 3, 8, 0, 0, 9, 3, 3, 3, 10, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 9, 3, 3, 3, 3, 3, 3, 3, 3, 8, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 11, 3, 3, 3, 8, 0, 0, 9, 3, 3, 3, 10, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 11, 3, 3, 3, 8, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 11, 3, 3, 3, 3, 10, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 11, 3, 3, 3, 3, 10, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 9, 3, 3, 3, 10, 0, 2, 0, 2],
    [2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2],
    [2, 0, 11, 3, 3, 3, 3, 3, 10, 0, 0, 9, 3, 3, 3, 10, 0, 0, 11, 3, 3, 3, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 3, 3, 3, 3, 3, 3, 3, 3, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 3, 3, 3, 10, 0, 0, 11, 3, 3, 3, 8, 0, 0, 11, 3, 3, 3, 3, 3, 10, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [11, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 10]
]

class Map:
    def __init__(self, dimensions, wall_initials, survivor_initials, pacbot_initials, alien_initials):
        """
        Args:
            dimensions (tuple): (rows, cols) e.g., (10, 10)
            wall_initials (list): List of (x, y) tuples for walls
            survivor_initials (list): List of (x, y) tuples for survivors
            pacbot_initials (list): List of dicts or tuples [{'id': 1, 'pos': (x,y)}, ...]
            alien_initials (list): List of dicts or tuples [{'id': 2, 'pos': (x,y)}, ...]
        """

        self.rows, self.cols = dimensions
        self.static_map = np.full((self.rows, self.cols), StaticMapState.BLANK, dtype=int)
        self.dynamic_positions = []
        
        # Helper to format data uniformly
        for p in pacbot_initials:
            self.dynamic_positions.append({
                'id': p['id'], 
                'pos': p['pos'], 
                'type': DynamicMapState.PACBOT
            })
            
        for a in alien_initials:
            self.dynamic_positions.append({
                'id': a['id'], 
                'pos': a['pos'], 
                'type': DynamicMapState.ALIEN
            })

    def print_map(grid):
        """Print the map grid to the console."""
        symbol_map = {
            StaticMapState.BLANK: ' ',
            StaticMapState.SURVIVOR: 'S',
            StaticMapState.WALL_VERTICAL: '|',
            StaticMapState.WALL_HORIZONTAL: '-',
            StaticMapState.WALL_T_UP: '⊥',
            StaticMapState.WALL_T_DOWN: 'T',
            StaticMapState.WALL_T_TOP_RIGHT: '├',
            StaticMapState.WALL_T_TOP_LEFT: '┤',
            StaticMapState.WALL_CORNER_NE: '┐',
            StaticMapState.WALL_CORNER_NW: '┌',
            StaticMapState.WALL_CORNER_SE: '┘',
            StaticMapState.WALL_CORNER_SW: '└',
            StaticMapState.WALL_CROSS: '+'
        }
        
        for row in grid:
            row_symbols = [symbol_map[StaticMapState(cell)] for cell in row]
            print(''.join(row_symbols))

    def set_map(self, new_map):
        """
        Set the entire static map from a 2D array.
        
        Args:
            new_map (list or np.ndarray): 2D array representing the new static map.
                Should have dimensions matching (self.rows, self.cols).
        
        Raises:
            ValueError: If the dimensions of new_map don't match the map dimensions.
        """
        new_map_array = np.array(new_map, dtype=int)
        
        if new_map_array.shape != (self.rows, self.cols):
            raise ValueError(
                f"Map dimensions mismatch: expected {(self.rows, self.cols)}, "
                f"got {new_map_array.shape}"
            )
        
        self.static_map = new_map_array

    def set(self, position, new_state):
        """
        Change position data on static map, given position and new state. 
        """
        r, c = position
        # Check bounds to be safe
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.static_map[r, c] = new_state

    def get(self, position):
        """
        Finds current state of given position.
        Cross references static and dynamic to find data. 
        """
        target_pos = tuple(position)

        # 1) Check dynamic positions first (Dynamic layers on top of static)
        for entity in self.dynamic_positions:
            if tuple(entity['pos']) == target_pos:
                return entity['type']

        # 2) If no dynamic entity found, check static map
        r, c = target_pos
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.static_map[r, c]
        
        return None # Out of bounds

    def update(self, identifier, new_position):
        """
        Updates dynamic position given identifier and new position. 
        """
        found = False
        for entity in self.dynamic_positions:
            if entity['id'] == identifier:
                entity['pos'] = new_position
                found = True
                break
        
        if not found:
            print(f"Warning: Entity with ID {identifier} not found.")

    def remove(self, identifier):
        """
        Removes item from dynamic position matrix given identifier. 
        """

        initial_count = len(self.dynamic_positions)
        self.dynamic_positions = [e for e in self.dynamic_positions if e['id'] != identifier]
        
        if len(self.dynamic_positions) == initial_count:
            print(f"Warning: Failed to remove. ID {identifier} not found.")