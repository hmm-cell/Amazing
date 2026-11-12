import random
from typing import Dict, List, Tuple, Set, Optional

#each orientation with its bit value
N = 1 #wall at north 0001
E = 2 #wall at east 0010
S = 4 #wall at south 0100
W = 8 #wall at wewst 1000
ALL = N | E | S | W #all sides walled 1111

LETTERS: dict[int, str] = {N: "N", E: "E", S: "S", W: "W"}

# IMPORTANT. direction is used to determine where youll move to.

# For example if youre at (x=2, y=3) and you move N youll end up at (x=2, y=2).
# Moving N from (2, 3) to (2, 2) means removing the N wall from (2, 3) and the S wall from (2, 2).
# Hence N has S as the third value in the dict. It tells the future
# wall remover function which wall to remove on the new cell.

# This repeats for all directions with their respective opposite: (N-S), (W-E)
# Everything in this project is (x, y): column first, then row.
# The matrix itself is stored as matrix[y][x] (rows first), like the output file.

DIRECTIONS: Dict[int, tuple[int, int, int]] = {
    N: (0, -1, S),
    S: (0, 1, N),
    E: (1, 0, W),
    W: (-1, 0, E),
}

#cell PATTERN of 42 symbol with its coords (x, y)

PATTERN_42: set[tuple[int, int]] = {
    #4 shape
    (0, 0), (0, 1), (0, 2),
    (1, 2), (2, 2), (2, 1),
    (2, 0), (2, 3), (2, 4),

    #2 shape
    (5, 0), (6, 0), (7, 0),
    (7, 1), (7, 2), (6, 2),
    (5, 2), (5, 3), (5, 4),
    (6, 4), (7, 4)
}

class Grid:
    """Grid of CELLS in the matrix, each cell is 4bit to determine the value of the respective 4 walls"""

#grid generator method, it puts every cell of the matrix at ALL(15) value
    def __init__(self, width: int, height: int, entry: tuple[int, int], exit: tuple[int, int], perfect: bool, seed: Optional[int] = None):
        if width < 1 or height < 1:
            raise ValueError("width and height must be biigger than (idk yet)")
        self.width = width
        self.height = height
        self.matrix: List[List[int]] = [[ALL for _ in range(width)] for _ in range(height)]
        self.fixed: Set[Tuple[int, int]] = set()
        self.entry = entry
        self.exit = exit
        self.perfect = perfect

        #defaulting seed to NONE
        #if its still NONE (not selected locked seed in menu), get a random seed
        if seed is None:
            seed = random.randint(0, 999999)
        self.seed = seed

        #atribute the seed value to rng object for the generator method
        self.rng = random.Random(self.seed)

        # get the width and heigth of the pattern.
        px_vals = [p[0] for p in PATTERN_42]
        py_vals = [p[1] for p in PATTERN_42]
        pattern_width = max(px_vals) - min(px_vals) + 1
        pattern_height = max(py_vals) - min(py_vals) + 1

        if self.width >= 10 and self.height >= 10:
            # get where the pattern starts in the middle of the grid
            ox = (self.width - pattern_width) // 2
            oy = (self.height - pattern_height) // 2

            # populate self.fixed with the locked cells of the pattern
            self.fixed = {(ox + px, oy + py) for px, py in PATTERN_42}
        else:
            print("Error: Grid is too small to fit the 42 pattern.")

    def is_fixed_cell(self, x: int, y: int) -> bool:
        return (x, y) in self.fixed

    """Raise ValueError if ENTRY or EXIT is inside the 42 pattern."""
    def check_entry_exit(self) -> bool:
        for name, (x, y) in (("ENTRY", self.entry), ("EXIT", self.exit)):
            if self.is_fixed_cell(x, y):
                raise ValueError(f"{name} ({x}, {y}) is inside the 42 pattern")
    
    # wall remover method, removes specific walls based on where the algo is randomly moving to
    def remove_wall(self, x: int, y: int, direction: int) -> None:
        # get coord movements and opposite wall from  DIRECTIONS cosnt
        dx, dy, opposite_wall = DIRECTIONS[direction]

        #go to the next direction
        nx = x + dx
        ny = y + dy

        if not ((0 <= nx < self.width) and (0 <= ny < self.height)):
            raise ValueError("out of bounds")

        # call is_fixed_cell to know if we are inside a locked cell or going to a locked cell
        # if in locked cell or going to locked cell no removal of wall
        if self.is_fixed_cell(x, y) or self.is_fixed_cell(nx, ny):
            raise ValueError("going to locked cell or in locked cell")
        
        # remove wall from current cell! ~negative bitwise operator. ~0001 = 1110
        # &operator is to check the ~direction vs the current cell and lets say 1111 to &1110 then we get 1110.
        # but if its &1110 and the cell is 1110, nothing is changed!
        self.matrix[y][x] &= ~direction
        self.matrix[ny][nx] &= ~opposite_wall

    def generate_maze(self) -> None:
        if self.perfect:
            self.perfect_maze()
        else:
            self.imperfect_maze()

    def perfect_maze(self) -> None:

        # Get all the unblocked cells
        available_cells = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if not self.is_fixed_cell(x, y)
        ]
        if not available_cells:
            raise ValueError("There are no available cells")

        # Choose the starting cell at random (for more variable maze designs)
        start = self.rng.choice(available_cells)
        visited: Set[Tuple[int, int]] = {start}
        stack: List[Tuple[int, int]] = [start]

        while stack:
            x, y = stack[-1]

            # Find all valid neighbours (unvisited, inbounds and unblocked)
            neighbours = []
            for direction, (dx, dy, _) in DIRECTIONS.items():
                nx = x + dx
                ny = y + dy
                if (
                    0 <= nx < self.width
                    and 0 <= ny < self.height
                    and (nx, ny) not in visited
                    and not self.is_fixed_cell(nx, ny)
                ):
                    neighbours.append((nx, ny, direction))

            # Choose a neighbor and move in (agressively)
            if neighbours:
                nx, ny, direction = self.rng.choice(neighbours)
                self.remove_wall(x, y, direction)
                visited.add((nx, ny))
                stack.append((nx, ny))

            # Go back if there's no neighbors
            else:
                stack.pop()

    # Function is called with the amount of walls to be removed. (int)
    def imperfect_maze(self, removed_walls: int = 10) -> None:
        if extra_walls < 0:
            raise ValueError("extra_walls cannot be negative")

        # Generate perfect maze
        self.generate_maze()

        # Aknowledge possible walls to be removed
        walls = []

        for y in range(self.height):
            for x in range(self.width):

                if self.is_fixed_cell(x, y):
                    continue

                # Only two directions so there's no repetition
                for direction in (E, S):
                    dx, dy, _ = DIRECTIONS[direction]
                    nx = x + dx
                    ny = y + dy

                    if not (0 <= nx < self.width and 0 <= ny < self.height):
                        continue

                    if self.is_fixed_cell(nx, ny):
                        continue
                        
                    if self.matrix[y][x] & direction:
                        walls.append((x, y, direction))

        # Randomly choose removed_walls walls to remove
        walls_to_remove = random.sample(
            walls,
            min(removed_walls, len(walls))
        )

        for x, y, direction in walls_to_remove:
            self.remove_wall(x, y, direction)

    def hex_convert(self) -> str:
        #convert values from ints inside list to hexadecimal str using join
        converted_rows = ["".join(format(x, "X") for x in row) for row in self.matrix]
        return "\n".join(converted_rows)